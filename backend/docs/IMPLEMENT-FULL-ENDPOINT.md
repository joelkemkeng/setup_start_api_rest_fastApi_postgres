# IMPLEMENT-ENDPOINT.MD

# Guide complet d'implémentation d'endpoints dans l'API Mobile Musician

Ce guide détaillé décrit toutes les étapes à suivre pour implémenter un nouvel endpoint dans l'API Mobile Musician. Il couvre l'ensemble du processus, de la conception des schémas à la sécurisation des routes avec JWT.

## Table des matières

1. [Structure du projet](#1-structure-du-projet)
2. [Étape 1 : Définir les schémas de données](#étape-1--définir-les-schémas-de-données)
3. [Étape 2 : Créer ou mettre à jour le modèle de base de données](#étape-2--créer-ou-mettre-à-jour-le-modèle-de-base-de-données)
4. [Étape 3 : Implémenter l'endpoint](#étape-3--implémenter-lendpoint)
5. [Étape 4 : Ajouter la sécurité JWT](#étape-4--ajouter-la-sécurité-jwt)
6. [Étape 5 : Gérer les relations entre modèles](#étape-5--gérer-les-relations-entre-modèles)
7. [Étape 6 : Tests de l'endpoint](#étape-6--tests-de-lendpoint)
8. [Exemples complets](#exemples-complets)
9. [Troubleshooting](#troubleshooting)

## 1. Structure du projet

Avant de commencer, familiarisez-vous avec la structure du projet :

```
backend/
├── app/
│   ├── api/
│   │   ├── endpoints/          # Modules contenant les endpoints API
│   │   │   ├── __init__.py
│   │   │   ├── users.py        # Endpoints liés aux utilisateurs
│   │   │   └── ...             # Autres modules d'endpoint
│   │   ├── __init__.py
│   │   └── router.py           # Configuration des routeurs FastAPI
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration de l'application
│   │   ├── security.py         # Fonctions de sécurité (JWT, hashing)
│   │   └── exceptions.py       # Exceptions personnalisées
│   ├── middlewares/
│   │   ├── __init__.py
│   │   └── normalized_response.py  # Middleware pour normaliser les réponses
│   ├── models/                 # Modèles SQLAlchemy
│   │   ├── __init__.py
│   │   ├── base.py             # Classe de base pour les modèles
│   │   └── user.py             # Modèle User
│   ├── schemas/                # Schémas Pydantic
│   │   ├── __init__.py
│   │   ├── common.py           # Schémas communs (réponses)
│   │   └── user.py             # Schémas utilisateurs
│   ├── __init__.py
│   ├── database.py             # Configuration de la base de données
│   └── main.py                 # Point d'entrée de l'application
├── migrations/                 # Migrations Alembic
├── static/                     # Fichiers statiques
└── tests/                      # Tests
```

## Étape 1 : Définir les schémas de données

Les schémas Pydantic définissent la structure des données entrantes et sortantes de l'API.

### 1.1 Créer un nouveau fichier de schéma (si nécessaire)

Si vous ajoutez un concept entièrement nouveau (comme "Event" ou "Message"), créez un nouveau fichier dans `app/schemas/`.

```bash
touch backend/app/schemas/event.py
```

### 1.2 Définir les schémas de requête et de réponse

Pour chaque endpoint, vous aurez généralement besoin de :
- Schéma pour les données **entrantes** (ce que le client envoie)
- Schéma pour les données **sortantes** (ce que l'API renvoie)

Exemple pour un système d'événements musicaux :

```python
# app/schemas/event.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.schemas.common import SuccessResponse, ErrorResponse

class EventBase(BaseModel):
    """Schéma de base pour les événements."""
    title: str = Field(
        ..., 
        min_length=3, 
        max_length=100, 
        description="Titre de l'événement", 
        example="Concert au parc"
    )
    description: str = Field(
        ..., 
        min_length=10, 
        max_length=2000, 
        description="Description détaillée de l'événement",
        example="Concert en plein air avec plusieurs artistes locaux."
    )
    location: str = Field(
        ..., 
        min_length=3, 
        max_length=200, 
        description="Lieu de l'événement",
        example="Parc de la Villette, Paris"
    )
    event_date: datetime = Field(
        ..., 
        description="Date et heure de l'événement",
        example="2025-06-15T19:30:00Z"
    )
    
class EventCreate(EventBase):
    """Schéma pour la création d'un événement."""
    tags: Optional[List[str]] = Field(
        None, 
        description="Liste de tags/catégories pour l'événement",
        example=["jazz", "plein-air", "gratuit"]
    )

class EventResponseData(EventBase):
    """Données pour la réponse d'un événement."""
    id: UUID = Field(
        ..., 
        description="Identifiant unique de l'événement"
    )
    organizer_id: UUID = Field(
        ..., 
        description="Identifiant de l'organisateur"
    )
    created_at: datetime = Field(
        ..., 
        description="Date de création de l'événement"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Liste de tags/catégories pour l'événement"
    )
    
    class Config:
        from_attributes = True  # Pour Pydantic v2

class EventCreateResponse(SuccessResponse[EventResponseData]):
    """Réponse standardisée pour la création d'un événement."""
    code: int = 201
    message: str = "Événement créé avec succès"

class EventListResponse(SuccessResponse[List[EventResponseData]]):
    """Réponse standardisée pour la liste des événements."""
    code: int = 200
    message: str = "Événements récupérés avec succès"

class EventError(ErrorResponse[None]):
    """Réponse standardisée pour les erreurs liées aux événements."""
    pass
```

### 1.3 Mettre à jour le fichier __init__.py

Exportez les nouveaux schémas dans `app/schemas/__init__.py` :

```python
# app/schemas/__init__.py
from app.schemas.user import UserCreate, UserResponse, UserCreateResponse, UserResponseData
from app.schemas.common import StatusCode, SuccessResponse, ErrorResponse
from app.schemas.event import EventCreate, EventResponseData, EventCreateResponse, EventListResponse, EventError

__all__ = [
    # Utilisateurs
    "UserCreate", "UserResponse", "UserCreateResponse", "UserResponseData",
    # Événements
    "EventCreate", "EventResponseData", "EventCreateResponse", "EventListResponse", "EventError",
    # Communs
    "StatusCode", "SuccessResponse", "ErrorResponse"
]
```

## Étape 2 : Créer ou mettre à jour le modèle de base de données

### 2.1 Créer un nouveau fichier de modèle (si nécessaire)

```bash
touch backend/app/models/event.py
```

### 2.2 Définir le modèle SQLAlchemy

```python
# app/models/event.py
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.models.base import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(200), nullable=False)
    event_date = Column(DateTime, nullable=False)
    tags = Column(ARRAY(String), nullable=True, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Clé étrangère vers le modèle User
    organizer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Relation avec le modèle User (organisateur)
    organizer = relationship("User", back_populates="organized_events")
    
    # Relation many-to-many avec les participants
    participants = relationship(
        "User",
        secondary="event_participants",
        back_populates="participated_events"
    )
```

### 2.3 Mettre à jour le modèle User pour les relations

Si votre nouveau modèle a des relations avec le modèle User, mettez à jour `app/models/user.py` :

```python
# Ajouter ces lignes à app/models/user.py
# Relations avec les événements
organized_events = relationship("Event", back_populates="organizer")
participated_events = relationship(
    "Event",
    secondary="event_participants",
    back_populates="participants"
)
```

### 2.4 Créer une table d'association pour les relations many-to-many (si nécessaire)

```python
# Dans app/models/event.py, ajouter après la classe Event
from sqlalchemy import Table, Column, ForeignKey
from app.models.base import Base

# Table d'association pour la relation many-to-many User-Event
event_participants = Table(
    "event_participants",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("event_id", UUID(as_uuid=True), ForeignKey("events.id"), primary_key=True)
)
```

### 2.5 Mettre à jour le fichier __init__.py des modèles

```python
# app/models/__init__.py
from app.models.user import User
from app.models.event import Event, event_participants

__all__ = ["User", "Event", "event_participants"]
```

### 2.6 Créer une migration de base de données

Après avoir défini le modèle, créez une migration Alembic pour mettre à jour la base de données :

```bash
cd backend
alembic revision --autogenerate -m "Add Event model"
alembic upgrade head
```

## Étape 3 : Implémenter l'endpoint

### 3.1 Créer un fichier pour les endpoints (si nécessaire)

```bash
touch backend/app/api/endpoints/events.py
```

### 3.2 Implémenter les endpoints CRUD

Voici un exemple d'implémentation d'endpoints CRUD (Create, Read, Update, Delete) pour les événements :

```python
# app/api/endpoints/events.py
from fastapi import APIRouter, Depends, status, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import uuid

from app.models.event import Event
from app.models.user import User
from app.schemas.event import (
    EventCreate, EventResponseData, EventCreateResponse, 
    EventListResponse, EventError
)
from app.database import get_db
from app.core.exceptions import APIException
from app.core.security import get_current_user

router = APIRouter()

@router.post(
    "/",
    response_model=EventCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer un nouvel événement",
    description="Crée un nouvel événement musical organisé par l'utilisateur authentifié.",
    responses={
        201: {"description": "Événement créé avec succès"},
        401: {"description": "Non authentifié"},
        422: {"description": "Données invalides"}
    }
)
async def create_event(
    event: EventCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> EventCreateResponse:
    """
    Crée un nouvel événement musical.
    
    L'utilisateur authentifié devient automatiquement l'organisateur de l'événement.
    
    - **title**: Titre de l'événement (3-100 caractères)
    - **description**: Description détaillée (10-2000 caractères)
    - **location**: Lieu où se déroule l'événement (3-200 caractères)
    - **event_date**: Date et heure de l'événement (format ISO 8601)
    - **tags**: Liste facultative de tags/catégories
    """
    # Créer l'objet Event
    new_event = Event(
        id=uuid.uuid4(),
        title=event.title,
        description=event.description,
        location=event.location,
        event_date=event.event_date,
        tags=event.tags if event.tags else [],
        organizer_id=current_user.id,
        created_at=datetime.utcnow()
    )
    
    # Ajouter à la base de données
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    
    # Construire la réponse
    response_data = EventResponseData.model_validate(new_event)
    
    return EventCreateResponse(
        code=status.HTTP_201_CREATED,
        message="Événement créé avec succès",
        data=response_data
    )

@router.get(
    "/",
    response_model=EventListResponse,
    summary="Lister les événements",
    description="Récupère la liste des événements, avec possibilité de filtrage."
)
async def list_events(
    location: Optional[str] = Query(None, description="Filtrer par lieu"),
    tags: Optional[List[str]] = Query(None, description="Filtrer par tags"),
    start_date: Optional[datetime] = Query(None, description="Date de début"),
    end_date: Optional[datetime] = Query(None, description="Date de fin"),
    skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter (pagination)"),
    limit: int = Query(100, ge=1, le=100, description="Nombre d'éléments à retourner"),
    db: Session = Depends(get_db)
) -> EventListResponse:
    """Liste les événements disponibles avec options de filtrage."""
    query = db.query(Event)
    
    # Appliquer les filtres
    if location:
        query = query.filter(Event.location.ilike(f"%{location}%"))
    
    if tags:
        for tag in tags:
            query = query.filter(Event.tags.contains([tag]))
    
    if start_date:
        query = query.filter(Event.event_date >= start_date)
    
    if end_date:
        query = query.filter(Event.event_date <= end_date)
    
    # Pagination
    events = query.order_by(Event.event_date).offset(skip).limit(limit).all()
    
    # Convertir en schémas de réponse
    events_data = [EventResponseData.model_validate(event) for event in events]
    
    return EventListResponse(
        code=status.HTTP_200_OK,
        message="Événements récupérés avec succès",
        data=events_data
    )

@router.get(
    "/{event_id}",
    response_model=SuccessResponse[EventResponseData],
    summary="Obtenir un événement par ID",
    description="Récupère les détails d'un événement spécifique par son ID."
)
async def get_event(
    event_id: uuid.UUID = Path(..., description="ID de l'événement à récupérer"),
    db: Session = Depends(get_db)
) -> SuccessResponse[EventResponseData]:
    """Récupère les détails d'un événement spécifique."""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise APIException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Événement non trouvé",
            errors=[{
                "field": "event_id",
                "message": f"Aucun événement avec l'ID {event_id}"
            }]
        )
    
    return SuccessResponse(
        status="success",
        code=status.HTTP_200_OK,
        message="Événement récupéré avec succès",
        data=EventResponseData.model_validate(event)
    )

@router.put(
    "/{event_id}",
    response_model=SuccessResponse[EventResponseData],
    summary="Mettre à jour un événement",
    description="Met à jour les détails d'un événement existant. L'utilisateur doit être l'organisateur."
)
async def update_event(
    event_data: EventCreate,
    event_id: uuid.UUID = Path(..., description="ID de l'événement à mettre à jour"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> SuccessResponse[EventResponseData]:
    """
    Met à jour un événement existant.
    
    L'utilisateur authentifié doit être l'organisateur de l'événement.
    """
    # Récupérer l'événement
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise APIException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Événement non trouvé",
            errors=[{
                "field": "event_id",
                "message": f"Aucun événement avec l'ID {event_id}"
            }]
        )
    
    # Vérifier que l'utilisateur est bien l'organisateur
    if event.organizer_id != current_user.id:
        raise APIException(
            status_code=status.HTTP_403_FORBIDDEN,
            message="Accès interdit",
            errors=[{
                "field": "user",
                "message": "Vous n'êtes pas l'organisateur de cet événement"
            }]
        )
    
    # Mettre à jour les champs
    event.title = event_data.title
    event.description = event_data.description
    event.location = event_data.location
    event.event_date = event_data.event_date
    event.tags = event_data.tags if event_data.tags else []
    
    # Sauvegarder les modifications
    db.commit()
    db.refresh(event)
    
    return SuccessResponse(
        status="success",
        code=status.HTTP_200_OK,
        message="Événement mis à jour avec succès",
        data=EventResponseData.model_validate(event)
    )

@router.delete(
    "/{event_id}",
    response_model=SuccessResponse[None],
    summary="Supprimer un événement",
    description="Supprime un événement existant. L'utilisateur doit être l'organisateur."
)
async def delete_event(
    event_id: uuid.UUID = Path(..., description="ID de l'événement à supprimer"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> SuccessResponse[None]:
    """
    Supprime un événement existant.
    
    L'utilisateur authentifié doit être l'organisateur de l'événement.
    """
    # Récupérer l'événement
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise APIException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Événement non trouvé",
            errors=[{
                "field": "event_id",
                "message": f"Aucun événement avec l'ID {event_id}"
            }]
        )
    
    # Vérifier que l'utilisateur est bien l'organisateur
    if event.organizer_id != current_user.id:
        raise APIException(
            status_code=status.HTTP_403_FORBIDDEN,
            message="Accès interdit",
            errors=[{
                "field": "user",
                "message": "Vous n'êtes pas l'organisateur de cet événement"
            }]
        )
    
    # Supprimer l'événement
    db.delete(event)
    db.commit()
    
    return SuccessResponse(
        status="success",
        code=status.HTTP_200_OK,
        message="Événement supprimé avec succès"
    )

@router.post(
    "/{event_id}/participate",
    response_model=SuccessResponse[None],
    summary="Participer à un événement",
    description="Ajoute l'utilisateur courant à la liste des participants d'un événement."
)
async def participate_event(
    event_id: uuid.UUID = Path(..., description="ID de l'événement"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> SuccessResponse[None]:
    """
    Inscrit l'utilisateur comme participant à un événement.
    """
    # Récupérer l'événement
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise APIException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Événement non trouvé",
            errors=[{
                "field": "event_id",
                "message": f"Aucun événement avec l'ID {event_id}"
            }]
        )
    
    # Vérifier si l'utilisateur est déjà participant
    if current_user in event.participants:
        return SuccessResponse(
            status="success",
            code=status.HTTP_200_OK,
            message="Vous êtes déjà inscrit à cet événement"
        )
    
    # Ajouter l'utilisateur aux participants
    event.participants.append(current_user)
    db.commit()
    
    return SuccessResponse(
        status="success",
        code=status.HTTP_200_OK,
        message="Vous êtes maintenant inscrit à cet événement"
    )
```

### 3.3 Mettre à jour le routeur pour inclure les nouveaux endpoints

Mettez à jour `app/api/router.py` pour inclure le nouveau module d'endpoints :

```python
# app/api/router.py
from fastapi import APIRouter

from app.api.endpoints import users, events

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["Utilisateurs"])
api_router.include_router(events.router, prefix="/events", tags=["Événements"])
```

## Étape 4 : Ajouter la sécurité JWT

### 4.1 Configurer la fonction de sécurité

Si ce n'est pas déjà fait, assurez-vous que le module `security.py` est correctement configuré :

```python
# app/core/security.py
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from jose import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.models.user import User
from app.database import get_db
from app.core.exceptions import APIException

# Configuration pour le hashage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuration pour l'authentification OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_password_hash(password: str) -> str:
    """Hashe un mot de passe."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie si un mot de passe correspond au hash stocké."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Crée un token JWT pour l'utilisateur.
    
    Args:
        subject: Identifiant de l'utilisateur (généralement user.id)
        expires_delta: Durée de validité du token
        
    Returns:
        Token JWT encodé
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Récupère l'utilisateur actuellement authentifié via le token JWT.
    
    Cette fonction est utilisée comme dépendance pour les endpoints nécessitant une authentification.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise APIException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Token JWT invalide",
                errors=[{"message": "Token malformé - identifiant utilisateur manquant"}]
            )
    except jwt.JWTError:
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Token JWT invalide",
            errors=[{"message": "Token invalide ou expiré"}]
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Utilisateur non trouvé",
            errors=[{"message": "Utilisateur non trouvé ou désactivé"}]
        )
    
    if not user.is_active:
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Utilisateur inactif",
            errors=[{"message": "Ce compte utilisateur est désactivé"}]
        )
    
    return user

async def get_optional_user(
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme)
) -> Optional[User]:
    """
    Version optionnelle de get_current_user.
    
    Cette fonction peut être utilisée pour les endpoints qui fonctionnent avec ou sans authentification.
    """
    if not token:
        return None
    
    try:
        return await get_current_user(db=db, token=token)
    except HTTPException:
        return None
```

### 4.2 Utiliser la sécurité dans les endpoints

Pour sécuriser un endpoint, utilisez la dépendance `get_current_user` :

```python
@router.post("/secure-endpoint")
async def secure_endpoint(current_user: User = Depends(get_current_user)):
    """Cet endpoint n'est accessible qu'aux utilisateurs authentifiés."""
    return {"message": f"Bonjour, {current_user.username}!"}
```

Pour un endpoint qui fonctionne avec ou sans authentification :

```python
@router.get("/public-endpoint")
async def public_endpoint(current_user: Optional[User] = Depends(get_optional_user)):
    """Cet endpoint est accessible à tous, mais offre des fonctionnalités supplémentaires aux utilisateurs authentifiés."""
    if current_user:
        return {"message": f"Bonjour, {current_user.username}!"}
    else:
        return {"message": "Bonjour, visiteur!"}
```

## Étape 5 : Gérer les relations entre modèles

### 5.1 Relations One-to-Many

Pour une relation où un utilisateur peut créer plusieurs événements :

```python
# Dans le modèle User
organized_events = relationship("Event", back_populates="organizer")

# Dans le modèle Event
organizer_id = Column(UUID, ForeignKey("users.id"))
organizer = relationship("User", back_populates="organized_events")
```

Exemple d'utilisation dans un endpoint :

```python
@router.get("/users/{user_id}/events")
async def get_user_events(
    user_id: uuid.UUID,
    db: Session = Depends(get_db)
) -> SuccessResponse[List[EventResponseData]]:
    """Récupère tous les événements organisés par un utilisateur."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise APIException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Utilisateur non trouvé"
        )
    
    # Accès direct aux événements de l'utilisateur grâce à la relation
    events_data = [EventResponseData.model_validate(event) for event in user.organized_events]
    
    return SuccessResponse(
        status="success",
        code=status.HTTP_200_OK,
        message="Événements récupérés avec succès",
        data=events_data
    )
```

### 5.2 Relations Many-to-Many

Pour une relation où des utilisateurs peuvent participer à plusieurs événements et des événements peuvent avoir plusieurs participants :

```python
# Table d'association
event_participants = Table(
    "event_participants",
    Base.metadata,
    Column("user_id", UUID, ForeignKey("users.id"), primary_key=True),
    Column("event_id", UUID, ForeignKey("events.id"), primary_key=True)
)

# Dans le modèle User
participated_events = relationship(
    "Event",
    secondary=event_participants,
    back_populates="participants"
)

# Dans le modèle Event
participants = relationship(
    "User",
    secondary=event_participants,
    back_populates="participated_events"
)
```

Exemple d'utilisation dans un endpoint :

```python
@router.get("/users/{user_id}/participations")
async def get_user_participations(
    user_id: uuid.UUID,
    db: Session = Depends(get_db)
) -> SuccessResponse[List[EventResponseData]]:
    """Récupère tous les événements auxquels un utilisateur participe."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise APIException(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Utilisateur non trouvé"
        )
    
    # Accès direct aux événements auxquels l'utilisateur participe
    events_data = [EventResponseData.model_validate(event) for event in user.participated_events]
    
    return SuccessResponse(
        status="success",
        code=status.HTTP_200_OK,
        message="Participations récupérées avec succès",
        data=events_data
    )
```

### 5.3 Jointures et requêtes avancées

Pour des requêtes plus complexes, utilisez des jointures SQLAlchemy :

```python
@router.get("/events/popular")
async def get_popular_events(
    db: Session = Depends(get_db)
) -> SuccessResponse[List[Dict]]:
    """Récupère les événements les plus populaires (avec le plus de participants)."""
    # Requête avec jointure et agrégation
    from sqlalchemy import func
    from sqlalchemy.orm import aliased
    
    # Alias pour les tables
    ep = aliased(event_participants)
    
    # Sous-requête pour compter les participants
    subq = (
        db.query(
            ep.c.event_id.label("event_id"),
            func.count(ep.c.user_id).label("participant_count")
        )
        .group_by(ep.c.event_id)
        .subquery()
    )
    
    # Requête principale avec jointure
    events = (
        db.query(Event, subq.c.participant_count)
        .join(subq, Event.id == subq.c.event_id)
        .order_by(subq.c.participant_count.desc())
        .limit(10)
        .all()
    )
    
    # Construire la réponse
    result = []
    for event, count in events:
        event_data = EventResponseData.model_validate(event).dict()
        event_data["participant_count"] = count
        result.append(event_data)
    
    return SuccessResponse(
        status="success",
        code=status.HTTP_200_OK,
        message="Événements populaires récupérés avec succès",
        data=result
    )
```

## Étape 6 : Tests de l'endpoint

### 6.1 Créer des tests unitaires

Créez un fichier de test pour vos nouveaux endpoints :

```bash
mkdir -p backend/tests/api
touch backend/tests/api/test_events.py
```

```python
# tests/api/test_events.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid

from app.main import app
from app.models.user import User
from app.models.event import Event
from app.core.security import create_access_token

client = TestClient(app)

# Fixtures pour les tests
@pytest.fixture
def test_user(db: Session):
    """Crée un utilisateur de test."""
    user = User(
        id=uuid.uuid4(),
        username="testuser",
        email="testuser@example.com",
        password_hash="hashed_password",
        is_active=True,
        created_at=datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def auth_headers(test_user):
    """Crée des en-têtes d'authentification pour un utilisateur de test."""
    access_token = create_access_token(
        subject=str(test_user.id)
    )
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture
def test_event(db: Session, test_user):
    """Crée un événement de test."""
    event = Event(
        id=uuid.uuid4(),
        title="Test Event",
        description="Test description",
        location="Test location",
        event_date=datetime.utcnow() + timedelta(days=7),
        organizer_id=test_user.id,
        created_at=datetime.utcnow()
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

# Tests des endpoints
def test_create_event(client, auth_headers):
    """Teste la création d'un événement."""
    event_data = {
        "title": "New Event",
        "description": "Event description",
        "location": "Event location",
        "event_date": (datetime.utcnow() + timedelta(days=10)).isoformat(),
        "tags": ["music", "outdoor"]
    }
    
    response = client.post(
        "/api/v1/events/",
        json=event_data,
        headers=auth_headers
    )
    
    # Vérification du statut et de la structure
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["code"] == 201
    assert "event_id" in data["data"]
    assert data["data"]["title"] == event_data["title"]

def test_get_event(client, test_event):
    """Teste la récupération d'un événement."""
    response = client.get(f"/api/v1/events/{test_event.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["id"] == str(test_event.id)
    assert data["data"]["title"] == test_event.title

def test_update_event(client, auth_headers, test_event):
    """Teste la mise à jour d'un événement."""
    update_data = {
        "title": "Updated Event",
        "description": test_event.description,
        "location": test_event.location,
        "event_date": test_event.event_date.isoformat()
    }
    
    response = client.put(
        f"/api/v1/events/{test_event.id}",
        json=update_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["title"] == update_data["title"]

def test_list_events(client, test_event):
    """Teste la récupération de la liste des événements."""
    response = client.get("/api/v1/events/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    
    # Test des filtres
    response = client.get(f"/api/v1/events/?location={test_event.location}")
    assert response.status_code == 200
    data = response.json()
    assert len([e for e in data["data"] if e["id"] == str(test_event.id)]) == 1

def test_delete_event(client, auth_headers, test_event, db):
    """Teste la suppression d'un événement."""
    response = client.delete(
        f"/api/v1/events/{test_event.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    # Vérifier que l'événement a bien été supprimé
    event = db.query(Event).filter(Event.id == test_event.id).first()
    assert event is None
```

### 6.2 Exécuter les tests

```bash
cd backend
pytest tests/api/test_events.py -v
```

## Exemples complets

### Exemple 1 : Endpoint de connexion utilisateur

Voici un exemple complet d'implémentation d'un endpoint d'authentification :

```python
# app/api/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.models.user import User
from app.schemas.auth import Token, TokenData
from app.database import get_db
from app.core.security import verify_password, create_access_token
from app.core.exceptions import APIException
from app.config import settings

router = APIRouter()

@router.post(
    "/login",
    response_model=Token,
    summary="Authentifier un utilisateur",
    description="Authentifie un utilisateur avec son nom d'utilisateur/email et son mot de passe."
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Token:
    """
    Authentifie un utilisateur et génère un token JWT.
    
    - **username**: Nom d'utilisateur ou email
    - **password**: Mot de passe
    """
    # Rechercher l'utilisateur par nom d'utilisateur ou email
    user = db.query(User).filter(
        (User.username == form_data.username) | (User.email == form_data.username)
    ).first()
    
    # Vérifier si l'utilisateur existe et si le mot de passe est correct
    if not user or not verify_password(form_data.password, user.password_hash):
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Identifiants incorrects",
            errors=[{"field": "credentials", "message": "Nom d'utilisateur ou mot de passe incorrect"}]
        )
    
    # Vérifier si l'utilisateur est actif
    if not user.is_active:
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Utilisateur inactif",
            errors=[{"field": "user", "message": "Ce compte utilisateur est désactivé"}]
        )
    
    # Créer le token d'accès avec une durée de validité
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id),
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer"
    )
```

### Exemple 2 : Endpoint avec pagination et filtrage

Voici un exemple d'endpoint pour lister des utilisateurs avec pagination et filtrage :

```python
# app/api/endpoints/users.py
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.models.user import User
from app.schemas.user import UserPublic, UserListResponse
from app.database import get_db
from app.core.security import get_current_user

router = APIRouter()

@router.get(
    "/",
    response_model=UserListResponse,
    summary="Lister les utilisateurs",
    description="Récupère la liste des utilisateurs avec pagination et options de filtrage."
)
async def list_users(
    username: Optional[str] = Query(None, description="Filtrer par nom d'utilisateur"),
    is_active: Optional[bool] = Query(None, description="Filtrer par statut"),
    skip: int = Query(0, ge=0, description="Nombre d'éléments à sauter (pagination)"),
    limit: int = Query(100, ge=1, le=100, description="Nombre d'éléments à retourner"),
    sort_by: str = Query("username", description="Champ pour le tri"),
    sort_order: str = Query("asc", description="Ordre de tri (asc/desc)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserListResponse:
    """Liste les utilisateurs avec pagination et filtrage."""
    # Construire la requête de base
    query = db.query(User)
    
    # Appliquer les filtres
    if username:
        query = query.filter(User.username.ilike(f"%{username}%"))
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    # Appliquer le tri
    if sort_order.lower() == "desc":
        query = query.order_by(getattr(User, sort_by).desc())
    else:
        query = query.order_by(getattr(User, sort_by).asc())
    
    # Appliquer la pagination
    total = query.count()
    users = query.offset(skip).limit(limit).all()
    
    # Convertir en schémas
    user_list = [UserPublic.model_validate(user) for user in users]
    
    return UserListResponse(
        status="success",
        code=status.HTTP_200_OK,
        message="Utilisateurs récupérés avec succès",
        data=user_list,
        meta={
            "total": total,
            "page": skip // limit + 1,
            "pages": (total + limit - 1) // limit,
            "per_page": limit
        }
    )
```

## Troubleshooting

### Problème : Les imports ne fonctionnent pas

**Solution** : Vérifiez que tous les fichiers `__init__.py` sont présents et que les modules sont bien exportés.

### Problème : Erreur "Module not found"

**Solution** : Assurez-vous que le PYTHONPATH inclut bien le répertoire racine de votre projet.

### Problème : SQLAlchemy ne trouve pas les tables

**Solution** : Vérifiez que vos modèles sont bien importés dans `models/__init__.py` et que les migrations Alembic ont été exécutées.

### Problème : L'authentification JWT ne fonctionne pas

**Solution** : 
1. Vérifiez que les variables d'environnement SECRET_KEY et ALGORITHM sont correctement définies
2. Assurez-vous que les tokens générés ont le bon format
3. Vérifiez l'expiration des tokens

### Problème : Les relations entre modèles ne fonctionnent pas

**Solution** :
1. Vérifiez que les clés étrangères sont correctement définies
2. Assurez-vous que les relations `relationship()` sont bien configurées des deux côtés
3. Pour les relations many-to-many, vérifiez que la table d'association est correctement définie

### Problème : Les réponses ne sont pas correctement normalisées

**Solution** : 
1. Vérifiez que le middleware de normalisation est bien activé
2. Assurez-vous que les exceptions personnalisées sont correctement formatées
3. Vérifiez que les schémas de réponse héritent bien des classes de base (SuccessResponse, ErrorResponse)

### Problème : La validation Pydantic échoue

**Solution** :
1. Vérifiez les types de données que vous manipulez
2. Assurez-vous que les valeurs obligatoires sont bien fournies
3. Pour les conversions ORM vers Pydantic, assurez-vous que `from_attributes = True` est défini

---

En suivant ce guide étape par étape, vous devriez être en mesure d'implémenter efficacement des endpoints dans l'API Mobile Musician. Voici quelques conseils supplémentaires pour finaliser le processus :

## Timeline récapitulative

Pour résumer la procédure complète d'implémentation d'un endpoint, voici une timeline de référence :

### Jour 1 : Conception et modélisation

1. **9h00 - 10h00** : Analyser les besoins et définir les fonctionnalités de l'endpoint
2. **10h00 - 11h00** : Concevoir la structure des données (entrées/sorties)
3. **11h00 - 12h00** : Planifier les relations avec les modèles existants
4. **14h00 - 16h00** : Créer les schémas Pydantic
5. **16h00 - 17h00** : Créer ou mettre à jour les modèles SQLAlchemy

### Jour 2 : Implémentation

1. **9h00 - 10h00** : Créer les migrations de base de données et les appliquer
2. **10h00 - 12h00** : Implémenter les endpoints CRUD de base
3. **14h00 - 15h00** : Ajouter la sécurité JWT aux endpoints
4. **15h00 - 16h00** : Implémenter la gestion des relations entre modèles
5. **16h00 - 17h00** : Documenter les endpoints avec des docstrings et OpenAPI

### Jour 3 : Tests et finalisation

1. **9h00 - 11h00** : Écrire des tests unitaires pour les endpoints
2. **11h00 - 12h00** : Exécuter les tests et corriger les problèmes
3. **14h00 - 15h00** : Vérifier la documentation OpenAPI générée
4. **15h00 - 16h00** : Revue de code et optimisations
5. **16h00 - 17h00** : Mise à jour de la documentation du projet

## Liste de vérification finale

Avant de considérer un endpoint comme terminé, vérifiez les points suivants :

- [ ] Les schémas Pydantic sont complets avec des validations et exemples
- [ ] Les modèles SQLAlchemy sont correctement définis avec les relations appropriées
- [ ] Les migrations de base de données ont été créées et appliquées
- [ ] Les endpoints CRUD sont implémentés et fonctionnels
- [ ] La sécurité JWT est correctement appliquée si nécessaire
- [ ] Les réponses sont normalisées selon le format standard
- [ ] Les cas d'erreur sont gérés avec des messages appropriés
- [ ] La documentation OpenAPI est complète et précise
- [ ] Les tests unitaires couvrent les cas normaux et les cas d'erreur
- [ ] Le code respecte les conventions de style du projet

## Recommandations complémentaires

### Performances

Pour les endpoints qui manipulent de grandes quantités de données :

1. **Pagination** : Utilisez toujours la pagination pour limiter la taille des réponses
2. **Lazy Loading** : Utilisez `lazy='dynamic'` dans les relations SQLAlchemy pour éviter de charger des données inutiles
3. **Indexes** : Ajoutez des index SQL sur les colonnes fréquemment utilisées pour les filtres et les jointures

```python
# Exemple d'index dans SQLAlchemy
__table_args__ = (
    Index('idx_events_location', 'location'),
    Index('idx_events_date', 'event_date'),
)
```

### Documentation

Assurez-vous que chaque endpoint est bien documenté avec :

1. **Résumé** : Brève description (1 ligne) de ce que fait l'endpoint
2. **Description détaillée** : Explication complète avec contexte
3. **Paramètres de chemin et de requête** : Description de chaque paramètre
4. **Corps de requête** : Structure et validation des données entrantes
5. **Réponses** : Toutes les réponses possibles, avec codes HTTP et exemples

### Bonnes pratiques

1. **Noms d'endpoints** : Utilisez des noms pluriels pour les collections (`/users`, `/events`)
2. **Méthodes HTTP** : Respectez les conventions REST (GET pour lire, POST pour créer, etc.)
3. **Idempotence** : Les endpoints PUT et DELETE doivent être idempotents (plusieurs appels identiques ont le même effet qu'un seul)
4. **Validation** : Validez toutes les entrées avant de les traiter
5. **Messages d'erreur** : Fournissez des messages d'erreur clairs et utiles

## Conclusion

L'implémentation d'endpoints dans une API FastAPI comme Mobile Musician suit un processus bien défini, de la conception des schémas à la mise en place des tests. En suivant rigoureusement ces étapes et en utilisant les modèles fournis, vous pouvez créer des endpoints robustes, bien documentés et faciles à maintenir.

La structure modulaire de FastAPI, combinée avec la puissance de Pydantic et SQLAlchemy, permet de construire des APIs RESTful professionnelles avec un minimum d'effort. L'ajout de notre couche de normalisation des réponses améliore encore l'expérience pour les clients consommant l'API.
