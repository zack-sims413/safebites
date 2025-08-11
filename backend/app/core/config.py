from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/safebites"
    POSTGIS_ENABLED: bool = True
    
    # API Keys
    YELP_API_KEY: Optional[str] = None
    OPENCAGE_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    
    # Cache
    CACHE_TTL_SECONDS: int = 86400  # 24 hours
    REDIS_URL: str = "redis://localhost:6379"
    
    # Application
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "your-secret-key-change-this"
    
    # Rate Limiting
    YELP_RATE_LIMIT: int = 5000
    OPENCAGE_RATE_LIMIT: int = 2500
    
    # Mock Mode
    MOCK_MODE_ENABLED: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create global settings instance
settings = Settings() 