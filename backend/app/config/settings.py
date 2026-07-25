from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional, Union
import os
from dotenv import load_dotenv
from pydantic_settings import SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    """Application settings with validation"""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")
    
    # Application
    APP_NAME: str = "FlytBase BDR System"
    DEBUG: bool = Field(default=False, env="DEBUG")
    ENVIRONMENT: str = Field(default="production", env="ENVIRONMENT")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    PORT: int = Field(default=8000, env="PORT")
    
    # Database
    MONGODB_URI: str = Field(..., env="MONGODB_URI")
    MONGODB_DB_NAME: str = Field(default="flytbase_bdr", env="MONGODB_DB_NAME")
    
    # Gemini API
    GEMINI_API_KEY: str = Field(..., env="GEMINI_API_KEY")
    GEMINI_MODEL: str = Field(default="gemini-1.5-pro", env="GEMINI_MODEL")
    GEMINI_EMBEDDING_MODEL: str = Field(default="models/embedding-001", env="GEMINI_EMBEDDING_MODEL")
    
    # CORS
    ALLOWED_ORIGINS: Union[List[str], str] = Field(
        default=["http://localhost:3000", "https://*.vercel.app"],
        env="ALLOWED_ORIGINS"
    )
    ALLOWED_HOSTS: Union[List[str], str] = Field(
        default=["*"],
        env="ALLOWED_HOSTS"
    )
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")
    
    # Redis (for Celery)
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    
    # External APIs
    LINKEDIN_API_KEY: Optional[str] = Field(None, env="LINKEDIN_API_KEY")
    CRUNCHBASE_API_KEY: Optional[str] = Field(None, env="CRUNCHBASE_API_KEY")
    NEWS_API_KEY: Optional[str] = Field(None, env="NEWS_API_KEY")
    
    # Email
    SENDGRID_API_KEY: Optional[str] = Field(None, env="SENDGRID_API_KEY")
    FROM_EMAIL: str = Field(default="bdr@flytbase.com", env="FROM_EMAIL")
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_allowed_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
settings = Settings()
