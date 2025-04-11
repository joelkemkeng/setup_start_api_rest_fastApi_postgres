from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

from app.schemas.common import SuccessResponse, ErrorResponse

# Schéma pour la réponse de connexion
class TokenPayload(BaseModel):
    """Schéma pour le contenu du token JWT."""
    sub: str = Field(..., description="ID de l'utilisateur")
    exp: datetime = Field(..., description="Date d'expiration du token")
    iat: datetime = Field(..., description="Date de création du token")
    type: str = Field(..., description="Type de token")

# Schéma pour le token
class Token(BaseModel):
    """Schéma pour le token d'accès JWT."""
    access_token: str = Field(..., description="Token d'accès JWT")
    token_type: str = Field(..., description="Type de token", example="bearer")

# Type None pour représenter aucune métadonnée
class NoMetadata(BaseModel):
    pass

# Réponse pour l'authentification
class AuthResponse(SuccessResponse[Token, None]):
    """Réponse standardisée pour l'authentification."""
    code: int = 200
    message: str = "Authentification réussie"

# Erreur d'authentification
class AuthError(ErrorResponse[None, None]):
    """Réponse d'erreur standardisée pour l'authentification."""
    code: int = 401
    message: str = "Échec de l'authentification"

# Schéma pour la déconnexion
class LogoutResponse(SuccessResponse[None, None]):
    """Réponse standardisée pour la déconnexion."""
    code: int = 200
    message: str = "Déconnexion réussie"