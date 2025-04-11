# Guide du Développeur TuneLink API

Ce document est destiné aux développeurs travaillant sur l'API TuneLink. Il explique l'architecture, les conventions et les bonnes pratiques à suivre.

## Table des matières

1. [Structure du projet](#structure-du-projet)
2. [Configuration et démarrage](#configuration-et-démarrage)
3. [Optimisations récentes](#optimisations-récentes)
4. [Conventions de codage](#conventions-de-codage)
5. [Documentation technique](#documentation-technique)
6. [Workflow de développement](#workflow-de-développement)

## Structure du projet

```
backend/
├── alembic.ini              # Configuration de l'outil de migration
├── app/                     # Code source de l'application
│   ├── api/                 # Endpoints API
│   │   ├── endpoints/       # Endpoints organisés par domaine
│   │   └── router.py        # Routeur principal
│   ├── core/                # Fonctionnalités centrales
│   │   ├── exceptions.py    # Gestion des exceptions
│   │   └── security.py      # Authentification et sécurité
│   ├── crud/                # Opérations CRUD
│   ├── database.py          # Configuration de la base de données
│   ├── main.py              # Point d'entrée de l'application
│   ├── middlewares/         # Middlewares FastAPI
│   ├── models/              # Modèles SQLAlchemy
│   ├── schemas/             # Schémas Pydantic
│   │   ├── auth.py          # Schémas d'authentification
│   │   ├── common.py        # Schémas communs/partagés
│   │   └── user.py          # Schémas utilisateur
│   └── services/            # Logique métier
├── docs/                    # Documentation technique
├── migrations/              # Migrations Alembic
├── scripts/                 # Scripts utilitaires
├── static/                  # Fichiers statiques
└── requirements.txt         # Dépendances du projet
```

## Configuration et démarrage

### Variables d'environnement

L'API utilise les variables d'environnement suivantes:

```sh
# Base de données
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tunelink

# Sécurité
SECRET_KEY=your_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=4320  # 3 jours

# Serveur
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

### Démarrage du serveur

```sh
# Installation des dépendances
pip install -r requirements.txt

# Migrations
cd backend
alembic upgrade head

# Démarrage du serveur
cd backend
uvicorn app.main:app --reload
```

## Optimisations récentes

### Formulaires Swagger améliorés

Les endpoints ont été optimisés pour utiliser des formulaires structurés dans Swagger UI:

- Les endpoints JSON complexes ont été remplacés par des formulaires avec champs individuels
- Chaque champ contient des exemples préremplis pour faciliter les tests
- Meilleure documentation des paramètres

### Suppression des doublons d'endpoints

- Suppression de `/auth/login-form` en faveur de `/auth/login` avec formulaire
- Cohérence dans les formats de requête/réponse

### Réponses standardisées

Toutes les réponses suivent un format uniforme:

```json
{
  "status": "success|error|warning|info",
  "code": 200,
  "message": "Description de la réponse",
  "data": { /* Données principales */ },
  "meta": { /* Métadonnées (pagination, etc.) */ },
  "errors": [ /* Liste des erreurs (si échec) */ ]
}
```

Voir `docs/REPONSES_STANDARDISEES.md` pour plus de détails.

## Conventions de codage

### Nommage

- **Fichiers**: snake_case (ex: `user_profile.py`)
- **Classes**: PascalCase (ex: `UserProfile`)
- **Fonctions/méthodes**: snake_case (ex: `get_user_profile`)
- **Variables**: snake_case (ex: `user_profile`)
- **Constantes**: UPPER_SNAKE_CASE (ex: `MAX_USERS`)

### Documentation

- Documenter toutes les fonctions avec des docstrings
- Documenter tous les endpoints avec des descriptions précises
- Ajouter des exemples pour les requêtes/réponses complexes

### Validation

- Utiliser les validateurs Pydantic pour les entrées
- Gérer correctement les exceptions avec le middleware normalisé

## Documentation technique

- `AUTH_SYSTEM.md`: Système d'authentification JWT
- `REPONSES_STANDARDISEES.md`: Format des réponses API
- `SWAGGER_AUTH_ISSUES.md`: Guide d'optimisation Swagger
- `USER_MODEL.md`: Documentation du modèle utilisateur

## Workflow de développement

1. **Création de branche**: Pour chaque fonctionnalité, créer une branche
2. **Migrations**: Utiliser Alembic pour les changements de modèles
3. **Tests**: Ajouter des tests dans `app/test/`
4. **Documentation**: Mettre à jour la documentation technique
5. **Pull Request**: Créer une PR avec une description détaillée

---

Pour toute question ou suggestion, contacter l'équipe de développement.