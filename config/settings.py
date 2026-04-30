from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field
from typing import List
from .constants import MAX_FILE_SIZE, MAX_TOTAL_SIZE, ALLOWED_TYPES

class Settings(BaseSettings):
    # Application settings
    MAX_FILE_SIZE: int = Field(default=MAX_FILE_SIZE)
    MAX_TOTAL_SIZE: int = Field(default=MAX_TOTAL_SIZE)
    ALLOWED_TYPES: List[str] = Field(default_factory=lambda: ALLOWED_TYPES)

    # Database settings
    CHROMA_DB_PATH: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "documents"

    # Retrieval settings
    VECTOR_SEARCH_K: int = 10
    HYBRID_RETRIEVER_WEIGHTS: List[float] = Field(default_factory=lambda: [0.4, 0.6])

    # Logging settings
    LOG_LEVEL: str = "INFO"

    # Cache settings
    CACHE_DIR: str = "document_cache"
    CACHE_EXPIRE_DAYS: int = 7

    # Pydantic v2 configuration
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",          # ignore unknown env vars
        validate_default=True,   # validate default values
        frozen=False             # allow mutation if needed
    )

settings = Settings()