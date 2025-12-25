"""
Generation Service for the AI-Powered Book Assistant
Handles AI generation using Gemini API
"""
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from src.core.config import settings
from src.models.response import SourceChunk
import logging

logger = logging.getLogger(__name__)


class GenerationService:
    def __init__(self):
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMINI_MODEL_NAME)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Could not initialize Gemini API: {e}")
            self.model = None

    async def generate_response(
        self,
        query: str,
        context: List[Dict[str, Any]],
        query_type: str = "GLOBAL_QA"
    ) -> Dict[str, Any]:
        """
        Generate a response based on the query and context
        """
        try:
            # Check if model is initialized
            if not self.model:
                logger.warning("Generation model not initialized, returning fallback response")
                return {
                    "response_text": "Service is not properly initialized. Please check API keys and connections.",
                    "source_chunks": [],
                    "confidence_score": 0.0,
                    "is_fallback": True
                }

            # Prepare the context for the model
            context_text = self._prepare_context(context, query_type)

            # Create the prompt for the model
            prompt = self._create_prompt(query, context_text, query_type)

            # Generate the response
            response = await self._call_gemini_api(prompt)

            # Calculate a confidence score based on the response
            confidence_score = self._calculate_confidence_score(response, context)

            return {
                "response_text": response,
                "source_chunks": self._extract_source_chunks(context),
                "confidence_score": confidence_score,
                "is_fallback": not response or response.strip().lower().startswith("i don't know")
            }
        except Exception as e:
            logger.error(f"Failed to generate response: {str(e)}")
            return {
                "response_text": "I'm sorry, I encountered an error while processing your request. Please try again.",
                "source_chunks": [],
                "confidence_score": 0.0,
                "is_fallback": True
            }

    def _prepare_context(self, context: List[Dict[str, Any]], query_type: str) -> str:
        """
        Prepare context text based on query type
        """
        if not context:
            return ""

        if query_type == "SELECTION_QA":
            # For selection-based queries, only use the selected text context
            context_parts = []
            for item in context:
                content = item.get("content", "") or item.get("chunk_text", "")
                if content.strip():
                    context_parts.append(f"Content: {content}")
            return "\n\n".join(context_parts)
        else:
            # For global queries, use all available context
            context_parts = []
            for item in context:
                title = item.get("title", "Untitled")
                content = item.get("content", "") or item.get("chunk_text", "")
                if content.strip():
                    context_parts.append(f"Title: {title}\nContent: {content}")
            return "\n\n".join(context_parts)

    def _create_prompt(self, query: str, context: str, query_type: str) -> str:
        """
        Create a prompt for the Gemini model
        """
        if query_type == "SELECTION_QA":
            return f"""
            You are an AI assistant for a book. Answer the user's question based ONLY on the provided selected text. Do not use any external knowledge or information beyond what is provided below.

            Selected Text:
            {context}

            Question: {query}

            Answer: """
        else:
            return f"""
            You are an AI assistant for a book. Based on the following book content, answer the user's question:

            Context:
            {context}

            Question: {query}

            Answer: """

    async def _call_gemini_api(self, prompt: str) -> str:
        """
        Call the Gemini API to generate a response
        """
        try:
            # Check if model is initialized
            if not self.model:
                logger.warning("Generation model not initialized, returning fallback response")
                return "Service is not properly initialized. Please check API keys and connections."

            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 1000,
                    "candidate_count": 1
                }
            )
            return response.text if response.text else ""
        except Exception as e:
            logger.error(f"Gemini API call failed: {str(e)}")
            return "I'm sorry, I couldn't generate a response at this time."

    def _calculate_confidence_score(self, response: str, context: List[Dict[str, Any]]) -> float:
        """
        Calculate a confidence score based on the response and context
        """
        if not response or not context:
            return 0.0

        # Simple heuristic: if the response contains information from the context,
        # it's likely more confident
        response_lower = response.lower()
        context_matches = 0
        total_context_parts = 0

        for item in context:
            content = item.get("content", "") or item.get("chunk_text", "")
            if content.strip():
                total_context_parts += 1
                if content.lower() in response_lower:
                    context_matches += 1

        if total_context_parts > 0:
            base_score = context_matches / total_context_parts
        else:
            base_score = 0.5  # Default score if no context

        # Adjust score based on response length and coherence
        response_length = len(response.split())
        if response_length < 10:
            base_score *= 0.7  # Lower score for very short responses

        return min(base_score, 1.0)  # Ensure score is between 0 and 1

    def _extract_source_chunks(self, context: List[Dict[str, Any]]) -> List[SourceChunk]:
        """
        Extract source chunks from the context with proper attribution
        """
        source_chunks = []
        for item in context:
            # Ensure we have proper attribution information
            content_id = item.get("id", "")
            title = item.get("title", "Untitled")
            text = item.get("content", "") or item.get("chunk_text", "")

            # Only include items with meaningful content
            if text.strip():
                source_chunk = SourceChunk(
                    content_id=content_id,
                    title=title,
                    text=text
                )
                source_chunks.append(source_chunk)
        return source_chunks

    async def validate_response_quality(self, response: str, context: List[Dict[str, Any]]) -> bool:
        """
        Validate if the response quality is acceptable
        """
        if not response or len(response.strip()) < 10:
            return False

        # Check if response is just saying "I don't know" or similar
        response_lower = response.lower()
        if any(phrase in response_lower for phrase in [
            "i don't know", "i do not know", "not mentioned", "not specified",
            "not provided", "no information", "not found in the text", "no content found"
        ]):
            return False

        return True

    def check_content_existence(self, query: str, context: List[Dict[str, Any]]) -> bool:
        """
        Check if the content exists to answer the query
        """
        if not context:
            return False

        # Simple check: if context is empty or contains no meaningful content
        for item in context:
            content = item.get("content", "") or item.get("chunk_text", "")
            if content.strip():
                return True

        return False