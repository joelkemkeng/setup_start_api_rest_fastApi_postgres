from fastapi import APIRouter, Depends

from app.api.endpoints import users, auth
from app.core.security import get_current_user

api_router = APIRouter()

# Routes d'authentification (pas besoin d'être authentifié)
api_router.include_router(
    auth.router, 
    prefix="/auth", 
    tags=["Authentification"]
)

# Routes utilisateur générales
api_router.include_router(
    users.router, 
    prefix="/users", 
    tags=["Utilisateurs"]
)