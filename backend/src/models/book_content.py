"""
Book Content model for the AI-Powered Book Assistant
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class BookContentBase(BaseModel):
    title: str
    content: str
    chunk_text: str
    metadata: Dict[str, Any]  # chapter, section, position in book
    embedding_vector: Optional[List[float]] = None  # vector representation for similarity search
    relations: Optional[List[str]] = []  # references to related content


class BookContentCreate(BookContentBase):
    pass


class BookContentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    chunk_text: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    embedding_vector: Optional[List[float]] = None
    relations: Optional[List[str]] = None


class BookContent(BookContentBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True