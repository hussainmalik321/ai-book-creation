"""
Response model for the AI-Powered Book Assistant
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SourceChunk(BaseModel):
    content_id: str
    title: str
    text: str


class ResponseBase(BaseModel):
    query_id: str
    response_text: str
    source_chunks: List[SourceChunk]  # content IDs used to generate response
    confidence_score: Optional[float] = None  # confidence level of response
    is_fallback: Optional[bool] = False  # true if response indicates lack of knowledge


class ResponseCreate(ResponseBase):
    pass


class ResponseUpdate(BaseModel):
    response_text: Optional[str] = None
    source_chunks: Optional[List[SourceChunk]] = None
    confidence_score: Optional[float] = None
    is_fallback: Optional[bool] = None


class Response(ResponseBase):
    id: str
    timestamp: datetime

    class Config:
        from_attributes = True