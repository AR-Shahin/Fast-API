import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()
class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATABASE_URL: str = f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
    DATABASE_URL_MYSQL :str = "mysql://root:password@localhost:3306/fast_common?charset=utf8mb4"
    # "mysql://root:password@localhost:3306/fast_common?charset=utf8mb4"
    class Config:
        env_file = ".env"

settings = Settings()