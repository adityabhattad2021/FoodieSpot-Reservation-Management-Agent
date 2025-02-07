from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_BASE_URL: str 
    GROQ_API_KEY: str
    DEFAULT_MODEL: str 
    BACKEND_API_KEY: str
    

settings = Settings()