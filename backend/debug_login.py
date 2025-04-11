import requests
import json
import os

base_url = "http://localhost:8000"

def login_user():
    """Obtention d'un token avec les identifiants de l'utilisateur existant"""
    login_url = f"{base_url}/api/v1/auth/login"
    
    # Identifiants de l'utilisateur
    credentials = {
        "email": "user@example.com",
        "password": "Password123!"
    }
    
    # Effectuer la requête
    response = requests.post(login_url, json=credentials)
    
    # Vérifier si la connexion a réussi
    if response.status_code == 200:
        print("Connexion réussie!")
        print(f"Status code: {response.status_code}")
        
        # Afficher la réponse
        data = response.json()
        print(json.dumps(data, indent=2))
        
        # Extraire le token
        token = data.get("data", {}).get("access_token")
        print(f"\nToken obtenu: {token}")
        
        return token
    else:
        print(f"Échec de la connexion. Status code: {response.status_code}")
        print(response.text)
        return None

def test_protected_endpoint(token):
    """Test d'un endpoint protégé avec le token"""
    if not token:
        print("Pas de token disponible.")
        return
    
    # URL de l'endpoint protégé
    me_url = f"{base_url}/api/v1/users/me"
    
    # Headers avec le token Bearer
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Effectuer la requête
    response = requests.get(me_url, headers=headers)
    
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        print("\nAccès à l'endpoint protégé réussi!")
        print(f"Status code: {response.status_code}")
        
        # Afficher la réponse
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        print(f"\nÉchec de l'accès à l'endpoint protégé. Status code: {response.status_code}")
        print(response.text)

# Exécution du test
if __name__ == "__main__":
    print("=== Test de connexion et d'accès à un endpoint protégé ===\n")
    token = login_user()
    if token:
        test_protected_endpoint(token)