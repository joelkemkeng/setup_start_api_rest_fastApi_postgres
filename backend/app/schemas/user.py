from pydantic import BaseModel, EmailStr, Field, validator, HttpUrl, confloat
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.schemas.common import SuccessResponse, ErrorResponse, PaginatedResponse




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
    """Schéma pour la création d'un utilisateur - contient uniquement les champs obligatoires."""
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


class UserProfileUpdate(BaseModel):
    """Schéma pour la mise à jour du profil utilisateur."""
    username: Optional[str] = Field(
        None, 
        min_length=3, 
        max_length=50, 
        description="Nom d'utilisateur unique", 
        example="musicien2025"
    )
    profile_picture: Optional[str] = Field(
        None, 
        description="URL de la photo de profil", 
        example="https://example.com/profile.jpg"
    )
    biography: Optional[str] = Field(
        None, 
        description="Biographie du musicien", 
        example="Musicien passionné avec 10 ans d'expérience..."
    )
    latitude: Optional[float] = Field(
        None, 
        description="Latitude de la position géographique", 
        example=48.8566
    )
    longitude: Optional[float] = Field(
        None, 
        description="Longitude de la position géographique", 
        example=2.3522
    )




class UserInDB(UserBase):
    """Schéma complet d'un utilisateur en base de données."""
    id: UUID
    created_at: datetime
    is_active: bool
    profile_picture: Optional[str] = None
    biography: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    """Schéma pour afficher le profil complet d'un utilisateur."""
    id: UUID = Field(..., description="Identifiant unique de l'utilisateur")
    username: str = Field(..., description="Nom d'utilisateur")
    profile_picture: Optional[str] = Field(None, description="URL de la photo de profil")
    biography: Optional[str] = Field(None, description="Biographie du musicien")
    latitude: Optional[float] = Field(None, description="Latitude de la position géographique")
    longitude: Optional[float] = Field(None, description="Longitude de la position géographique")
    
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


# Type None pour représenter aucune métadonnée
class NoMetadata(BaseModel):
    pass


# Réponses normalisées avec le type None explicite pour les métadonnées
class UserCreateResponse(SuccessResponse[UserResponseData, None]):
    """Réponse standardisée pour la création d'un utilisateur."""
    code: int = 201
    message: str = "Utilisateur créé avec succès"


class UserProfileResponse(SuccessResponse[UserProfile, None]):
    """Réponse standardisée pour le profil d'un utilisateur."""
    code: int = 200
    message: str = "Profil utilisateur récupéré avec succès"


class UsersListResponse(PaginatedResponse[List[UserProfile]]):
    """Réponse standardisée pour la liste des utilisateurs avec pagination."""
    code: int = 200
    message: str = "Liste des utilisateurs récupérée avec succès"


class UserError(ErrorResponse[None, None]):
    """Réponse standardisée pour les erreurs liées aux utilisateurs."""
    pass