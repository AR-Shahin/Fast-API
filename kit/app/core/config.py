import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Project"
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATABASE_URL: str = f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"

    class Config:
        env_file = ".env"

settings = Settings()