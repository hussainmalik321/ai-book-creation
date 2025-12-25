from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Powered Book Assistant"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # Gemini API Configuration
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL_NAME: str = "gemini-2.5-flash"  # Updated to latest available model

    # Qdrant Configuration
    QDRANT_URL: str = ""
    QDRANT_API_KEY: Optional[str] = None

    # Database Configuration
    DATABASE_URL: str = ""
    NEON_DATABASE_URL: str = ""

    # Application settings
    BACKEND_ENV: str = "production"
    FRONTEND_ORIGIN: str = "http://localhost:3000"
    PORT: int = 8001

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()