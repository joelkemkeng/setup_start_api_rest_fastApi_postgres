from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from app.schemas.common import StatusCode

class APIException(HTTPException):
    """
    Exception personnalisée pour les erreurs API.
    Génère une réponse normalisée avec le format standard de l'API.
    """
    
    def __init__(
        self, 
        status_code: int = status.HTTP_400_BAD_REQUEST,
        message: str = "Une erreur est survenue",
        errors: Optional[List[Dict[str, Any]]] = None,
        headers: Optional[Dict[str, Any]] = None
    ):
        self.status_api = StatusCode.ERROR
        self.message = message
        self.errors = errors or []
        
        # Formater le détail selon notre format de réponse standard
        detail = {
            "status": self.status_api,
            "code": status_code,
            "message": self.message,
            "data": None,
            "errors": self.errors
        }
        
        super().__init__(status_code=status_code, detail=detail, headers=headers)