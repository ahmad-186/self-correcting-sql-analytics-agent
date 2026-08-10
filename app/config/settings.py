from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    app_name: str = "AI SSQL ANalytics Agent"
    app_env: str  = "development"
    debug: bool = True

    # Database
    database_url: str
    # LLM
    mistral_api_key: str
    llm_model: str = "mistral-small-2506"

    # Agent
    max_retries: int = 3

    # Logging
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    """
    Create the Settings object once and reuse it throughout the application's lifetime.
    """

    return Settings()

settings = get_settings()