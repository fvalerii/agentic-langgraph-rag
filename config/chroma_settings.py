from pydantic import BaseModel

class ChromaSettings(BaseModel):
    DB_PATH: str = "./chroma_db"
    COLLECTION_NAME: str = "documents"