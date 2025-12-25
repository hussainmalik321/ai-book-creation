"""
Security utilities for the AI-Powered Book Assistant
"""
from fastapi import Request, HTTPException
from typing import Optional
import time
import hashlib
from collections import defaultdict
from src.core.config import settings


class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 3600):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if the identifier is allowed to make a request
        """
        current_time = time.time()

        # Clean old requests outside the window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if current_time - req_time < self.window_seconds
        ]

        # Check if under limit
        if len(self.requests[identifier]) < self.max_requests:
            self.requests[identifier].append(current_time)
            return True

        return False


# Global rate limiter instance
rate_limiter = RateLimiter()


def get_client_identifier(request: Request) -> str:
    """
    Get a unique identifier for the client for rate limiting
    """
    # Try to get from X-Forwarded-For header first (for when behind proxy)
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        # Take the first IP from the list
        client_ip = forwarded.split(",")[0].strip()
    else:
        client_ip = request.client.host

    # Also consider user-agent for more granular rate limiting
    user_agent = request.headers.get("user-agent", "")
    identifier = f"{client_ip}:{hashlib.md5(user_agent.encode()).hexdigest()[:8]}"

    return identifier


def check_rate_limit(request: Request) -> bool:
    """
    Check if the request is within rate limits
    """
    identifier = get_client_identifier(request)
    return rate_limiter.is_allowed(identifier)


async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware to enforce rate limiting
    """
    if not check_rate_limit(request):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )

    response = await call_next(request)
    return response


def validate_content_length(content: str, max_length: int = 10000) -> bool:
    """
    Validate content length to prevent oversized payloads
    """
    return len(content) <= max_length


def sanitize_input(text: str) -> str:
    """
    Basic input sanitization
    """
    # Remove null bytes and other potentially harmful characters
    sanitized = text.replace('\x00', '').strip()
    return sanitized