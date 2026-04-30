from pydantic import BaseModel, Field
from typing import List

class RetrievalSettings(BaseModel):
    VECTOR_SEARCH_K: int = 10
    HYBRID_RETRIEVER_WEIGHTS: List[float] = Field(default_factory=lambda: [0.4, 0.6])