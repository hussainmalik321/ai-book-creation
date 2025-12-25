"""
Chat Session model for the AI-Powered Book Assistant
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatSessionBase(BaseModel):
    user_id: Optional[str] = None  # optional, for tracking if needed


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionUpdate(BaseModel):
    user_id: Optional[str] = None
    active: Optional[bool] = None


class ChatSession(ChatSessionBase):
    id: str
    start_time: datetime
    last_activity: datetime
    active: bool

    class Config:
        from_attributes = True