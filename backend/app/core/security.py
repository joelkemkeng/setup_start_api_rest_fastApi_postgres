from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union, List
from uuid import UUID

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db

# Configuration de l'algorithme de hachage
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuration du schéma OAuth2 pour l'authentification
# Définir le schema OAuth2 avec l'URL de token et auto_error=False pour permettre aux endpoints publics
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# L'ancien OAuth2PasswordBearer ne fonctionne pas correctement avec Swagger
# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="/api/v1/auth/login-form",
#     scheme_name="Bearer Authentication",
#     description="Entrez le token JWT obtenu lors de la connexion"
# )

# Utiliser OAuth2PasswordBearer pour la meilleure intégration avec Swagger UI
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    scheme_name="Bearer Authentication",
    description="Entrez le token JWT obtenu lors de la connexion"
)

# Liste des clés secrètes alternatives pour la transition
ALTERNATIVE_KEYS = ["hetic"]

def get_password_hash(password: str) -> str:
    """
    Génère un hash sécurisé pour un mot de passe en utilisant l'algorithme bcrypt.
    
    Args:
        password: Mot de passe en clair
    
    Returns:
        str: Mot de passe haché sécurisé
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si un mot de passe en clair correspond au hash stocké.
    
    Args:
        plain_password: Mot de passe en clair fourni par l'utilisateur
        hashed_password: Hash du mot de passe stocké en base de données
    
    Returns:
        bool: True si le mot de passe correspond, False sinon
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Crée un token JWT avec une durée de vie spécifiée.
    
    Args:
        data: Données à encoder dans le token (typiquement l'identifiant de l'utilisateur)
        expires_delta: Durée de validité du token (par défaut: paramètre de configuration)
    
    Returns:
        str: Token JWT généré
    """
    to_encode = data.copy()
    
    # Définir la date d'expiration
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Ajouter les claims standards et personnalisés
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access_token"
    })
    
    # Encoder le token avec la clé secrète
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_token_from_header(request: Request) -> Optional[str]:
    """
    Extrait le token JWT de l'en-tête Authorization.
    
    Args:
        request: Requête HTTP
    
    Returns:
        Optional[str]: Token JWT extrait ou None si l'en-tête est absent ou mal formé
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    
    parts = auth_header.split()
    if parts[0].lower() != "bearer":
        return None
    if len(parts) == 1:
        return None
    if len(parts) > 2:
        return None
    
    return parts[1]

def decode_token(token: str) -> Dict[str, Any]:
    """
    Décode un token JWT et retourne les informations qu'il contient.
    Essaie d'abord avec la clé principale, puis avec les clés alternatives.
    
    Args:
        token: Token JWT à décoder
    
    Returns:
        Dict[str, Any]: Contenu du token
    
    Raises:
        HTTPException: Si le token est invalide ou expiré
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token d'authentification invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # D'abord, essayer avec la clé principale
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except (JWTError, ValidationError):
        # Si ça échoue, essayer avec les clés alternatives
        for alt_key in ALTERNATIVE_KEYS:
            try:
                payload = jwt.decode(
                    token, alt_key, algorithms=[settings.ALGORITHM]
                )
                # Si une clé alternative fonctionne, retourner le payload
                return payload
            except (JWTError, ValidationError):
                # Continuer avec la prochaine clé
                continue
    
    # Si toutes les tentatives échouent, lever l'exception
    raise credentials_exception

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Décode le token JWT et récupère l'utilisateur correspondant en base de données.
    Cette fonction est utilisée comme dépendance dans les endpoints protégés.
    
    Args:
        token: Token JWT fourni dans l'en-tête Authorization
        db: Session de base de données
    
    Returns:
        User: Instance de l'utilisateur authentifié
    
    Raises:
        HTTPException: Si le token est invalide ou l'utilisateur n'existe pas
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token d'authentification invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Décoder le token (en essayant toutes les clés)
        payload = decode_token(token)
        
        # Extraire l'identifiant utilisateur
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        
        # Vérifier le type de token
        token_type: str = payload.get("type")
        if token_type != "access_token":
            raise credentials_exception
        
        # Tentative de récupération de l'utilisateur en base de données
        from app.models.user import User
        
        user = db.query(User).filter(User.id == user_id).first()
        
        if user is None:
            raise credentials_exception
            
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Compte utilisateur inactif",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Mettre à jour la date de dernière connexion
        user.last_login = datetime.utcnow()
        db.commit()
        
        # Retourner les informations de l'utilisateur
        return {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active
        }
            
    except (JWTError, ValidationError):
        raise credentials_exception