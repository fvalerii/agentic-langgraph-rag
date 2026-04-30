from pydantic import BaseModel

class LoggingSettings(BaseModel):
    LEVEL: str = "INFO"