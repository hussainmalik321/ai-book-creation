"""
API dependencies for the AI-Powered Book Assistant
"""
from fastapi import Depends, HTTPException, status
from typing import Generator
from src.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession


def get_session() -> Generator[AsyncSession, None, None]:
    """
    Get database session dependency
    """
    session_gen = get_db()
    session = next(session_gen)
    try:
        yield session
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database session error: {str(e)}"
        )
    finally:
        session.close()