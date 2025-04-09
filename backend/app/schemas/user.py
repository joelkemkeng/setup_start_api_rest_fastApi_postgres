from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from uuid import UUID
from datetime import datetime

from app.schemas.common import SuccessResponse, ErrorResponse

class UserBase(BaseModel):
    """Schéma de base pour les utilisateurs."""
    username: str = Field(
        ..., 
        min_length=3, 
        max_length=50, 
        description="Nom d'utilisateur unique", 
        example="musicien2025"
    )
    email: EmailStr = Field(
        ..., 
        description="Adresse email valide", 
        example="musicien@example.com"
    )

class UserCreate(UserBase):
    """Schéma pour la création d'un utilisateur."""
    password: str = Field(
        ..., 
        min_length=8, 
        description="Mot de passe (minimum 8 caractères)", 
        example="MotDePasse123!"
    )
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Le mot de passe doit contenir au moins 8 caractères')
        if not any(char.isdigit() for char in v):
            raise ValueError('Le mot de passe doit contenir au moins un chiffre')
        if not any(char.isupper() for char in v):
            raise ValueError('Le mot de passe doit contenir au moins une lettre majuscule')
        return v

class UserInDB(UserBase):
    """Schéma complet d'un utilisateur en base de données."""
    id: UUID
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class UserResponseData(BaseModel):
    """Données pour la réponse de création d'utilisateur."""
    user_id: UUID = Field(
        ..., 
        description="Identifiant unique de l'utilisateur",
        example="83e89dc4-b40d-4083-a0b2-1e57bc56c032"
    )
    username: str = Field(
        ..., 
        description="Nom d'utilisateur",
        example="musicien2025"
    )

# Pour la compatibilité avec le code existant
class UserResponse(BaseModel):
    message: str = Field(..., description="Message de confirmation")
    user_id: UUID = Field(..., description="Identifiant unique de l'utilisateur")

# Réponses normalisées
class UserCreateResponse(SuccessResponse[UserResponseData]):
    """Réponse standardisée pour la création d'un utilisateur."""
    code: int = 201
    message: str = "Utilisateur créé avec succès"

class UserError(ErrorResponse[None]):
    """Réponse standardisée pour les erreurs liées aux utilisateurs."""
    pass