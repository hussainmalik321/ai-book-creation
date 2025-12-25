"""
Chat API routes for the AI-Powered Book Assistant
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from datetime import datetime
import uuid

from src.models.user_query import UserQueryCreate, QueryType
from src.models.response import Response, SourceChunk
from src.models.chat_session import ChatSessionCreate
from src.services.chat_service import ChatService
from src.core.exceptions import BookAssistantException
from src.core.config import settings

router = APIRouter()


# Initialize chat service
try:
    chat_service = ChatService()
except Exception as e:
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"Failed to initialize chat service: {e}")
    chat_service = None


@router.post("/query", response_model=Response)
async def query_endpoint(
    query_data: UserQueryCreate
):
    """
    Submit a query to the AI assistant
    """
    try:
        # Process the query
        response = await chat_service.process_query(query_data)

        # Set the query_id to a generated ID since we don't have a real query record
        response.query_id = str(uuid.uuid4())

        return response
    except BookAssistantException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """
    Get session information and history
    """
    try:
        # In a real implementation, this would fetch from the database
        # For now, return a mock response
        return {
            "session_id": session_id,
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "active": True,
            "query_history": []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/session")
async def create_session(session_data: ChatSessionCreate = None):
    """
    Create a new chat session
    """
    try:
        # Check if chat service is initialized
        if not chat_service:
            raise HTTPException(status_code=503, detail="Chat service is not available. Please check API keys and connections.")

        if session_data is None:
            session_data = ChatSessionCreate()

        session = await chat_service.create_session(session_data)
        return {
            "session_id": session.id,
            "created_at": session.start_time,
            "active": session.active
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Additional validation for the query endpoint
@router.post("/query", response_model=Response)
async def query_endpoint_with_validation(query_data: UserQueryCreate):
    """
    Submit a query to the AI assistant with validation
    """
    try:
        # Check if chat service is initialized
        if not chat_service:
            raise HTTPException(status_code=503, detail="Chat service is not available. Please check API keys and connections.")

        # Validate query data
        if not query_data.query_text or not query_data.query_text.strip():
            raise HTTPException(status_code=400, detail="Query text is required")

        if query_data.query_type == QueryType.SELECTION_QA and not query_data.selected_text:
            raise HTTPException(status_code=400, detail="Selected text is required for selection-based queries")

        # Process the query
        response = await chat_service.process_query(query_data)

        # Set the query_id to a generated ID since we don't have a real query record
        response.query_id = str(uuid.uuid4())

        return response
    except BookAssistantException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/query/selection", response_model=Response)
async def selection_query_endpoint(query_data: UserQueryCreate):
    """
    Submit a selection-based query to the AI assistant
    """
    try:
        # Check if chat service is initialized
        if not chat_service:
            raise HTTPException(status_code=503, detail="Chat service is not available. Please check API keys and connections.")

        # Validate query data specifically for selection-based queries
        if not query_data.query_text or not query_data.query_text.strip():
            raise HTTPException(status_code=400, detail="Query text is required")

        if query_data.query_type != QueryType.SELECTION_QA:
            raise HTTPException(status_code=400, detail="This endpoint is for selection-based queries only")

        if not query_data.selected_text:
            raise HTTPException(status_code=400, detail="Selected text is required for selection-based queries")

        # Process the query
        response = await chat_service.process_query(query_data)

        # Set the query_id to a generated ID since we don't have a real query record
        response.query_id = str(uuid.uuid4())

        return response
    except BookAssistantException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")