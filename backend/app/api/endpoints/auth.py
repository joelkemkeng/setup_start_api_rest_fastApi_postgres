from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any

from app.core.security import create_access_token, verify_password, get_current_user
from app.database import get_db
from app.schemas.auth import AuthResponse, AuthError, Token, LogoutResponse
from app.models.user import User
from app.config import settings
from app.core.exceptions import APIException

router = APIRouter()

@router.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Authentifier un utilisateur",
    description="""
    Authentifie un utilisateur avec son email et son mot de passe, et retourne un token JWT.
    
    **Exemples d'identifiants disponibles :**
    - Email: musicien1@example.com, Mot de passe: Password123!
    - Email: musicien2@example.com, Mot de passe: Password123!
    """,
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "multipart/form-data": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "email": {
                                "type": "string",
                                "description": "Adresse email de l'utilisateur",
                                "example": "musicien1@example.com",
                                "format": "email"
                            },
                            "password": {
                                "type": "string",
                                "description": "Mot de passe de l'utilisateur",
                                "example": "Password123!",
                                "format": "password"
                            }
                        },
                        "required": ["email", "password"]
                    },
                    "encoding": {
                        "email": {
                            "contentType": "text/plain"
                        },
                        "password": {
                            "contentType": "text/plain"
                        }
                    }
                }
            }
        }
    },
    responses={
        200: {
            "description": "Authentification réussie",
            "model": AuthResponse,
            "content": {
                "application/json": {
                    "example": {
                        "code": 200,
                        "message": "Authentification réussie",
                        "data": {
                            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "token_type": "bearer"
                        }
                    }
                }
            }
        },
        401: {
            "description": "Identifiants invalides",
            "model": AuthError,
            "content": {
                "application/json": {
                    "example": {
                        "code": 401,
                        "message": "Identifiants invalides",
                        "errors": [
                            {
                                "field": "credentials",
                                "message": "Email ou mot de passe incorrect"
                            }
                        ],
                        "status": "error"
                    }
                }
            }
        }
    }
)
async def login(
    email: str = Form(..., description="Adresse email de l'utilisateur", example="musicien1@example.com", media_type="multipart/form-data"),
    password: str = Form(..., description="Mot de passe de l'utilisateur", example="Password123!", media_type="multipart/form-data"),
    db: Session = Depends(get_db)
) -> AuthResponse:
    """
    Authentifie un utilisateur et génère un token JWT.

    - **email**: Email de l'utilisateur
    - **password**: Mot de passe de l'utilisateur

    Retourne un token JWT pour l'authentification.
    """
    # Chercher l'utilisateur par email
    user = db.query(User).filter(User.email == email).first()

    # Vérifier si l'utilisateur existe et si le mot de passe est correct
    if not user or not verify_password(password, user.password_hash):
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Identifiants incorrects",
            errors=[{
                "field": "credentials",
                "message": "Email ou mot de passe incorrect"
            }]
        )

    # Vérifier si l'utilisateur est actif
    if not user.is_active:
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Compte inactif",
            errors=[{
                "field": "account",
                "message": "Ce compte a été désactivé"
            }]
        )

    # Créer un token d'accès
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    # Retourner le token
    token_data = Token(
        access_token=access_token,
        token_type="bearer"
    )

    return AuthResponse(
        code=status.HTTP_200_OK,
        message="Authentification réussie",
        data=token_data
    )

@router.post(
    "/logout",
    response_model=LogoutResponse,
    status_code=status.HTTP_200_OK,
    summary="Déconnecter un utilisateur",
    description="Déconnecte un utilisateur en invalidant son token JWT.",
    responses={
        200: {
            "description": "Déconnexion réussie",
            "model": LogoutResponse
        },
        401: {
            "description": "Non authentifié",
            "model": AuthError,
            "content": {
                "application/json": {
                    "example": {
                        "code": 401,
                        "message": "Non authentifié",
                        "errors": [
                            {
                                "field": "authorization",
                                "message": "Token d'authentification invalide ou expiré"
                            }
                        ],
                        "status": "error"
                    }
                }
            }
        }
    }
)
async def logout(
    current_user: dict = Depends(get_current_user)
) -> LogoutResponse:
    """
    Déconnecte un utilisateur.

    Note: Dans une implémentation JWT stateless, la déconnexion côté serveur n'est 
    pas vraiment possible. Le client doit simplement supprimer le token.
    Cette fonction est fournie pour des raisons d'uniformité avec les autres APIs.

    Retourne un message de confirmation.
    """
    # Note: Dans un système JWT stateless, il n'y a pas vraiment de déconnexion côté serveur
    # Le client doit simplement supprimer le token
    
    # Dans une implémentation future, on pourrait ajouter le token à une liste noire
    # ou utiliser des tokens à révocation

    return LogoutResponse(
        code=status.HTTP_200_OK,
        message="Déconnexion réussie"
    )