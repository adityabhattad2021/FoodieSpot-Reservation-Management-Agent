import os
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

class Settings(BaseSettings):
    API_BASE_URL: str = "http://localhost:8000"
    GROQ_API_KEY: str
    DEFAULT_MODEL: str = "llama-3.1-8b-instant"
    
    model_config = SettingsConfigDict(env_file=DOTENV)

settings = Settings()