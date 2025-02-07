import os
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/foodiespot_db"
    SECRET_KEY:str 
    BACKEND_API_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ADMIN_USERNAME: str 
    ADMIN_PASSWORD: str
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=DOTENV)

settings = Settings()