from typing import Generic, TypeVar, Optional, Any, Dict, List
from pydantic import BaseModel, Field
from enum import Enum

T = TypeVar('T')
M = TypeVar('M')  # Pour les métadonnées

class StatusCode(str, Enum):
    """Codes de statut pour les réponses API."""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

class PaginationMeta(BaseModel):
    """Métadonnées de pagination pour les listes."""
    total: int = Field(..., description="Nombre total d'éléments", example=100)
    page: int = Field(..., description="Page actuelle", example=1)
    pages: int = Field(..., description="Nombre total de pages", example=10)
    per_page: int = Field(..., description="Nombre d'éléments par page", example=10)
    
class ResponseBase(BaseModel, Generic[T, M]):
    """Schéma de base pour toutes les réponses API."""
    status: StatusCode = Field(..., description="Statut de la réponse (success, error, warning, info)")
    code: int = Field(..., description="Code HTTP de la réponse")
    message: str = Field(..., description="Message informatif sur la réponse")
    data: Optional[T] = Field(None, description="Données de la réponse (optionnel)")
    meta: Optional[M] = Field(None, description="Métadonnées (pagination, etc.)")
    errors: Optional[List[Dict[str, Any]]] = Field(None, description="Liste des erreurs (le cas échéant)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "code": 200,
                "message": "Opération réussie",
                "data": {},
                "meta": None,
                "errors": None
            }
        }

class SuccessResponse(ResponseBase[T, M]):
    """Réponse en cas de succès."""
    status: StatusCode = StatusCode.SUCCESS
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "code": 200,
                "message": "Opération réussie",
                "data": {},
                "meta": None,
                "errors": None
            }
        }

class ErrorResponse(ResponseBase[T, M]):
    """Réponse en cas d'erreur."""
    status: StatusCode = StatusCode.ERROR
    data: Optional[T] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "error",
                "code": 400,
                "message": "Erreur lors du traitement de la demande",
                "data": None,
                "meta": None,
                "errors": [
                    {
                        "field": "username",
                        "message": "Ce nom d'utilisateur est déjà utilisé"
                    }
                ]
            }
        }

class WarningResponse(ResponseBase[T, M]):
    """Réponse avec avertissement."""
    status: StatusCode = StatusCode.WARNING
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "warning",
                "code": 200,
                "message": "Opération réussie avec des avertissements",
                "data": {},
                "meta": None,
                "errors": [
                    {
                        "field": "password",
                        "message": "Le mot de passe choisi est faible"
                    }
                ]
            }
        }

class InfoResponse(ResponseBase[T, M]):
    """Réponse informative."""
    status: StatusCode = StatusCode.INFO
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "info",
                "code": 200,
                "message": "Information",
                "data": {},
                "meta": None,
                "errors": None
            }
        }

# Alias pour la compatibilité avec le code existant
class PaginatedResponse(SuccessResponse[T, PaginationMeta]):
    """Réponse paginée pour les listes d'éléments."""
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "code": 200,
                "message": "Liste récupérée avec succès",
                "data": [],
                "meta": {
                    "total": 100,
                    "page": 1,
                    "pages": 10,
                    "per_page": 10
                },
                "errors": None
            }
        }