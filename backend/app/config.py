import os
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/foodiespot_db"

    model_config = SettingsConfigDict(env_file=DOTENV)

settings = Settings()