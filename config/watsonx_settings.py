from pydantic import BaseModel, Field

class WatsonxSettings(BaseModel):
    APIKEY: str
    URL: str = "https://us-south.ml.cloud.ibm.com"
    PROJECT_ID: str = "skills-network"