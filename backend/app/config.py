from typing import List
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Charger les variables d'environnement
load_dotenv()


class Settings(BaseSettings):
    # Configuration de la base de données
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@db/mobile_musician"
    )

    # Configuration JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secure_secret_key_here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "4320")
    )

    # Configuration CORS
    BACKEND_CORS_ORIGINS: List[str] = eval(
        os.getenv(
            "BACKEND_CORS_ORIGINS",
            '["http://localhost:3000","http://localhost:8080","http://localhost:19006"]',
        )
    )

    # Configuration de l'environnement
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    class Config:
        case_sensitive = True


# Instance des paramètres
settings = Settings()
