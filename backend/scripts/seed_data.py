#!/usr/bin/env python3
"""
Script de peuplement de la base de données avec des données de test
"""

import sys
import os
import uuid
from datetime import datetime

# Ajouter le répertoire parent au PATH pour pouvoir importer les modules de l'application
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal
from app.models.user import User, Instrument, Genre
from app.core.security import get_password_hash

def seed_data(force=True):
    db = SessionLocal()
    try:
        # Vérifier si des données existent déjà
        if not force and db.query(User).count() > 0 and db.query(Instrument).count() > 0 and db.query(Genre).count() > 0:
            print("La base de données contient déjà des données. Pas besoin de la peupler.")
            return
        
        # Si force=True ou si la base de données est vide
        print("Nettoyage des données existantes...")
        db.execute(text("DELETE FROM user_instrument"))
        db.execute(text("DELETE FROM user_genre"))
        db.execute(text("DELETE FROM users"))
        db.execute(text("DELETE FROM instruments"))
        db.execute(text("DELETE FROM genres"))
        db.commit()
        
        print("Ajout des données de test...")
        
        # Ajouter des instruments
        instruments = [
            Instrument(
                id=uuid.uuid4(),
                name="Guitare",
                category="Cordes",
                icon_url="https://example.com/icons/guitar.png"
            ),
            Instrument(
                id=uuid.uuid4(),
                name="Piano",
                category="Clavier",
                icon_url="https://example.com/icons/piano.png"
            ),
            Instrument(
                id=uuid.uuid4(),
                name="Batterie",
                category="Percussion",
                icon_url="https://example.com/icons/drums.png"
            ),
            Instrument(
                id=uuid.uuid4(),
                name="Violon",
                category="Cordes",
                icon_url="https://example.com/icons/violin.png"
            ),
            Instrument(
                id=uuid.uuid4(),
                name="Saxophone",
                category="Vent",
                icon_url="https://example.com/icons/saxophone.png"
            )
        ]
        
        for instrument in instruments:
            db.add(instrument)
        
        # Ajouter des genres musicaux
        genres = [
            Genre(
                id=uuid.uuid4(),
                name="Rock",
                description="Genre musical caractérisé par des sons électriques et un rythme marqué"
            ),
            Genre(
                id=uuid.uuid4(),
                name="Jazz",
                description="Genre musical né au début du XXe siècle aux États-Unis"
            ),
            Genre(
                id=uuid.uuid4(),
                name="Pop",
                description="Genre musical caractérisé par des mélodies accrocheuses et des structures simples"
            ),
            Genre(
                id=uuid.uuid4(),
                name="Classique",
                description="Musique savante occidentale, principalement du 17e au 19e siècle"
            ),
            Genre(
                id=uuid.uuid4(),
                name="Hip-Hop",
                description="Genre musical urbain développé à New York dans les années 1970"
            )
        ]
        
        for genre in genres:
            db.add(genre)
        
        # Ajouter des utilisateurs
        users = [
            User(
                id=uuid.uuid4(),
                username="musicien1",
                email="musicien1@example.com",
                password_hash=get_password_hash("Password123!"),
                profile_picture="https://example.com/profiles/1.jpg",
                biography="Guitariste passionné avec 10 ans d'expérience",
                latitude=48.8566,
                longitude=2.3522,
                created_at=datetime.utcnow(),
                is_active=True,
                last_login=datetime.utcnow()
            ),
            User(
                id=uuid.uuid4(),
                username="musicien2",
                email="musicien2@example.com",
                password_hash=get_password_hash("Password123!"),
                profile_picture="https://example.com/profiles/2.jpg",
                biography="Pianiste classique reconverti dans le jazz",
                latitude=45.7640,
                longitude=4.8357,
                created_at=datetime.utcnow(),
                is_active=True,
                last_login=datetime.utcnow()
            )
        ]
        
        for user in users:
            db.add(user)
        
        # Commiter les changements pour avoir les IDs
        db.commit()
        
        # Ajouter les associations avec SQL brut pour inclure skill_level
        for i, user in enumerate(users):
            # Associer des instruments avec skill_level
            skill_levels = ["Débutant", "Intermédiaire", "Avancé", "Expert"]
            
            for j in range(2):  # Ajouter 2 instruments par utilisateur
                instrument_idx = (i + j) % len(instruments)
                skill_level = skill_levels[(i + j) % len(skill_levels)]
                
                db.execute(
                    text("""
                    INSERT INTO user_instrument (user_id, instrument_id, skill_level)
                    VALUES (:user_id, :instrument_id, :skill_level)
                    """),
                    {
                        "user_id": str(user.id),
                        "instrument_id": str(instruments[instrument_idx].id),
                        "skill_level": skill_level
                    }
                )
            
            # Associer des genres
            for j in range(2):  # Ajouter 2 genres par utilisateur
                genre_idx = (i + j) % len(genres)
                
                db.execute(
                    text("""
                    INSERT INTO user_genre (user_id, genre_id)
                    VALUES (:user_id, :genre_id)
                    """),
                    {
                        "user_id": str(user.id),
                        "genre_id": str(genres[genre_idx].id)
                    }
                )
        
        # Commiter les associations
        db.commit()
        
        print("Données ajoutées avec succès :")
        print(f"- {len(instruments)} instruments")
        print(f"- {len(genres)} genres")
        print(f"- {len(users)} utilisateurs")
        
        # Afficher les IDs pour les tests
        print("\nInstruments IDs pour les tests :")
        for instrument in instruments:
            print(f"- {instrument.name}: {instrument.id}")
        
        print("\nGenres IDs pour les tests :")
        for genre in genres:
            print(f"- {genre.name}: {genre.id}")
            
    except Exception as e:
        db.rollback()
        print(f"Erreur lors de l'ajout des données : {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data(force=True)