from fastapi import Request, Response
from fastapi.responses import JSONResponse
from typing import Callable, Any
from starlette.middleware.base import BaseHTTPMiddleware
import json

from app.schemas.common import StatusCode

class NormalizedResponseMiddleware(BaseHTTPMiddleware):
    """
    Middleware qui normalise toutes les réponses dans le format standard de l'API.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Traitement normal de la requête
        response = await call_next(request)
        
        # Pas de normalisation pour les réponses non-JSON ou déjà normalisées
        if (
            response.headers.get("content-type") != "application/json" 
            or request.url.path.startswith("/openapi") 
            or request.url.path in ["/docs", "/redoc", "/rapidoc"]
        ):
            return response
            
        # Essayer de récupérer le contenu de la réponse
        try:
            body = json.loads(response.body)
            
            # Vérifier si la réponse est déjà normalisée
            if isinstance(body, dict) and "status" in body and "code" in body:
                return response
                
            # Normaliser la réponse
            normalized_body = {
                "status": StatusCode.SUCCESS,
                "code": response.status_code,
                "message": "Opération réussie",
                "data": body,
                "errors": None
            }
            
            return JSONResponse(
                content=normalized_body,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except:
            # En cas d'erreur, retourner la réponse originale
            return response