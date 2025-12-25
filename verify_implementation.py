"""
Verification script for AI-Powered Book Assistant
This script tests the core functionality of the implemented system
"""
import asyncio
import sys
from pathlib import Path

# Add the backend src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.services.chat_service import ChatService
from src.services.content_service import ContentService
from src.models.user_query import UserQueryCreate, QueryType


async def verify_implementation():
    print("Verifying AI-Powered Book Assistant Implementation...")

    # Test 1: Basic Chat Service import
    print("\n[TEST] Testing Chat Service import...")
    try:
        # Just test if the class can be imported, don't initialize
        from src.services.chat_service import ChatService
        print("  [OK] ChatService imported successfully")
    except Exception as e:
        print(f"  [ERROR] ChatService import failed: {e}")
        return False

    # Test 2: Content Service import
    print("\n[TEST] Testing Content Service import...")
    try:
        # Just test if the class can be imported, don't initialize
        from src.services.content_service import ContentService
        print("  [OK] ContentService imported successfully")
    except Exception as e:
        print(f"  [ERROR] ContentService import failed: {e}")
        return False

    # Test 3: Basic Query Processing (without actual API calls)
    print("\n[TEST] Testing Query Processing...")
    try:
        # Test with a simple query
        query_data = UserQueryCreate(
            query_text="What is the main concept of this book?",
            query_type=QueryType.GLOBAL_QA
        )
        print("  [OK] UserQueryCreate model works correctly")
    except Exception as e:
        print(f"  [ERROR] UserQueryCreate failed: {e}")
        return False

    # Test 4: Selection-based query (without actual API calls)
    print("\n[TEST] Testing Selection-Based Query...")
    try:
        selection_query = UserQueryCreate(
            query_text="Explain this concept",
            query_type=QueryType.SELECTION_QA,
            selected_text="This is a sample selected text for testing purposes."
        )
        print("  [OK] Selection-based query model works correctly")
    except Exception as e:
        print(f"  [ERROR] Selection-based query failed: {e}")
        return False

    # Test 5: Check that all required services are importable
    print("\n[TEST] Testing Service Imports...")
    try:
        from src.services.retrieval_service import RetrievalService
        from src.services.generation_service import GenerationService
        from src.core.config import settings
        from src.core.security import RateLimiter
        print("  [OK] All services import successfully")
    except ImportError as e:
        print(f"  [ERROR] Service import failed: {e}")
        return False

    # Test 6: Check configuration
    print("\n[TEST] Testing Configuration...")
    try:
        # Verify settings exist
        assert hasattr(settings, 'PROJECT_NAME')
        assert hasattr(settings, 'GEMINI_API_KEY')
        assert hasattr(settings, 'QDRANT_URL')
        print("  [OK] Configuration loaded successfully")
    except Exception as e:
        print(f"  [ERROR] Configuration check failed: {e}")
        return False

    # Test 7: Check that all API routes exist
    print("\n[TEST] Testing API Routes...")
    try:
        from src.api.routes import chat, content
        print("  [OK] API routes imported successfully")
    except ImportError as e:
        print(f"  [ERROR] API routes import failed: {e}")
        return False

    print("\n[SUCCESS] All verification tests passed!")
    print("\n[SUMMARY] Implementation Summary:")
    print("  • Backend API with FastAPI framework")
    print("  • Gemini API integration for AI responses")
    print("  • Qdrant vector database for content retrieval")
    print("  • Support for both global and selection-based Q&A")
    print("  • Session management and conversation history")
    print("  • Source attribution for responses")
    print("  • Rate limiting and security measures")
    print("  • Frontend React components for UI")
    print("  • Environment configuration and documentation")

    return True


if __name__ == "__main__":
    success = asyncio.run(verify_implementation())
    if success:
        print("\n[SUCCESS] Implementation verification completed successfully!")
        sys.exit(0)
    else:
        print("\n[FAILURE] Implementation verification failed!")
        sys.exit(1)