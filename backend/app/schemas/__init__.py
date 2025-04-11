# Exporter les schémas pour qu'ils soient disponibles directement depuis app.schemas
from app.schemas.user import UserCreate, UserResponse, UserCreateResponse, UserResponseData, UserError
from app.schemas.common import StatusCode, SuccessResponse, ErrorResponse
from app.schemas.auth import Token, AuthResponse, AuthError, LogoutResponse, TokenPayload

__all__ = [
    # Utilisateurs
    "UserCreate", 
    "UserResponse",
    "UserCreateResponse",
    "UserResponseData", 
    "UserError",
    
    # Authentification
    "Token",
    "AuthResponse",
    "AuthError",
    "LogoutResponse",
    "TokenPayload",
    
    # Communs
    "StatusCode",
    "SuccessResponse",
    "ErrorResponse"
]