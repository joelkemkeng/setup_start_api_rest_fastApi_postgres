# Système d'Authentification de l'API TuneLink

Ce document détaille le système d'authentification et d'autorisation utilisé dans l'API TuneLink.

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Flux d'authentification](#flux-dauthentification)
3. [Structure des tokens JWT](#structure-des-tokens-jwt)
4. [Sécurisation des endpoints](#sécurisation-des-endpoints)
5. [Gestion des sessions](#gestion-des-sessions)
6. [Tests et utilisation](#tests-et-utilisation)
7. [Cycle de vie du token](#cycle-de-vie-du-token)

## Vue d'ensemble

L'API TuneLink utilise l'authentification JWT (JSON Web Token) pour sécuriser l'accès aux ressources protégées. Le flux d'authentification suit le modèle suivant:

1. L'utilisateur s'inscrit ou se connecte
2. L'API génère et retourne un token JWT
3. Le client inclut ce token dans l'en-tête `Authorization` de chaque requête
4. L'API valide le token et autorise ou refuse l'accès

## Flux d'authentification

### 1. Inscription

Endpoint: `POST /api/v1/users/register`

Formulaire:
- **username**: Nom d'utilisateur unique
- **email**: Adresse email valide
- **password**: Mot de passe sécurisé (min 8 caractères, 1 chiffre, 1 majuscule)

Après inscription, l'utilisateur doit se connecter pour obtenir un token.

### 2. Connexion

Endpoint: `POST /api/v1/auth/login`

Formulaire:
- **email**: Email de l'utilisateur
- **password**: Mot de passe

Réponse:
```json
{
  "status": "success",
  "code": 200,
  "message": "Authentification réussie",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
    "token_type": "bearer"
  },
  "meta": null,
  "errors": null
}
```

### 3. Accès aux ressources protégées

Le client doit inclure l'en-tête suivant dans toutes les requêtes aux endpoints protégés:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...
```

### 4. Déconnexion

Endpoint: `POST /api/v1/auth/logout`

Nécessite un token valide. La déconnexion consiste à effacer le token côté client.

## Structure des tokens JWT

### Payload JWT

```json
{
  "sub": "83e89dc4-b40d-4083-a0b2-1e57bc56c032", // ID utilisateur
  "exp": 1681234567,                              // Date d'expiration
  "iat": 1681230967,                              // Date d'émission
  "type": "access_token"                          // Type de token
}
```

### Signature

Les tokens sont signés avec l'algorithme HMAC-SHA256 (HS256) en utilisant une clé secrète définie dans les paramètres de l'application.

## Sécurisation des endpoints

Les endpoints sont sécurisés à l'aide de la dépendance `get_current_user`:

```python
@router.get("/me", response_model=UserProfileResponse)
async def get_user_me(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserProfileResponse:
    # ...
```

### Endpoints publics

- `POST /api/v1/auth/login`
- `POST /api/v1/users/register`
- `GET /api/v1/users/profile/{user_id}`

### Endpoints protégés

- `GET /api/v1/users/me`
- `PATCH /api/v1/users/me`
- `PATCH /api/v1/users/me/instruments`
- `PATCH /api/v1/users/me/genres`
- `POST /api/v1/auth/logout`
- `GET /api/v1/users/profile/{user_id}`

## Gestion des sessions

L'API utilise un système stateless avec tokens JWT. Il n'y a pas de sessions côté serveur, mais:

- La date de dernière connexion (`last_login`) est mise à jour à chaque validation de token
- Les tokens expirent après un délai configurable (par défaut: 30 jours)
- L'utilisateur peut être désactivé (champ `is_active`) pour révoquer tous les accès

## Tests et utilisation

### Dans Swagger UI

1. Accédez à `/docs`
2. Connectez-vous via l'endpoint `/auth/login`
3. Copiez le token généré
4. Cliquez sur le bouton "Authorize" en haut de la page
5. Entrez `Bearer votre_token` dans le champ
6. Cliquez sur "Authorize" puis fermez la fenêtre
7. Tous les endpoints protégés sont maintenant accessibles

### Dans Postman ou autres clients API

1. Définissez la requête pour l'endpoint `/auth/login`
2. Exécutez-la pour obtenir le token JWT
3. Pour les requêtes suivantes, ajoutez l'en-tête: `Authorization: Bearer votre_token`

## Cycle de vie du token

1. **Création** : À la connexion réussie de l'utilisateur
2. **Utilisation** : Dans l'en-tête `Authorization` des requêtes
3. **Validation** : À chaque requête sur un endpoint protégé
4. **Expiration** : Après la durée configurée (paramètre `ACCESS_TOKEN_EXPIRE_MINUTES`)
5. **Révocation** : En désactivant le compte utilisateur (`is_active=False`)

---

Le système d'authentification JWT offre un bon équilibre entre sécurité et facilité d'utilisation, avec un fonctionnement sans état adapté aux architectures orientées API.