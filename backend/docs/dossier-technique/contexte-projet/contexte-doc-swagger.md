Voici un document Markdown détaillant un **Cursor Rule** (règle de guidance) pour une IA, spécifiquement conçu pour guider l'utilisation des bonnes pratiques avec Swagger/OpenAPI dans un projet FastAPI pour *Mobile Musician App*. Ce guide met l'accent sur une documentation claire et précise, une gestion correcte des types de données dans Swagger, une authentification bien implémentée, et des en-têtes (headers) générés de manière optimale, tout en limitant les restrictions inutiles pour laisser de la flexibilité. Ce Markdown est structuré pour être utilisé comme une base de connaissance par une IA ou un développeur.

---

```markdown
# Cursor Rule - Bonnes Pratiques pour Swagger/OpenAPI avec FastAPI

Ce document fournit des règles et des recommandations précises pour guider une IA ou un développeur dans l'implémentation et la documentation d'une API RESTful avec **FastAPI**, en utilisant **Swagger/OpenAPI** comme outil de documentation interactive. L'objectif est de garantir une API bien documentée, avec des formulaires Swagger cohérents avec les types de données attendus, une gestion sécurisée mais flexible de l'authentification, et des en-têtes bien définis. Ces règles s'appliquent au projet *Mobile Musician App* mais sont généralisables à d'autres projets FastAPI.

---

## Principes Généraux

### Objectif
- Fournir une documentation Swagger claire, intuitive et complète pour chaque endpoint.
- Assurer une correspondance exacte entre les types de données dans le code FastAPI et les formulaires affichés dans Swagger.
- Implémenter une authentification sécurisée avec JWT, tout en restant flexible sur les restrictions.
- Générer des en-têtes (headers) de manière standardisée et documentée.

### Contexte
- **Technologie** : FastAPI, qui génère automatiquement une spécification OpenAPI utilisée par Swagger.
- **Focus** : Backend de *Mobile Musician App* (gestion des utilisateurs, événements, messagerie, notifications).
- **Priorité** : Simplicité, clarté, et bonnes pratiques sans surcharger de restrictions inutiles.

---

## Règles Détaillées

### 1. Documentation Swagger/OpenAPI
#### Règle Générale
- Chaque endpoint doit être documenté avec une description claire, incluant son **objectif**, ses **entrées**, ses **sorties**, et des **exemples** si pertinent.
- Utiliser les décorateurs FastAPI (`@app.get`, `@app.post`, etc.) avec les paramètres `description`, `summary`, et `response_description` pour enrichir Swagger.

#### Mise en Pratique
- **Description** : Ajouter un texte explicatif dans `description` pour chaque route.
  ```python
  @app.post("/users/register", description="Crée un nouvel utilisateur dans le système.", summary="Inscription utilisateur")
  async def register_user(user: UserCreate):
      pass
  ```
- **Exemples** : Utiliser `responses` pour inclure des exemples de réponses.
  ```python
  from fastapi import FastAPI
  from pydantic import BaseModel

  app = FastAPI()

  class UserCreate(BaseModel):
      nom_utilisateur: str
      email: str
      mot_de_passe: str

  @app.post("/users/register", response_description="Utilisateur créé avec succès", responses={
      201: {"description": "Création réussie", "content": {"application/json": {"example": {"id": "uuid", "nom_utilisateur": "john_doe"}}}},
      400: {"description": "Erreur de validation", "content": {"application/json": {"example": {"detail": "Email déjà utilisé"}}}}
  })
  async def register_user(user: UserCreate):
      return {"id": "uuid", "nom_utilisateur": user.nom_utilisateur}
  ```

#### Bonne Pratique
- Toujours inclure un `summary` court et une `description` détaillée.
- Ajouter des exemples de succès (code 200/201) et d’erreur (400, 401, etc.) pour guider les utilisateurs de l’API.

---

### 2. Cohérence des Types de Données dans Swagger
#### Règle Générale
- Les formulaires Swagger doivent refléter précisément les types de données définis dans les modèles Pydantic utilisés par FastAPI.
- Si une donnée spécifique est attendue (ex. : fichier image, UUID), le formulaire Swagger doit le montrer clairement.

#### Mise en Pratique
1. **Types Simples (chaînes, nombres)** :
   - Utiliser des modèles Pydantic pour définir les entrées.
   - Swagger affiche automatiquement des champs texte ou numérique.
   ```python
   class EventCreate(BaseModel):
       titre: str
       latitude: float
       longitude: float
   @app.post("/events/")
   async def create_event(event: EventCreate):
       pass
   ```
   - Résultat dans Swagger : Champs texte pour `titre`, champs numériques pour `latitude` et `longitude`.

2. **Upload de Fichiers (ex. : Image)** :
   - Utiliser `UploadFile` de FastAPI pour les fichiers.
   - Swagger affiche un bouton "Choose File".
   ```python
   from fastapi import UploadFile, File

   @app.post("/users/profile-picture", description="Télécharge une photo de profil pour l'utilisateur.")
   async def upload_profile_picture(file: UploadFile = File(...)):
       return {"filename": file.filename}
   ```
   - Résultat dans Swagger : Un champ de type "file" pour uploader une image.

3. **Listes ou Objets Complexes** :
   - Définir des modèles imbriqués ou des listes dans Pydantic.
   ```python
   class Instrument(BaseModel):
       instrument_id: str
       niveau: str

   class UserInstruments(BaseModel):
       instruments: list[Instrument]

   @app.post("/users/instruments")
   async def add_instruments(data: UserInstruments):
       pass
   ```
   - Résultat dans Swagger : Un formulaire avec une liste d’objets (chaque objet ayant `instrument_id` et `niveau`).

#### Bonne Pratique
- Valider les types dans Pydantic (ex. : `EmailStr` pour les emails, `UUID` pour les identifiants).
- Ajouter des contraintes explicites (ex. : `max_length`, `minimum`) pour guider l’utilisateur dans Swagger.
  ```python
  from pydantic import BaseModel, EmailStr

  class UserCreate(BaseModel):
      nom_utilisateur: str = Field(..., max_length=50)
      email: EmailStr
  ```

---

### 3. Gestion de l’Authentification
#### Règle Générale
- Implémenter une authentification basée sur JWT, visible et testable dans Swagger.
- Ne pas imposer de restrictions excessives (ex. : éviter des politiques de sécurité trop strictes comme des expirations courtes inutiles).

#### Mise en Pratique
1. **Schéma d’Authentification** :
   - Utiliser `OAuth2PasswordBearer` pour gérer les tokens JWT.
   ```python
   from fastapi import Depends, HTTPException, status
   from fastapi.security import OAuth2PasswordBearer
   import jwt

   oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

   SECRET_KEY = "hetic"  # À sécuriser via variables d’environnement
   ALGORITHM = "HS256"

   def get_current_user(token: str = Depends(oauth2_scheme)):
       try:
           payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
           user_id = payload.get("sub")
           if not user_id:
               raise HTTPException(status_code=401, detail="Token invalide")
           return user_id
       except jwt.PyJWTError:
           raise HTTPException(status_code=401, detail="Token invalide")

   @app.get("/users/me", description="Retourne les informations de l’utilisateur connecté.")
   async def read_users_me(current_user: str = Depends(get_current_user)):
       return {"user_id": current_user}
   ```
   - Résultat dans Swagger : Bouton "Authorize" pour entrer un token, automatiquement ajouté aux en-têtes des endpoints protégés.

2. **Endpoint de Connexion** :
   ```python
   from pydantic import BaseModel

   class Login(BaseModel):
       email: str
       mot_de_passe: str

   @app.post("/users/login", description="Connecte un utilisateur et retourne un token JWT.")
   async def login_user(credentials: Login):
       # Simuler vérification (à remplacer par logique réelle)
       token = jwt.encode({"sub": "user_id_example"}, SECRET_KEY, algorithm=ALGORITHM)
       return {"access_token": token, "token_type": "bearer"}
   ```
   - Résultat dans Swagger : Formulaire avec champs `email` et `mot_de_passe`, réponse avec token testable.

#### Bonne Pratique
- Ajouter une description dans Swagger pour expliquer l’utilisation du token.
- Utiliser des variables d’environnement pour `SECRET_KEY` (ex. : via `python-dotenv`).
- Limiter les restrictions : Expiration longue (ex. : 24h) pour faciliter les tests, sans imposer de refresh tokens complexes sauf si nécessaire.

---

### 4. Gestion des En-têtes (Headers)
#### Règle Générale
- Les en-têtes doivent être générés automatiquement via FastAPI et bien documentés dans Swagger.
- Inclure les en-têtes standards (ex. : `Authorization`) et éviter les en-têtes personnalisés inutiles.

#### Mise en Pratique
1. **En-tête d’Authentification** :
   - Géré par `Depends(oauth2_scheme)` dans les routes protégées.
   - Swagger ajoute automatiquement `Authorization: Bearer <token>` dans les requêtes.
   ```python
   @app.get("/events/", description="Liste tous les événements.")
   async def list_events(current_user: str = Depends(get_current_user)):
       return {"events": []}
   ```

2. **En-têtes Personnalisés (si nécessaire)** :
   - Définir explicitement via `Header`.
   ```python
   from fastapi import Header

   @app.get("/events/nearby", description="Recherche les événements proches avec un rayon personnalisé.")
   async def nearby_events(radius: float = Header(default=10.0, description="Rayon en km")):
       return {"radius": radius}
   ```
   - Résultat dans Swagger : Champ pour entrer `radius` dans les en-têtes.

#### Bonne Pratique
- Documenter chaque en-tête dans `description` (ex. : "Rayon en km pour la recherche géographique").
- Préférer les paramètres de requête ou de corps aux en-têtes personnalisés pour simplifier l’API.

---

### 5. Limitation des Restrictions
#### Règle Générale
- Éviter les contraintes excessives qui compliquent l’utilisation ou le développement (ex. : validation trop stricte, politiques de sécurité inutilement complexes).

#### Mise en Pratique
- **Validation Flexible** : Permettre des valeurs optionnelles ou par défaut.
  ```python
  class EventCreate(BaseModel):
      titre: str
      description: str | None = None  # Optionnel
      capacite_max: int = 50  # Valeur par défaut
  ```
- **Authentification** : Ne pas imposer de refresh tokens ou d’expirations courtes sauf si explicitement requis.
- **Erreurs** : Retourner des messages d’erreur clairs sans bloquer l’utilisateur.
  ```python
  @app.post("/events/")
  async def create_event(event: EventCreate):
      if not event.titre:
          raise HTTPException(status_code=400, detail="Le titre est requis")
      return {"message": "Événement créé"}
  ```

#### Bonne Pratique
- Prioriser la simplicité pour un prototype (ex. : éviter les restrictions de taille de fichier sauf si critique).
- Documenter les cas où des restrictions pourraient être ajoutées ultérieurement.

---

### 6. Exemple Complet
Voici un exemple intégrant toutes les règles pour un endpoint typique :
```python
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field

app = FastAPI(title="Mobile Musician API", description="API pour connecter les musiciens.")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

class EventCreate(BaseModel):
    titre: str = Field(..., max_length=100, description="Titre de l'événement")
    description: str | None = Field(None, description="Description optionnelle")
    url_image: str | None = Field(None, description="URL de l'image (optionnel)")

@app.post("/events/", 
         summary="Créer un événement", 
         description="Permet à un utilisateur authentifié de créer un événement musical avec une image optionnelle.",
         response_description="Détails de l'événement créé",
         responses={
             201: {"description": "Événement créé", "content": {"application/json": {"example": {"id": "uuid", "titre": "Jam Paris"}}}},
             401: {"description": "Non authentifié", "content": {"application/json": {"example": {"detail": "Token requis"}}}}
         })
async def create_event(
    event: EventCreate, 
    image: UploadFile | None = File(None, description="Image de l'événement (optionnel)"), 
    current_user: str = Depends(oauth2_scheme)
):
    # Logique simulée
    if not current_user:
        raise HTTPException(status_code=401, detail="Utilisateur non authentifié")
    return {"id": "uuid", "titre": event.titre, "image": image.filename if image else None}
```

#### Résultat dans Swagger
- **Formulaire** : 
  - Champs texte pour `titre` et `description`.
  - Champ "Choose File" pour `image`.
  - Bouton "Authorize" pour le token JWT.
- **Documentation** : Summary, description, exemples de réponses (succès et erreur).
- **En-têtes** : `Authorization` automatiquement ajouté.

---

## Conclusion
Ces règles garantissent une API FastAPI bien documentée via Swagger/OpenAPI, avec :
- Une correspondance claire entre les types de données et les formulaires Swagger.
- Une authentification sécurisée mais flexible avec JWT.
- Des en-têtes standards et bien définis.
- Une approche minimaliste sur les restrictions pour un développement rapide et efficace.

Utilisez ce guide pour chaque endpoint de *Mobile Musician App* afin d’assurer une documentation de haute qualité et une expérience utilisateur optimale dans Swagger. Si vous avez besoin d’un exemple spécifique ou d’une implémentation, demandez-moi !
```

---

### Points Clés
- **Swagger** : Chaque endpoint est documenté avec `summary`, `description`, et `responses` pour une clarté maximale.
- **Types de Données** : Les formulaires Swagger reflètent les modèles Pydantic (texte, fichiers, listes), avec des exemples comme l’upload d’image.
- **Authentification** : JWT intégré via `OAuth2PasswordBearer`, testable dans Swagger, sans restrictions excessives.
- **En-têtes** : Gestion automatique par FastAPI, documentation explicite pour les cas personnalisés.
- **Flexibilité** : Restrictions limitées pour un prototype rapide, tout en suivant les bonnes pratiques.

Ce **Cursor Rule** est prêt à être utilisé comme guide pour toute IA travaillant sur le backend FastAPI de *Mobile Musician App*. Si vous voulez un exemple appliqué à un endpoint spécifique, je peux le détailler davantage !