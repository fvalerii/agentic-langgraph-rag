from pydantic import BaseModel, Field
from typing import List
from .constants import MAX_FILE_SIZE, MAX_TOTAL_SIZE, ALLOWED_TYPES

class AppSettings(BaseModel):
    MAX_FILE_SIZE: int = Field(default=MAX_FILE_SIZE)
    MAX_TOTAL_SIZE: int = Field(default=MAX_TOTAL_SIZE)
    ALLOWED_TYPES: List[str] = Field(default_factory=lambda: list(ALLOWED_TYPES))