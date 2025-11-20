import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings"""
    app_name: str = "Observe Insurance Claims API"
    app_version: str = "1.0.0"
    
    # Firestore
    google_application_credentials: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    
    # CORS
    cors_origins: List[str] = ["*"]
    
    class Config:
        env_file = ".env"


settings = Settings()
