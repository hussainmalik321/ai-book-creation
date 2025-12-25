"""
Custom exceptions for the AI-Powered Book Assistant
"""


class BookAssistantException(Exception):
    """Base exception for the book assistant"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ContentNotFoundException(BookAssistantException):
    """Raised when requested content is not found"""
    def __init__(self, message: str = "Content not found"):
        super().__init__(message, 404)


class QueryProcessingException(BookAssistantException):
    """Raised when query processing fails"""
    def __init__(self, message: str = "Query processing failed"):
        super().__init__(message, 500)


class InvalidQueryException(BookAssistantException):
    """Raised when query is invalid"""
    def __init__(self, message: str = "Invalid query"):
        super().__init__(message, 400)


class ContentRestrictionException(BookAssistantException):
    """Raised when content restriction rules are violated"""
    def __init__(self, message: str = "Content restriction violation"):
        super().__init__(message, 400)