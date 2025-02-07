
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str 
    SECRET_KEY:str 
    BACKEND_API_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ADMIN_USERNAME: str 
    ADMIN_PASSWORD: str
    ALGORITHM: str 



settings = Settings()