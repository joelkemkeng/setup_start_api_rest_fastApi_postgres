from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Form, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Any, List, Dict, Optional
from datetime import datetime
import uuid
import os
import shutil
from fastapi.responses import JSONResponse

from app.models.user import User
from app.schemas.user import (
    UserCreate, UserCreateResponse, UserResponseData, UserError, 
    UserProfile, UserProfileResponse, UserProfileUpdate,
    UsersListResponse
)
from app.database import get_db
from app.core.security import get_password_hash, get_current_user
from app.config import settings

router = APIRouter()

@router.post(
    "/register", 
    status_code=status.HTTP_201_CREATED, 
    response_model=UserCreateResponse,
    summary="Créer un nouveau compte utilisateur",
    description="Crée un nouveau compte utilisateur avec un nom d'utilisateur unique, une adresse email et un mot de passe.",
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "multipart/form-data": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "description": "Nom d'utilisateur unique (3-50 caractères)",
                                "example": "musicien2025",
                                "minLength": 3,
                                "maxLength": 50
                            },
                            "email": {
                                "type": "string",
                                "description": "Adresse email valide",
                                "example": "musicien@example.com",
                                "format": "email"
                            },
                            "password": {
                                "type": "string",
                                "description": "Mot de passe sécurisé (min 8 caractères, au moins 1 chiffre et 1 majuscule)",
                                "example": "MotDePasse123!",
                                "minLength": 8,
                                "format": "password"
                            }
                        },
                        "required": ["username", "email", "password"]
                    },
                    "encoding": {
                        "username": {
                            "contentType": "text/plain"
                        },
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
        201: {
            "description": "Utilisateur créé avec succès",
            "model": UserCreateResponse,
            "content": {
                "application/json": {
                    "example": {
                        "code": 201,
                        "message": "Utilisateur créé avec succès",
                        "data": {
                            "user_id": "550e8400-e29b-41d4-a716-446655440000",
                            "username": "musicien2025"
                        }
                    }
                }
            }
        },
        400: {
            "description": "Erreur de validation des données",
            "model": UserError,
            "content": {
                "application/json": {
                    "example": {
                        "code": 400,
                        "message": "Erreur lors du traitement de la demande",
                        "errors": [
                            {
                                "field": "username",
                                "message": "Ce nom d'utilisateur est déjà utilisé"
                            }
                        ],
                        "status": "error"
                    }
                }
            }
        },
        422: {
            "description": "Données invalides",
            "model": UserError,
            "content": {
                "application/json": {
                    "example": {
                        "code": 422,
                        "message": "Erreur de validation des données",
                        "errors": [
                            {
                                "field": "password",
                                "message": "Le mot de passe doit contenir au moins 8 caractères"
                            }
                        ],
                        "status": "error"
                    }
                }
            }
        }
    }
)
async def register(
    username: str = Form(..., min_length=3, max_length=50, description="Nom d'utilisateur unique (3-50 caractères)", example="musicien2025", media_type="multipart/form-data"),
    email: str = Form(..., description="Adresse email valide", example="musicien@example.com", media_type="multipart/form-data"),
    password: str = Form(..., min_length=8, description="Mot de passe sécurisé (min 8 caractères, au moins 1 chiffre et 1 majuscule)", example="MotDePasse123!", media_type="multipart/form-data"),
    db: Session = Depends(get_db)
) -> UserCreateResponse:
    """
    Crée un nouveau compte utilisateur dans le système.
    
    - **username**: Nom d'utilisateur unique (3-50 caractères)
    - **email**: Adresse email valide et unique
    - **password**: Mot de passe sécurisé (min 8 caractères, au moins 1 chiffre et 1 majuscule)
    
    Retourne un message de confirmation et l'identifiant de l'utilisateur créé.
    """
    # Valider le mot de passe manuellement puisqu'on n'utilise plus Pydantic ici
    if len(password) < 8:
        error_response = UserError(
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Mot de passe trop court",
            errors=[{
                "field": "password",
                "message": "Le mot de passe doit contenir au moins 8 caractères"
            }]
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error_response.dict()
        )
    
    if not any(char.isdigit() for char in password):
        error_response = UserError(
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Mot de passe trop faible",
            errors=[{
                "field": "password",
                "message": "Le mot de passe doit contenir au moins un chiffre"
            }]
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error_response.dict()
        )
    
    if not any(char.isupper() for char in password):
        error_response = UserError(
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Mot de passe trop faible",
            errors=[{
                "field": "password",
                "message": "Le mot de passe doit contenir au moins une lettre majuscule"
            }]
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error_response.dict()
        )
    
    # Vérifier si l'email est valide
    # Simple validation, à améliorer dans une version future
    if "@" not in email or "." not in email:
        error_response = UserError(
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Email invalide",
            errors=[{
                "field": "email",
                "message": "L'adresse email n'est pas valide"
            }]
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error_response.dict()
        )
    
    existing_user = db.query(User).filter(
        (User.email == email) | (User.username == username)
    ).first()

    if existing_user:
        # Version normalisée de l'erreur
        errors: List[Dict[str, str]] = []
        
        if existing_user.username == username:
            errors.append({
                "field": "username",
                "message": "Ce nom d'utilisateur est déjà utilisé"
            })
            
        if existing_user.email == email:
            errors.append({
                "field": "email",
                "message": "Cette adresse email est déjà utilisée"
            })
            
        error_response = UserError(
            code=status.HTTP_400_BAD_REQUEST,
            message="Le nom d'utilisateur ou l'email est déjà utilisé",
            errors=errors
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_response.dict()
        )

    # Hacher le mot de passe
    password_hash = get_password_hash(password)

    # Créer l'utilisateur avec seulement les champs de base
    new_user = User(
        id=uuid.uuid4(),
        username=username,
        email=email,
        password_hash=password_hash,
        created_at=datetime.utcnow(),
        is_active=True,
        last_login=datetime.utcnow()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Création d'une réponse normalisée
    response_data = UserResponseData(
        user_id=new_user.id,
        username=new_user.username
    )
    
    return UserCreateResponse(
        code=status.HTTP_201_CREATED,
        message="Utilisateur créé avec succès",
        data=response_data
    )


@router.get(
    "/me",
    response_model=UserProfileResponse,
    summary="Récupérer le profil de l'utilisateur connecté",
    description="Récupère les informations du profil de l'utilisateur actuellement connecté",
    responses={
        200: {
            "description": "Profil utilisateur récupéré avec succès",
            "model": UserProfileResponse
        },
        401: {
            "description": "Non authentifié",
            "model": UserError,
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
        },
        404: {
            "description": "Utilisateur non trouvé",
            "model": UserError,
            "content": {
                "application/json": {
                    "example": {
                        "code": 404,
                        "message": "Utilisateur non trouvé",
                        "errors": [
                            {
                                "field": "user_id",
                                "message": "L'utilisateur n'existe pas"
                            }
                        ],
                        "status": "error"
                    }
                }
            }
        }
    }
)
async def get_user_me(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserProfileResponse:
    """
    Récupère le profil complet de l'utilisateur actuellement connecté.
    
    Retourne toutes les informations du profil, y compris les instruments et genres.
    """
    user_id = current_user.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        error_response = UserError(
            code=status.HTTP_404_NOT_FOUND,
            message="Utilisateur non trouvé",
            errors=[{
                "field": "user_id",
                "message": "L'utilisateur n'existe pas"
            }]
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response.dict()
        )
    
    # Créer le profil utilisateur
    user_profile = UserProfile(
        id=user.id,
        username=user.username,
        profile_picture=user.profile_picture,
        biography=user.biography,
        latitude=user.latitude,
        longitude=user.longitude
    )
    
    return UserProfileResponse(
        code=status.HTTP_200_OK,
        message="Profil utilisateur récupéré avec succès",
        data=user_profile
    )


@router.patch(
    "/me",
    response_model=UserProfileResponse,
    summary="Mettre à jour le profil de l'utilisateur connecté",
    description="Met à jour les informations du profil de l'utilisateur actuellement connecté",
    openapi_extra={
        "requestBody": {
            "content": {
                "multipart/form-data": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "username": {
                                "type": "string",
                                "description": "Nom d'utilisateur unique (3-50 caractères)",
                                "example": "musicien2025",
                                "minLength": 3,
                                "maxLength": 50
                            },
                            "profile_picture": {
                                "type": "string",
                                "format": "binary",
                                "description": "Image de profil (formats acceptés: jpg, jpeg, png)",
                                "example": "photo_profil.jpg"
                            },
                            "biography": {
                                "type": "string",
                                "description": "Biographie du musicien (expérience, style musical, etc.)",
                                "example": "Musicien passionné avec 10 ans d'expérience en guitare classique et jazz. J'ai joué dans plusieurs groupes et participé à des festivals locaux."
                            },
                            "latitude": {
                                "type": "number",
                                "format": "float",
                                "description": "Latitude de la position géographique (entre -90 et 90)",
                                "example": 48.8566,
                                "minimum": -90,
                                "maximum": 90
                            },
                            "longitude": {
                                "type": "number",
                                "format": "float",
                                "description": "Longitude de la position géographique (entre -180 et 180)",
                                "example": 2.3522,
                                "minimum": -180,
                                "maximum": 180
                            }
                        }
                    },
                    "encoding": {
                        "profile_picture": {
                            "contentType": "image/jpeg, image/png"
                        }
                    }
                }
            }
        }
    },
    responses={
        200: {
            "description": "Profil utilisateur mis à jour avec succès",
            "model": UserProfileResponse,
            "content": {
                "application/json": {
                    "example": {
                        "code": 200,
                        "message": "Profil utilisateur mis à jour avec succès",
                        "data": {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "username": "musicien2025",
                            "profile_picture": "http://localhost:8000/static/profile_pictures/550e8400-e29b-41d4-a716-446655440000.jpg",
                            "biography": "Musicien passionné avec 10 ans d'expérience...",
                            "latitude": 48.8566,
                            "longitude": 2.3522
                        }
                    }
                }
            }
        },
        400: {
            "description": "Erreur de validation des données",
            "model": UserError,
            "content": {
                "application/json": {
                    "example": {
                        "code": 400,
                        "message": "Erreur lors du traitement de la demande",
                        "errors": [
                            {
                                "field": "username",
                                "message": "Ce nom d'utilisateur est déjà utilisé"
                            }
                        ],
                        "status": "error"
                    }
                }
            }
        },
        401: {
            "description": "Non authentifié",
            "model": UserError,
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
        },
        422: {
            "description": "Données invalides",
            "model": UserError,
            "content": {
                "application/json": {
                    "example": {
                        "code": 422,
                        "message": "Erreur de validation des données",
                        "errors": [
                            {
                                "field": "profile_picture",
                                "message": "Le fichier doit être une image (jpg, jpeg, png)"
                            }
                        ],
                        "status": "error"
                    }
                }
            }
        }
    }
)
async def update_user_me(
    username: Optional[str] = Form(None, min_length=3, max_length=50, description="Nom d'utilisateur unique", example="musicien2025"),
    profile_picture: Optional[UploadFile] = File(None, description="Image de profil (jpg, jpeg, png)", media_type="image/*"),
    biography: Optional[str] = Form(None, description="Biographie du musicien", example="Musicien passionné avec 10 ans d'expérience..."),
    latitude: Optional[float] = Form(None, description="Latitude de la position géographique", example=48.8566),
    longitude: Optional[float] = Form(None, description="Longitude de la position géographique", example=2.3522),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserProfileResponse:
    """
    Met à jour le profil de l'utilisateur connecté.
    
    - **username**: Nouveau nom d'utilisateur (optionnel)
    - **profile_picture**: Image de profil (jpg, jpeg, png) (optionnel)
    - **biography**: Biographie du musicien (optionnel)
    - **latitude**: Latitude de la position géographique (optionnel)
    - **longitude**: Longitude de la position géographique (optionnel)
    
    Retourne le profil mis à jour avec l'URL de l'image de profil.
    """
    user_id = current_user.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        error_response = UserError(
            code=status.HTTP_404_NOT_FOUND,
            message="Utilisateur non trouvé",
            errors=[{
                "field": "user_id",
                "message": "L'utilisateur n'existe pas"
            }]
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response.dict()
        )

    # Vérifier si le nouveau nom d'utilisateur est déjà pris
    if username and username != user.username:
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            error_response = UserError(
                code=status.HTTP_400_BAD_REQUEST,
                message="Erreur lors du traitement de la demande",
                errors=[{
                    "field": "username",
                    "message": "Ce nom d'utilisateur est déjà utilisé"
                }]
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_response.dict()
            )
        user.username = username

    # Gérer l'upload de l'image de profil
    if profile_picture:
        # Vérifier le type de fichier
        allowed_extensions = [".jpg", ".jpeg", ".png"]
        file_ext = os.path.splitext(profile_picture.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            error_response = UserError(
                code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                message="Type de fichier non supporté",
                errors=[{
                    "field": "profile_picture",
                    "message": "Le fichier doit être une image (jpg, jpeg, png)"
                }]
            )
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=error_response.dict()
            )

        # Créer le dossier de stockage s'il n'existe pas
        upload_dir = os.path.join("static", "profile_pictures")
        os.makedirs(upload_dir, exist_ok=True)

        # Générer un nom de fichier unique
        file_name = f"{user_id}{file_ext}"
        file_path = os.path.join(upload_dir, file_name)

        # Sauvegarder le fichier
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(profile_picture.file, buffer)
        except Exception as e:
            error_response = UserError(
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Erreur lors de la sauvegarde de l'image",
                errors=[{
                    "field": "profile_picture",
                    "message": str(e)
                }]
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_response.dict()
            )

        # Mettre à jour l'URL de l'image dans la base de données
        image_url = f"{settings.BASE_URL}/static/profile_pictures/{file_name}"
        user.profile_picture = image_url

    # Mettre à jour les autres champs s'ils sont fournis
    if biography is not None:
        user.biography = biography
    if latitude is not None:
        user.latitude = latitude
    if longitude is not None:
        user.longitude = longitude

    db.commit()
    db.refresh(user)

    # Créer le profil utilisateur mis à jour
    user_profile = UserProfile(
        id=user.id,
        username=user.username,
        profile_picture=user.profile_picture,
        biography=user.biography,
        latitude=user.latitude,
        longitude=user.longitude
    )
    
    return UserProfileResponse(
        code=status.HTTP_200_OK,
        message="Profil utilisateur mis à jour avec succès",
        data=user_profile
    )


@router.get(
    "/profile/{user_id}",
    response_model=UserProfileResponse,
    summary="Récupérer le profil d'un utilisateur",
    description="""
    Récupère les informations du profil d'un utilisateur par son ID (endpoint public).
    
    **Exemples d'IDs utilisateurs disponibles:**
    - musicien1: remplacer avec l'ID généré lors de la création des données
    - musicien2: remplacer avec l'ID généré lors de la création des données
    
    Vous pouvez utiliser le endpoint GET /api/v1/users/me pour obtenir votre propre ID utilisateur.
    """,
    responses={
        200: {
            "description": "Profil utilisateur récupéré avec succès",
            "model": UserProfileResponse
        },
        404: {
            "description": "Utilisateur non trouvé",
            "model": UserError,
            "content": {
                "application/json": {
                    "example": {
                        "code": 404,
                        "message": "Utilisateur non trouvé",
                        "errors": [
                            {
                                "field": "user_id",
                                "message": "L'utilisateur n'existe pas"
                            }
                        ],
                        "status": "error"
                    }
                }
            }
        },
        422: {
            "description": "Format d'ID invalide",
            "model": UserError,
            "content": {
                "application/json": {
                    "example": {
                        "code": 422,
                        "message": "Erreur de validation des données",
                        "errors": [
                            {
                                "field": "user_id",
                                "message": "L'ID de l'utilisateur doit être un UUID valide"
                            }
                        ],
                        "status": "error"
                    }
                }
            }
        }
    }
)
async def get_user_profile(
    user_id: uuid.UUID = Path(..., description="ID de l'utilisateur à consulter"),
    db: Session = Depends(get_db)
) -> UserProfileResponse:
    """
    Récupère le profil complet d'un utilisateur par son ID.
    
    Retourne toutes les informations publiques du profil, y compris les instruments et genres.
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        error_response = UserError(
            code=status.HTTP_404_NOT_FOUND,
            message="Utilisateur non trouvé",
            errors=[{
                "field": "user_id",
                "message": "L'utilisateur n'existe pas"
            }]
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_response.dict()
        )
    
    # Créer le profil utilisateur
    user_profile = UserProfile(
        id=user.id,
        username=user.username,
        profile_picture=user.profile_picture,
        biography=user.biography,
        latitude=user.latitude,
        longitude=user.longitude
    )
    
    return UserProfileResponse(
        code=status.HTTP_200_OK,
        message="Profil utilisateur récupéré avec succès",
        data=user_profile
    )