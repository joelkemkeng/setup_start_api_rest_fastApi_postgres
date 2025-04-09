from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List, Dict
from datetime import datetime
import uuid

from app.models.user import User
from app.schemas.user import UserCreate, UserCreateResponse, UserResponseData, UserError
from app.database import get_db
from app.core.security import get_password_hash

router = APIRouter()

@router.post(
    "/register", 
    status_code=status.HTTP_201_CREATED, 
    response_model=UserCreateResponse,
    summary="Créer un nouveau compte utilisateur",
    description="Crée un nouveau compte utilisateur avec un nom d'utilisateur unique, une adresse email et un mot de passe.",
    responses={
        201: {
            "description": "Utilisateur créé avec succès",
            "model": UserCreateResponse
        },
        400: {
            "description": "Nom d'utilisateur ou email déjà utilisé",
            "model": UserError
        },
        422: {
            "description": "Validation échouée - données invalides",
            "model": UserError
        }
    }
)
async def register(user: UserCreate, db: Session = Depends(get_db)) -> UserCreateResponse:
    """
    Crée un nouveau compte utilisateur dans le système.
    
    - **username**: Nom d'utilisateur unique (3-50 caractères)
    - **email**: Adresse email valide et unique
    - **password**: Mot de passe sécurisé (min 8 caractères, au moins 1 chiffre et 1 majuscule)
    
    Retourne un message de confirmation et l'identifiant de l'utilisateur créé.
    """
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()

    if existing_user:
        # Version normalisée de l'erreur
        errors: List[Dict[str, str]] = []
        
        if existing_user.username == user.username:
            errors.append({
                "field": "username",
                "message": "Ce nom d'utilisateur est déjà utilisé"
            })
            
        if existing_user.email == user.email:
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

    password_hash = get_password_hash(user.password)

    new_user = User(
        id=uuid.uuid4(),
        username=user.username,
        email=user.email,
        password_hash=password_hash,
        created_at=datetime.utcnow(),
        is_active=True
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