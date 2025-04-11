from fastapi import Request, Response
from fastapi.responses import JSONResponse
from typing import Callable, Any, Dict, Optional
from starlette.middleware.base import BaseHTTPMiddleware
import json

from app.schemas.common import StatusCode

class NormalizedResponseMiddleware(BaseHTTPMiddleware):
    """
    Middleware qui normalise toutes les réponses dans le format standard de l'API.
    
    Cette classe intercepte les réponses JSON et les transforme selon le format standardisé:
    {
        "status": "success"|"error"|"warning"|"info",
        "code": HTTP_STATUS_CODE,
        "message": "Message descriptif",
        "data": données_originales,
        "meta": métadonnées_optionnelles,
        "errors": liste_erreurs_optionnelle
    }
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Méthode principale du middleware qui intercepte les requêtes et normalise les réponses.
        
        Args:
            request: Requête HTTP entrante
            call_next: Fonction pour traiter la requête
            
        Returns:
            Response: Réponse HTTP normalisée ou originale selon le cas
        """
        # Traitement normal de la requête
        response = await call_next(request)
        
        # Pas de normalisation pour certains cas
        if self._should_skip_normalization(request, response):
            return response
            
        # Essayer de normaliser la réponse
        try:
            body = json.loads(response.body)
            
            # Vérifier si la réponse est déjà normalisée
            if self._is_already_normalized(body):
                return response
                
            # Normaliser la réponse
            normalized_body = self._normalize_response(body, response.status_code)
            
            return JSONResponse(
                content=normalized_body,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except Exception:
            # En cas d'erreur, retourner la réponse originale sans modification
            return response
    
    def _should_skip_normalization(self, request: Request, response: Response) -> bool:
        """
        Détermine si la normalisation doit être ignorée pour cette requête/réponse.
        
        Args:
            request: Requête HTTP
            response: Réponse HTTP
            
        Returns:
            bool: True si la normalisation doit être ignorée
        """
        # Ne pas normaliser les réponses non-JSON
        if response.headers.get("content-type") != "application/json":
            return True
            
        # Ne pas normaliser les requêtes liées à la documentation API
        if request.url.path.startswith("/openapi") or request.url.path in ["/docs", "/redoc", "/rapidoc"]:
            return True
            
        return False
    
    def _is_already_normalized(self, body: Dict[str, Any]) -> bool:
        """
        Vérifie si une réponse est déjà au format normalisé.
        
        Args:
            body: Corps de la réponse
            
        Returns:
            bool: True si la réponse est déjà normalisée
        """
        return (
            isinstance(body, dict) and 
            "status" in body and 
            "code" in body and
            "message" in body
        )
    
    def _normalize_response(self, body: Any, status_code: int) -> Dict[str, Any]:
        """
        Normalise une réponse selon le format standard.
        
        Args:
            body: Corps de la réponse originale
            status_code: Code HTTP de la réponse
            
        Returns:
            Dict[str, Any]: Réponse normalisée
        """
        # Créer une réponse normalisée
        return {
            "status": StatusCode.SUCCESS,
            "code": status_code,
            "message": self._get_default_message(status_code),
            "data": body,
            "meta": None,
            "errors": None
        }
    
    def _get_default_message(self, status_code: int) -> str:
        """
        Retourne un message par défaut en fonction du code HTTP.
        
        Args:
            status_code: Code HTTP
            
        Returns:
            str: Message descriptif
        """
        if 200 <= status_code < 300:
            return "Opération réussie"
        elif status_code == 400:
            return "Requête invalide"
        elif status_code == 401:
            return "Non autorisé"
        elif status_code == 403:
            return "Accès interdit"
        elif status_code == 404:
            return "Ressource non trouvée"
        elif status_code == 422:
            return "Erreur de validation des données"
        elif 400 <= status_code < 500:
            return "Erreur client"
        elif 500 <= status_code < 600:
            return "Erreur serveur"
        else:
            return "Opération terminée"