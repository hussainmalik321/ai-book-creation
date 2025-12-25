"""
Content API routes for the AI-Powered Book Assistant
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

router = APIRouter()


@router.get("/chapters")
async def get_chapters():
    """
    Get list of available chapters
    """
    try:
        # In a real implementation, this would fetch from the database
        # For now, return a mock response
        return {
            "chapters": [
                {
                    "id": "ch-1",
                    "title": "Introduction",
                    "sections": ["sec-1.1", "sec-1.2"]
                },
                {
                    "id": "ch-2",
                    "title": "Getting Started",
                    "sections": ["sec-2.1", "sec-2.2", "sec-2.3"]
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/chunk/{chunk_id}")
async def get_content_chunk(chunk_id: str):
    """
    Get specific content chunk by ID
    """
    try:
        # In a real implementation, this would fetch from the database/Qdrant
        # For now, return a mock response
        return {
            "chunk_id": chunk_id,
            "title": f"Content Chunk {chunk_id}",
            "content": f"This is the content for chunk {chunk_id}",
            "metadata": {
                "chapter": "Chapter 1",
                "section": "1.1",
                "position": 1
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/ingest")
async def ingest_content(content_data: Dict[str, Any]):
    """
    Ingest book content for indexing
    """
    try:
        from src.services.content_service import ContentService
        content_service = ContentService()

        # Check if content service is properly initialized
        if not content_service or not content_service.qdrant_client:
            raise HTTPException(status_code=503, detail="Content service is not available. Please check API keys and connections.")

        # Validate the content data
        if not isinstance(content_data, dict) or "book_data" not in content_data:
            raise HTTPException(status_code=400, detail="Invalid content data format. Expected 'book_data' key.")

        book_data = content_data["book_data"]
        if not isinstance(book_data, list):
            raise HTTPException(status_code=400, detail="book_data must be a list of content items.")

        success = await content_service.ingest_book_content(book_data)

        if success:
            return {
                "success": True,
                "message": "Content ingested successfully",
                "chunks_processed": len(book_data)
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to ingest content")
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/chunk-and-index")
async def chunk_and_index_content(content_data: Dict[str, Any]):
    """
    Chunk and index specific content
    """
    try:
        from src.services.content_service import ContentService
        content_service = ContentService()

        # Check if content service is properly initialized
        if not content_service or not content_service.qdrant_client:
            raise HTTPException(status_code=503, detail="Content service is not available. Please check API keys and connections.")

        content_id = content_data.get("content_id")
        content_text = content_data.get("content")

        if not content_id or not content_text:
            raise HTTPException(status_code=400, detail="content_id and content are required")

        # Simple chunking strategy - split by paragraphs or sentences
        import re
        # Split content into chunks (e.g., by paragraphs or by max length)
        paragraphs = content_text.split('\n\n')
        chunks = []

        for para in paragraphs:
            if len(para.strip()) > 0:
                # If paragraph is too long, split further
                if len(para) > 1000:  # Max chunk size
                    sentences = re.split(r'[.!?]+', para)
                    current_chunk = ""
                    for sentence in sentences:
                        if len(current_chunk + sentence) < 1000:
                            current_chunk += sentence + ". "
                        else:
                            if current_chunk.strip():
                                chunks.append(current_chunk.strip())
                            current_chunk = sentence + ". "
                    if current_chunk.strip():
                        chunks.append(current_chunk.strip())
                else:
                    chunks.append(para)

        success = await content_service.index_content_chunks(content_id, chunks)

        if success:
            return {
                "success": True,
                "message": f"Content {content_id} chunked and indexed successfully",
                "chunks_created": len(chunks)
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to chunk and index content")
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")