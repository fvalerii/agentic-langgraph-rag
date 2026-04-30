from pydantic import BaseModel

class CacheSettings(BaseModel):
    DIR: str = "document_cache"
    EXPIRE_DAYS: int = 7