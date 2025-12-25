from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import chat, content
from src.core.config import settings
from src.core.security import rate_limit_middleware

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Add CORS middleware
allowed_origins = settings.BACKEND_CORS_ORIGINS or [settings.FRONTEND_ORIGIN] if settings.FRONTEND_ORIGIN else ["*"]
# Add Hugging Face Spaces origin for deployment
allowed_origins.extend([
    "https://*.hf.space",
    "https://huggingface.co",
    "https://*.huggingface.co"
])
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting middleware
app.middleware("http")(rate_limit_middleware)

# Include API routes
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(content.router, prefix="/api/content", tags=["content"])

@app.get("/")
def read_root():
    return {"message": "AI-Powered Book Assistant API", "version": settings.VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)