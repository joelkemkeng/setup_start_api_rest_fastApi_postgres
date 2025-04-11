# Modèle Utilisateur (Musicien)

## Introduction

Le modèle Utilisateur est la base de l'application TuneLink. Il représente un musicien avec ses informations de profil, ses compétences musicales (instruments) et ses préférences musicales (genres).

## Modèles

### Utilisateur (User)

```python
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Profile information
    profile_picture = Column(String, nullable=True)
    biography = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    instruments = relationship("Instrument", secondary=user_instrument, back_populates="users")
    genres = relationship("Genre", secondary=user_genre, back_populates="users")
```

### Instrument (Instrument)

```python
class Instrument(Base):
    __tablename__ = "instruments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=True)
    icon_url = Column(String, nullable=True)
    
    # Relationships
    users = relationship("User", secondary=user_instrument, back_populates="instruments")
```

### Genre (Genre)

```python
class Genre(Base):
    __tablename__ = "genres"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    users = relationship("User", secondary=user_genre, back_populates="genres")
```

### Tables d'Association

#### user_instrument

```python
user_instrument = Table(
    "user_instrument",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("instrument_id", UUID(as_uuid=True), ForeignKey("instruments.id"), primary_key=True),
    Column("skill_level", String, nullable=False)
)
```

#### user_genre

```python
user_genre = Table(
    "user_genre",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
    Column("genre_id", UUID(as_uuid=True), ForeignKey("genres.id"), primary_key=True)
)
```

## Schémas API

### UserCreate

```python
class UserCreate(UserBase):
    password: str
    profile_picture: Optional[str] = None
    biography: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    instruments: Optional[List[UserInstrumentLink]] = None
    genres: Optional[List[UserGenreLink]] = None
```

### UserProfile

```python
class UserProfile(BaseModel):
    id: UUID
    username: str
    profile_picture: Optional[str] = None
    biography: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    instruments: List[InstrumentInDB] = []
    genres: List[GenreInDB] = []
```

### UserProfileUpdate

```python
class UserProfileUpdate(BaseModel):
    username: Optional[str] = None
    profile_picture: Optional[str] = None
    biography: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
```

## Endpoints API

### Créer un utilisateur

```
POST /api/v1/users/register
```

Crée un nouveau compte utilisateur avec toutes les informations de profil.

### Récupérer son profil

```
GET /api/v1/users/me
```

Récupère les informations du profil de l'utilisateur connecté.

### Mettre à jour son profil

```
PATCH /api/v1/users/me
```

Met à jour les informations du profil de l'utilisateur connecté.

### Récupérer le profil d'un utilisateur

```
GET /api/v1/users/profile/{user_id}
```

Récupère les informations du profil d'un utilisateur par son ID.

## Utilisation avec JWT

Le modèle Utilisateur est intégré avec le système d'authentification JWT. Lors de la connexion, le token JWT généré contient l'ID de l'utilisateur dans le claim `sub`.

La dépendance `get_current_user` vérifie que l'utilisateur existe en base de données et est actif avant de donner accès aux endpoints protégés.

## Relations avec d'autres entités

- **Instruments**: Relation many-to-many avec les instruments, avec un niveau de compétence pour chaque instrument
- **Genres**: Relation many-to-many avec les genres musicaux
- Dans les futures phases, l'utilisateur sera également lié aux événements, messages, etc.