# Hugging Face Spaces entry point
import os
from backend.main import app

# This allows Hugging Face to run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )