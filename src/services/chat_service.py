"""
Chat Service for the AI-Powered Book Assistant
Orchestrates the chat functionality
"""
from typing import Dict, Any, Optional, List
from src.models.user_query import UserQuery, UserQueryCreate
from src.models.response import Response, ResponseCreate
from src.models.chat_session import ChatSession, ChatSessionCreate
from src.services.retrieval_service import RetrievalService
from src.services.generation_service import GenerationService
from src.core.exceptions import InvalidQueryException, ContentRestrictionException
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self):
        try:
            self.retrieval_service = RetrievalService()
            self.generation_service = GenerationService()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error initializing chat services: {e}")
            self.retrieval_service = None
            self.generation_service = None

        # In-memory session storage for demo purposes
        # In production, use a database or Redis
        self.sessions = {}

    async def process_query(self, query_data: UserQueryCreate) -> Response:
        """
        Process a user query and generate a response
        """
        try:
            # Validate the query
            await self._validate_query(query_data)

            # Check if services are properly initialized
            if not hasattr(self, 'retrieval_service') or not hasattr(self, 'generation_service'):
                logger.error("ChatService not properly initialized - services missing")
                return Response(
                    id=str(uuid.uuid4()),
                    query_id="",
                    response_text="Service is not properly initialized. Please check API keys and connections.",
                    source_chunks=[],
                    confidence_score=0.0,
                    is_fallback=True,
                    timestamp=datetime.utcnow()
                )

            if not self.retrieval_service or not self.generation_service:
                return Response(
                    id=str(uuid.uuid4()),
                    query_id="",
                    response_text="Service is not properly initialized. Please check API keys and connections.",
                    source_chunks=[],
                    confidence_score=0.0,
                    is_fallback=True,
                    timestamp=datetime.utcnow()
                )

            # Retrieve relevant content based on query type
            context = []
            if query_data.query_type == "SELECTION_QA":
                if not query_data.selected_text:
                    raise InvalidQueryException("Selected text is required for selection-based queries")
                context = await self.retrieval_service.retrieve_content_by_selection(
                    query_data.selected_text
                )

                # Enforce content restriction for selection-based queries
                context = await self.enforce_content_restriction(
                    query_data.query_type,
                    query_data.selected_text,
                    context
                )
            else:
                context = await self.retrieval_service.retrieve_relevant_content(
                    query_data.query_text
                )

            # Generate response using the context
            generation_result = await self.generation_service.generate_response(
                query=query_data.query_text,
                context=context,
                query_type=query_data.query_type
            )

            # Create response object
            response_id = str(uuid.uuid4())
            response = Response(
                id=response_id,
                query_id="",  # Will be set after creating the query
                response_text=generation_result["response_text"],
                source_chunks=generation_result["source_chunks"],
                confidence_score=generation_result["confidence_score"],
                is_fallback=generation_result["is_fallback"],
                timestamp=datetime.utcnow()
            )

            # Add to session history if session_id is provided
            if query_data.session_id:
                await self.add_to_session_history(
                    query_data.session_id,
                    query_data.query_text,
                    generation_result["response_text"]
                )

            return response
        except Exception as e:
            logger.error(f"Failed to process query: {str(e)}")
            # Return a fallback response
            fallback_response = Response(
                id=str(uuid.uuid4()),
                query_id="",
                response_text="I'm sorry, I encountered an error while processing your request. Please try again.",
                source_chunks=[],
                confidence_score=0.0,
                is_fallback=True,
                timestamp=datetime.utcnow()
            )

            # Add to session history if session_id is provided
            if query_data.session_id:
                await self.add_to_session_history(
                    query_data.session_id,
                    query_data.query_text,
                    fallback_response.response_text
                )

            return fallback_response

    async def _validate_query(self, query_data: UserQueryCreate) -> None:
        """
        Validate the user query
        """
        if not query_data.query_text or not query_data.query_text.strip():
            raise InvalidQueryException("Query text cannot be empty")

        if query_data.query_type == "SELECTION_QA" and not query_data.selected_text:
            raise InvalidQueryException("Selected text is required for selection-based queries")

        # Additional validation can be added here


    async def create_session(self, session_data: ChatSessionCreate) -> ChatSession:
        """
        Create a new chat session
        """
        try:
            session_id = str(uuid.uuid4())
            session = ChatSession(
                id=session_id,
                user_id=session_data.user_id,
                start_time=datetime.utcnow(),
                last_activity=datetime.utcnow(),
                active=True
            )

            # Store session in memory
            self.sessions[session_id] = {
                "session": session,
                "history": []
            }

            return session
        except Exception as e:
            logger.error(f"Failed to create session: {str(e)}")
            raise

    async def add_to_session_history(self, session_id: str, query: str, response: str) -> bool:
        """
        Add a query-response pair to the session history
        """
        try:
            if session_id in self.sessions:
                self.sessions[session_id]["history"].append({
                    "query": query,
                    "response": response,
                    "timestamp": datetime.utcnow()
                })
                # Update last activity
                self.sessions[session_id]["session"].last_activity = datetime.utcnow()
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to add to session history: {str(e)}")
            return False

    async def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get the conversation history for a session
        """
        try:
            if session_id in self.sessions:
                return self.sessions[session_id]["history"]
            return []
        except Exception as e:
            logger.error(f"Failed to get session history: {str(e)}")
            return []

    async def update_session_activity(self, session_id: str) -> bool:
        """
        Update the last activity timestamp for a session
        """
        try:
            # In a real implementation, this would update the session in the database
            # For now, we'll just log the activity
            logger.info(f"Session {session_id} activity updated")
            return True
        except Exception as e:
            logger.error(f"Failed to update session activity: {str(e)}")
            return False

    async def enforce_content_restriction(
        self,
        query_type: str,
        selected_text: Optional[str],
        retrieved_content: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Enforce content restrictions based on query type
        """
        if query_type == "SELECTION_QA":
            if not selected_text:
                raise ContentRestrictionException("Selection-based query requires selected text")

            # Filter retrieved content to only include items related to the selected text
            filtered_content = []
            for item in retrieved_content:
                if self._is_content_related_to_selection(item, selected_text):
                    filtered_content.append(item)

            if not filtered_content:
                # If no content matches, return a limited response
                return [{
                    "id": "no_content",
                    "title": "No Relevant Content",
                    "content": "No content found that is directly related to your selected text.",
                    "chunk_text": "No content found that is directly related to your selected text.",
                    "metadata": {},
                    "relations": [],
                    "score": 0.0
                }]

            return filtered_content
        else:
            # For GLOBAL_QA, return all content
            return retrieved_content

    def _is_content_related_to_selection(self, content: Dict[str, Any], selected_text: str) -> bool:
        """
        Check if content is related to the selected text
        """
        content_text = content.get("content", "") or content.get("chunk_text", "")
        selected_lower = selected_text.lower()
        content_lower = content_text.lower()

        # Simple check: see if the selected text appears in the content or vice versa
        if selected_lower in content_lower or content_lower in selected_lower:
            return True

        # Check for keyword overlap
        selected_words = set(selected_lower.split()[:10])
        content_words = set(content_lower.split()[:20])
        common_words = selected_words.intersection(content_words)

        return len(common_words) > 2