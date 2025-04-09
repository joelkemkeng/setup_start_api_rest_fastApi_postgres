from typing import Generic, TypeVar, Optional, Any, Dict, List
from pydantic import BaseModel, Field
from enum import Enum

T = TypeVar('T')

class StatusCode(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

class ResponseBase(BaseModel, Generic[T]):
    """Schéma de base pour toutes les réponses API."""
    status: StatusCode = Field(..., description="Statut de la réponse")
    code: int = Field(..., description="Code HTTP de la réponse")
    message: str = Field(..., description="Message informatif sur la réponse")
    data: Optional[T] = Field(None, description="Données de la réponse (optionnel)")
    errors: Optional[List[Dict[str, Any]]] = Field(None, description="Liste des erreurs (le cas échéant)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "code": 200,
                "message": "Opération réussie",
                "data": {},
                "errors": None
            }
        }

class SuccessResponse(ResponseBase[T]):
    """Réponse en cas de succès."""
    status: StatusCode = StatusCode.SUCCESS
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "code": 200,
                "message": "Opération réussie",
                "data": {},
                "errors": None
            }
        }

class ErrorResponse(ResponseBase[T]):
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
                "errors": [
                    {
                        "field": "username",
                        "message": "Ce nom d'utilisateur est déjà utilisé"
                    }
                ]
            }
        }