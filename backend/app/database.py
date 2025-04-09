
"""
# Configuration de la connexion à la base de données
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import Base

# Utiliser une URL de connexion depuis la configuration
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db/mobile_musician"

#SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@db:5432/mobile_musician"


# Création du moteur SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Fabrique de sessions de base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
   
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Déclaration de Base ici
Base = declarative_base()  # Remplace 'Base = Base' par cette déclaration

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db/mobile_musician"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
