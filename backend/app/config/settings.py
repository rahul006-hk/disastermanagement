import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Disaster Relief AI Resource Planner"
    API_V1_STR: str = "/api"
    
    # DB URL - Primary Postgres, fallback SQLite for lightweight local dev/testing
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./disaster_relief.db")
    
    class Config:
        env_file = ".env"

settings = Settings()
