# Guide des Réponses Standardisées - API TuneLink

Ce document décrit le format standard de réponse utilisé par l'API TuneLink. Toutes les réponses de l'API suivent un format uniforme pour faciliter la consommation par les clients.

## Table des matières

1. [Format de réponse standard](#format-de-réponse-standard)
2. [Types de réponses](#types-de-réponses)
3. [Gestion des erreurs](#gestion-des-erreurs)
4. [Réponses paginées](#réponses-paginées)
5. [Format des exemples](#format-des-exemples)
6. [Utilisation avec Swagger](#utilisation-avec-swagger)
7. [Validation](#validation)

## Format de réponse standard

Toutes les réponses API suivent ce format standard:

```json
{
  "status": "success|error|warning|info",
  "code": 200,
  "message": "Message descriptif",
  "data": { /* Données de la réponse (pour les succès) */ },
  "meta": { /* Métadonnées (pagination, etc.) */ },
  "errors": [ /* Erreurs détaillées (pour les erreurs) */ ]
}
```

### Champs de la réponse

| Champ | Type | Description |
|-------|------|-------------|
| `status` | string | État de la réponse : `"success"`, `"error"`, `"warning"`, `"info"` |
| `code` | integer | Code HTTP de la réponse (200, 400, 401, etc.) |
| `message` | string | Message explicatif sur la réponse |
| `data` | any\|null | Données de la réponse (présent dans les réponses positives) |
| `meta` | object\|null | Métadonnées supplémentaires (pagination, etc.) |
| `errors` | array\|null | Liste détaillée des erreurs (présent dans les réponses négatives) |

## Types de réponses

### Réponse de succès

```json
{
  "status": "success",
  "code": 200,
  "message": "Opération réussie",
  "data": {
    "id": "83e89dc4-b40d-4083-a0b2-1e57bc56c032",
    "username": "musicien2025"
  },
  "meta": null,
  "errors": null
}
```

### Réponse d'erreur

```json
{
  "status": "error",
  "code": 400,
  "message": "Erreur lors du traitement de la demande",
  "data": null,
  "meta": null,
  "errors": [
    {
      "field": "username",
      "message": "Ce nom d'utilisateur est déjà utilisé"
    },
    {
      "field": "email",
      "message": "Cette adresse email est déjà utilisée"
    }
  ]
}
```

### Réponse d'avertissement

```json
{
  "status": "warning",
  "code": 200,
  "message": "Opération réussie avec des avertissements",
  "data": {
    "id": "83e89dc4-b40d-4083-a0b2-1e57bc56c032"
  },
  "meta": null,
  "errors": [
    {
      "field": "password",
      "message": "Le mot de passe choisi est faible"
    }
  ]
}
```

### Réponse d'information

```json
{
  "status": "info",
  "code": 200,
  "message": "Information disponible",
  "data": {
    "maintenance": "Le service sera en maintenance le 10 juin de 2h à 4h"
  },
  "meta": null,
  "errors": null
}
```

## Gestion des erreurs

Les erreurs sont normalisées pour faciliter leur traitement par le client. Chaque erreur contient:

- `field`: Le champ concerné par l'erreur (peut être un chemin comme `user.profile.email`)
- `message`: Message d'erreur explicite pour l'utilisateur final
- `type` (optionnel): Type d'erreur pour un traitement spécifique côté client

Exemple d'erreur de validation:

```json
{
  "status": "error",
  "code": 422,
  "message": "Erreur de validation des données",
  "data": null,
  "meta": null,
  "errors": [
    {
      "field": "username",
      "type": "value_error.min_length",
      "message": "Le nom d'utilisateur doit contenir au moins 3 caractères"
    },
    {
      "field": "email",
      "type": "value_error.email",
      "message": "L'adresse email n'est pas valide"
    }
  ]
}
```

## Réponses paginées

Pour les listes d'éléments, les métadonnées de pagination sont incluses dans le champ `meta`:

```json
{
  "status": "success",
  "code": 200,
  "message": "Liste récupérée avec succès",
  "data": [
    { "id": "1", "name": "Item 1" },
    { "id": "2", "name": "Item 2" }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "pages": 50,
    "per_page": 2
  },
  "errors": null
}
```

Champs de métadonnées pour la pagination:

| Champ | Type | Description |
|-------|------|-------------|
| `total` | integer | Nombre total d'éléments |
| `page` | integer | Numéro de la page actuelle |
| `pages` | integer | Nombre total de pages |
| `per_page` | integer | Nombre d'éléments par page |

## Format des exemples

Pour tester facilement les endpoints dans Swagger, tous les schémas incluent des exemples. Par exemple:

### Format d'entrée

```json
{
  "username": "musicien2025", 
  "email": "musicien@example.com",
  "password": "MotDePasse123!"
}
```

### Format de sortie

```json
{
  "status": "success",
  "code": 201,
  "message": "Utilisateur créé avec succès",
  "data": {
    "user_id": "83e89dc4-b40d-4083-a0b2-1e57bc56c032",
    "username": "musicien2025"
  },
  "meta": null,
  "errors": null
}
```

## Utilisation avec Swagger

L'API TuneLink fournit deux approches pour interagir avec les endpoints:

1. **Formulaires JSON**: Pour les requêtes complexes, vous pouvez envoyer un objet JSON complet.
2. **Formulaires structurés**: Pour les requêtes simples, vous pouvez utiliser les formulaires générés automatiquement.

Exemple pour l'authentification:
- Endpoint `/api/v1/auth/login`: Accepte un objet JSON avec email et mot de passe.
- Endpoint `/api/v1/auth/login-form`: Fournit un formulaire standard OAuth2 pour faciliter les tests.

## Validation

Pour vous assurer que vos réponses suivent le format standard, vous pouvez utiliser l'un de ces frameworks:

### Pour JavaScript/TypeScript

```typescript
interface StandardResponse<T, M> {
  status: 'success' | 'error' | 'warning' | 'info';
  code: number;
  message: string;
  data?: T | null;
  meta?: M | null;
  errors?: Array<{
    field: string;
    message: string;
    type?: string;
  }> | null;
}
```

### Pour Python (Pydantic)

```python
from typing import Generic, TypeVar, Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

T = TypeVar('T')
M = TypeVar('M')

class StatusCode(str, Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

class Error(BaseModel):
    field: str
    message: str
    type: Optional[str] = None

class ResponseBase(BaseModel, Generic[T, M]):
    status: StatusCode
    code: int
    message: str
    data: Optional[T] = None
    meta: Optional[M] = None
    errors: Optional[List[Error]] = None
```

---

En suivant ce format de réponse standardisé, vous pouvez garantir une expérience de développement cohérente et prévisible pour les consommateurs de votre API.