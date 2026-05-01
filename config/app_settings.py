from pydantic import BaseModel, Field
from typing import List

MAX_FILE_SIZE = 50 * 1024 * 1024
MAX_TOTAL_SIZE = 200 * 1024 * 1024
ALLOWED_TYPES = [".pdf", ".docx", ".txt", ".md"]

class AppSettings(BaseModel):
    MAX_FILE_SIZE: int = Field(default=MAX_FILE_SIZE)
    MAX_TOTAL_SIZE: int = Field(default=MAX_TOTAL_SIZE)
    ALLOWED_TYPES: List[str] = Field(default_factory=lambda: list(ALLOWED_TYPES))