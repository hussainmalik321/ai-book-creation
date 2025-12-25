"""
User Query model for the AI-Powered Book Assistant
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class QueryType(str, Enum):
    GLOBAL_QA = "GLOBAL_QA"
    SELECTION_QA = "SELECTION_QA"


class UserQueryBase(BaseModel):
    query_text: str
    query_type: QueryType
    selected_text: Optional[str] = None
    book_content_ids: Optional[List[str]] = []  # referenced content for selection mode
    session_id: Optional[str] = None  # for conversation context


class UserQueryCreate(UserQueryBase):
    pass


class UserQueryUpdate(BaseModel):
    query_text: Optional[str] = None
    selected_text: Optional[str] = None
    book_content_ids: Optional[List[str]] = None
    session_id: Optional[str] = None


class UserQuery(UserQueryBase):
    id: str
    timestamp: datetime

    class Config:
        from_attributes = True