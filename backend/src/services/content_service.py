"""
Content Service for the AI-Powered Book Assistant
Handles book content management, ingestion, and indexing
"""
from typing import List, Optional, Dict, Any
from src.models.book_content import BookContent, BookContentCreate
from src.core.config import settings
from qdrant_client import QdrantClient
from qdrant_client.http import models
import logging

logger = logging.getLogger(__name__)


class ContentService:
    def __init__(self):
        self.collection_name = "book_content"
        try:
            self.qdrant_client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
                prefer_grpc=False
            )
            self._init_collection()
        except Exception as e:
            # Log the error but don't crash the service
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Could not initialize Qdrant client: {e}")
            self.qdrant_client = None

    def _init_collection(self):
        """
        Initialize the Qdrant collection for book content
        """
        try:
            # Check if collection exists
            self.qdrant_client.get_collection(self.collection_name)
        except:
            # Create collection if it doesn't exist
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),  # Assuming 768-dim embeddings
            )
            logger.info(f"Created Qdrant collection: {self.collection_name}")

    async def create_content(self, content: BookContentCreate) -> BookContent:
        """
        Create and index a new content chunk
        """
        import uuid
        from datetime import datetime

        content_id = str(uuid.uuid4())

        # Create the content object
        book_content = BookContent(
            id=content_id,
            title=content.title,
            content=content.content,
            chunk_text=content.chunk_text,
            metadata=content.metadata,
            embedding_vector=content.embedding_vector,
            relations=content.relations,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Index in Qdrant if embedding exists
        if content.embedding_vector:
            await self._index_content(book_content)

        return book_content

    async def _index_content(self, content: BookContent):
        """
        Index content in Qdrant for retrieval
        """
        try:
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=content.id,
                        vector=content.embedding_vector or [],
                        payload={
                            "title": content.title,
                            "content": content.content,
                            "chunk_text": content.chunk_text,
                            "metadata": content.metadata,
                            "relations": content.relations
                        }
                    )
                ]
            )
            logger.info(f"Indexed content {content.id} in Qdrant")
        except Exception as e:
            logger.error(f"Failed to index content {content.id} in Qdrant: {str(e)}")
            raise

    async def search_content(self, query_vector: List[float], limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for relevant content based on query vector
        """
        try:
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )

            results = []
            for hit in search_results:
                results.append({
                    "id": str(hit.id),  # Convert to string for Pydantic validation
                    "title": hit.payload.get("title", ""),
                    "content": hit.payload.get("content", ""),
                    "chunk_text": hit.payload.get("chunk_text", ""),
                    "metadata": hit.payload.get("metadata", {}),
                    "relations": hit.payload.get("relations", []),
                    "score": hit.score
                })

            return results
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            raise

    async def get_content_by_id(self, content_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve content by ID
        """
        try:
            records = self.qdrant_client.retrieve(
                collection_name=self.collection_name,
                ids=[content_id]
            )

            if records:
                record = records[0]
                return {
                    "id": content_id,
                    "title": record.payload.get("title", ""),
                    "content": record.payload.get("content", ""),
                    "chunk_text": record.payload.get("chunk_text", ""),
                    "metadata": record.payload.get("metadata", {}),
                    "relations": record.payload.get("relations", [])
                }
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve content {content_id}: {str(e)}")
            return None

    async def ingest_book_content(self, book_data: List[Dict[str, Any]]) -> bool:
        """
        Ingest book content in bulk and create embeddings
        """
        try:
            from src.services.retrieval_service import RetrievalService
            retrieval_service = RetrievalService()

            for item in book_data:
                # Create embedding for the content using Gemini
                content_text = item.get("content", "")
                if not content_text.strip():
                    continue  # Skip empty content

                try:
                    embedding = await retrieval_service.create_embedding(content_text)
                except Exception as e:
                    logger.warning(f"Failed to create embedding for content '{item.get('title', '')}': {str(e)}")
                    embedding = [0.0] * 768  # Use zero vector as fallback

                content_create = BookContentCreate(
                    title=item.get("title", ""),
                    content=item.get("content", ""),
                    chunk_text=item.get("chunk_text", item.get("content", "")),
                    metadata=item.get("metadata", {}),
                    embedding_vector=embedding,
                    relations=item.get("relations", [])
                )

                await self.create_content(content_create)

            return True
        except Exception as e:
            logger.error(f"Failed to ingest book content: {str(e)}")
            return False

    async def index_content_chunks(self, content_id: str, chunks: List[str]) -> bool:
        """
        Create and index content chunks for retrieval
        """
        try:
            # This would be used to break down large content into smaller chunks for better retrieval
            for i, chunk_text in enumerate(chunks):
                # Create embedding for the chunk
                # Placeholder implementation
                embedding = [0.0] * 768  # Placeholder embedding

                chunk_content = BookContentCreate(
                    title=f"Chunk {i} of {content_id}",
                    content=chunk_text,
                    chunk_text=chunk_text,
                    metadata={"parent_id": content_id, "chunk_index": i},
                    embedding_vector=embedding,
                    relations=[content_id]
                )

                await self.create_content(chunk_content)

            return True
        except Exception as e:
            logger.error(f"Failed to index content chunks for {content_id}: {str(e)}")
            return False