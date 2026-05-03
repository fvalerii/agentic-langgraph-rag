from pydantic import BaseModel

class CacheSettings(BaseModel):
    CACHE_DIR: str = "document_cache"
    CACHE_EXPIRE_DAYS: int = 7