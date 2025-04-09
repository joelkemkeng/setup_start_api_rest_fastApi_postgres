from fastapi.testclient import TestClient
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
    assert "user_id" in data
    assert "message" in data
    assert data["message"] == "Utilisateur créé avec succès"