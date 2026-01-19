from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    OPENAI_API_KEY: Optional[str] = None
    MAX_UPLOAD_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: list = [".csv"]
    
    class Config:
        env_file = ".env"

settings = Settings()
