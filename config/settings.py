from pydantic_settings import BaseSettings
from pydantic import ConfigDict

from .watsonx_settings import WatsonxSettings
from .chroma_settings import ChromaSettings
from .cache_settings import CacheSettings
from .retrieval_settings import RetrievalSettings
from .app_settings import AppSettings
from .logging_settings import LoggingSettings

class Settings(BaseSettings):
    WATSONX: WatsonxSettings
    CHROMA: ChromaSettings
    CACHE: CacheSettings
    RETRIEVAL: RetrievalSettings
    APP: AppSettings
    LOGGING: LoggingSettings

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        validate_default=True,
        frozen=False,
        env_nested_delimiter="__"
    )

settings = Settings()