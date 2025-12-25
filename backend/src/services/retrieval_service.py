"""
Retrieval Service for the AI-Powered Book Assistant
Handles content retrieval and similarity search
"""
from typing import List, Dict, Any, Optional
from src.core.config import settings
from src.services.content_service import ContentService
from src.core.cache import cache
import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)


class RetrievalService:
    def __init__(self):
        self.content_service = ContentService()
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            # Use the newer embeddings API instead of the deprecated EmbeddingModel
            self.embedding_model = "embedding-001"  # Just store the model name for later use
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Could not initialize Gemini API: {e}")
            self.embedding_model = None

    async def create_embedding(self, text: str) -> List[float]:
        """
        Create embedding for the given text using Gemini API with caching
        """
        try:
            # Create cache key from text
            import hashlib
            cache_key = hashlib.md5(text.encode()).hexdigest()

            # Try to get from cache first
            cached_embedding = cache.get(cache_key)
            if cached_embedding:
                return cached_embedding

            # Check if embedding model is initialized
            if not self.embedding_model:
                logger.warning("Embedding model not initialized, returning zero vector")
                return [0.0] * 768

            # Use the newer embeddings API with correct model
            import google.generativeai as genai
            response = genai.embed_content(
                model="models/text-embedding-004",
                content=[text],
                task_type="RETRIEVAL_DOCUMENT"
            )
            embedding = response['embedding'][0] if response['embedding'] else [0.0] * 768

            # Cache the result
            cache.set(cache_key, embedding)

            return embedding
        except Exception as e:
            logger.error(f"Failed to create embedding for text: {str(e)}")
            # Return a zero vector as fallback
            return [0.0] * 768

    async def retrieve_relevant_content(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant content based on the query
        """
        try:
            # Create embedding for the query
            query_embedding = await self.create_embedding(query)

            # Search for relevant content
            results = await self.content_service.search_content(
                query_vector=query_embedding,
                limit=limit
            )

            return results
        except Exception as e:
            logger.error(f"Failed to retrieve relevant content: {str(e)}")
            return []

    async def retrieve_content_by_selection(self, selected_text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve content specifically based on selected text only
        This method restricts context to the selected text
        """
        try:
            # Create embedding for the selected text
            selection_embedding = await self.create_embedding(selected_text)

            # Search for content related to the selected text
            results = await self.content_service.search_content(
                query_vector=selection_embedding,
                limit=limit
            )

            # Ensure we only return content that's highly relevant to the selection
            # This is where we enforce the "selection-based" constraint
            filtered_results = []
            for result in results:
                # Add additional filtering to ensure relevance to selected text
                if self._is_relevant_to_selection(result, selected_text):
                    filtered_results.append(result)

            # If no highly relevant content is found, return the selected text itself as context
            if not filtered_results:
                # Create a pseudo-content item from the selected text
                pseudo_content = {
                    "id": "selected_text_only",
                    "title": "Selected Text",
                    "content": selected_text,
                    "chunk_text": selected_text,
                    "metadata": {"source": "user_selection"},
                    "relations": [],
                    "score": 1.0
                }
                filtered_results = [pseudo_content]

            return filtered_results
        except Exception as e:
            logger.error(f"Failed to retrieve content by selection: {str(e)}")
            return []

    def _is_relevant_to_selection(self, content: Dict[str, Any], selected_text: str) -> bool:
        """
        Check if content is highly relevant to the selected text
        This is a simple heuristic - in practice, you might use more sophisticated methods
        """
        # Simple check: see if the selected text appears in the content or vice versa
        content_text = content.get("content", "") or content.get("chunk_text", "")
        selected_lower = selected_text.lower()
        content_lower = content_text.lower()

        # Check if there's overlap between the selected text and the content
        # This is a basic heuristic - you could make this more sophisticated
        if selected_lower in content_lower or content_lower in selected_lower:
            return True

        # Additional check: if they share common keywords
        selected_words = set(selected_lower.split()[:10])  # First 10 words as keywords
        content_words = set(content_lower.split()[:20])   # First 20 words from content
        common_words = selected_words.intersection(content_words)

        # If more than 2 common words, consider it relevant
        return len(common_words) > 2

    async def get_content_by_id(self, content_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve specific content by ID
        """
        try:
            content = await self.content_service.get_content_by_id(content_id)
            return content
        except Exception as e:
            logger.error(f"Failed to get content by ID {content_id}: {str(e)}")
            return None