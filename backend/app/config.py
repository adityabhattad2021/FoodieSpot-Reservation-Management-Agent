from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/foodiespot_db"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()