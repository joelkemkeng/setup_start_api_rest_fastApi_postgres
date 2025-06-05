from fastapi.testclient import TestClient
from pathlib import Path
import sys

# Ajoute le dossier contenant le code de l'application au PYTHONPATH pour les tests
# On ajoute le dossier "backend" afin que le package "app" soit importable
sys.path.append(str(Path(__file__).resolve().parents[3]))

from app.main import app

client = TestClient(app)

def test_register_user():
    """Test l'inscription d'un utilisateur avec des données valides"""
    response = client.post(
        "/api/v1/users/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "TestPassword123!"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["code"] == 201
    assert data["message"] == "Utilisateur créé avec succès"
    assert "user_id" in data["data"]
