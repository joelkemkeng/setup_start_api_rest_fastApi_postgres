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
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")  # Clé par défaut modifiée
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

    # Configuration de l'API
    API_V1_STR: str = "/api/v1"
    SERVER_HOST: str = os.getenv("SERVER_HOST", "http://localhost")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))
    
    # URL de base pour les fichiers statiques
    @property
    def BASE_URL(self) -> str:
        return f"{self.SERVER_HOST}:{self.SERVER_PORT}"

    class Config:
        case_sensitive = True


# Instance des paramètres
settings = Settings()