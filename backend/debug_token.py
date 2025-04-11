import jwt
from datetime import datetime, timedelta
import uuid

# Configuration
SECRET_KEY = "supersecretkey"  # Clé principale
ALTERNATIVE_KEYS = ["hetic"]   # Clés alternatives

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Fonction pour créer un token avec une clé spécifique
def create_test_token(key = SECRET_KEY):
    # Créer l'ID utilisateur (pour test)
    user_id = str(uuid.uuid4())
    
    # Définir la date d'expiration
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Créer le payload du token
    payload = {
        "sub": user_id,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access_token"
    }
    
    # Encoder le token
    token = jwt.encode(payload, key, algorithm=ALGORITHM)
    
    print(f"User ID: {user_id}")
    print(f"Token: {token}")
    print(f"Clé utilisée: {key}")
    
    return token, user_id

# Fonction pour décoder un token
def decode_test_token(token):
    # Essayer avec la clé principale
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Décodage réussi avec la clé principale")
        
        # Extraire les informations
        user_id = payload.get("sub")
        exp = payload.get("exp")
        iat = payload.get("iat")
        token_type = payload.get("type")
        
        # Afficher les informations
        print(f"- User ID: {user_id}")
        print(f"- Expiration: {datetime.fromtimestamp(exp)}")
        print(f"- Création: {datetime.fromtimestamp(iat)}")
        print(f"- Type: {token_type}")
        
        return payload
    
    except jwt.ExpiredSignatureError:
        print("Erreur avec la clé principale: Token expiré")
    except jwt.InvalidTokenError:
        print("Erreur avec la clé principale: Token invalide")
    except Exception as e:
        print(f"Erreur avec la clé principale: {str(e)}")
    
    # Si ça échoue, essayer avec les clés alternatives
    for i, alt_key in enumerate(ALTERNATIVE_KEYS):
        try:
            payload = jwt.decode(token, alt_key, algorithms=[ALGORITHM])
            print(f"Décodage réussi avec la clé alternative {i+1}")
            
            # Extraire les informations
            user_id = payload.get("sub")
            exp = payload.get("exp")
            iat = payload.get("iat")
            token_type = payload.get("type")
            
            # Afficher les informations
            print(f"- User ID: {user_id}")
            print(f"- Expiration: {datetime.fromtimestamp(exp)}")
            print(f"- Création: {datetime.fromtimestamp(iat)}")
            print(f"- Type: {token_type}")
            
            return payload
        
        except jwt.ExpiredSignatureError:
            print(f"Erreur avec la clé alternative {i+1}: Token expiré")
        except jwt.InvalidTokenError:
            print(f"Erreur avec la clé alternative {i+1}: Token invalide")
        except Exception as e:
            print(f"Erreur avec la clé alternative {i+1}: {str(e)}")
    
    print("Échec de décodage avec toutes les clés")
    return None

# Génération d'un nouveau token avec la clé principale
print("=== Génération d'un nouveau token avec la clé principale ===")
new_token, user_id = create_test_token()

# Génération d'un nouveau token avec la clé alternative
print("\n=== Génération d'un nouveau token avec la clé alternative ===")
alt_token, alt_user_id = create_test_token(ALTERNATIVE_KEYS[0])

# Décodage du token généré avec la clé principale
print("\n=== Décodage du token généré avec la clé principale ===")
decode_test_token(new_token)

# Décodage du token généré avec la clé alternative
print("\n=== Décodage du token généré avec la clé alternative ===")
decode_test_token(alt_token)

# Décodage du token fourni par l'utilisateur
user_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4M2U4OWRjNC1iNDBkLTQwODMtYTBiMi0xZTU3YmM1NmMwMzIiLCJleHAiOjE3MTI4NzcwNDMsImlhdCI6MTcxMjg3NzAzNywidHlwZSI6ImFjY2Vzc190b2tlbiJ9.A-K9T5nF1nSVnHdlXWR9N_KjmB_6_-i42Xj4aXgz0xE"
print("\n=== Décodage du token fourni ===")
decode_test_token(user_token)