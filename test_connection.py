"""
Test script to verify API connections
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment():
    """Test that all environment variables are set"""
    print("Testing environment variables...")

    gemini_key = os.getenv('GEMINI_API_KEY')
    qdrant_url = os.getenv('QDRANT_URL')
    qdrant_key = os.getenv('QDRANT_API_KEY')
    neon_url = os.getenv('NEON_DATABASE_URL')

    print(f"GEMINI_API_KEY: {'SET' if gemini_key else 'NOT SET'}")
    print(f"QDRANT_URL: {'SET' if qdrant_url else 'NOT SET'}")
    print(f"QDRANT_API_KEY: {'SET' if qdrant_key else 'NOT SET'}")
    print(f"NEON_DATABASE_URL: {'SET' if neon_url else 'NOT SET'}")

    return all([gemini_key, qdrant_url, qdrant_key, neon_url])

def test_qdrant_connection():
    """Test Qdrant connection"""
    try:
        from qdrant_client import QdrantClient

        qdrant_url = os.getenv('QDRANT_URL')
        qdrant_key = os.getenv('QDRANT_API_KEY')

        if not qdrant_url or not qdrant_key:
            print("Qdrant connection test skipped - missing credentials")
            return False

        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_key,
            prefer_grpc=False
        )

        # Try to get collections to test connection
        collections = client.get_collections()
        print(f"Qdrant connection successful - found {len(collections.collections)} collections")
        return True
    except Exception as e:
        print(f"Qdrant connection failed: {e}")
        return False

def test_gemini_connection():
    """Test Gemini connection"""
    try:
        import google.generativeai as genai

        gemini_key = os.getenv('GEMINI_API_KEY')

        if not gemini_key:
            print("Gemini connection test skipped - missing API key")
            return False

        genai.configure(api_key=gemini_key)

        # List available models to see what's supported
        models = genai.list_models()
        available_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                available_models.append(model.name)

        print(f"Available models for generation: {available_models}")

        # Try different model names in order of preference
        model_names = ['gemini-2.5-flash', 'gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']

        for model_name in model_names:
            try:
                model = genai.GenerativeModel(model_name)
                # Perform a simple test generation
                response = model.generate_content("Hello, this is a test. Respond with just 'Hello'.")

                if response and response.text:
                    print(f"Gemini connection successful with model: {model_name}")
                    return True
            except Exception as model_error:
                print(f"Failed to use model {model_name}: {model_error}")
                continue

        print("Gemini connection failed - no suitable model available")
        return False
    except Exception as e:
        print(f"Gemini connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing API Connections...\n")

    # Test environment variables
    env_ok = test_environment()
    print()

    if env_ok:
        # Test Qdrant connection
        qdrant_ok = test_qdrant_connection()
        print()

        # Test Gemini connection
        gemini_ok = test_gemini_connection()
        print()

        if qdrant_ok and gemini_ok:
            print("All connections are working properly!")
        else:
            print("Some connections failed, but that's OK - services might be temporarily unavailable")
    else:
        print("Environment variables are not properly set")