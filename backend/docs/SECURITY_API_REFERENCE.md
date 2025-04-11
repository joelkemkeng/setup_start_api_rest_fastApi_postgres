# Référence de Sécurité API TuneLink

Ce document détaille les bonnes pratiques de sécurité et les mécanismes de protection implémentés dans l'API TuneLink.

## Table des matières

1. [Authentification](#authentification)
2. [Autorisation](#autorisation)
3. [Gestion des données sensibles](#gestion-des-données-sensibles)
4. [Format des réponses](#format-des-réponses)
5. [Validation des entrées](#validation-des-entrées)
6. [Headers de sécurité](#headers-de-sécurité)
7. [Meilleures pratiques](#meilleures-pratiques)

## Authentification

### JWT (JSON Web Tokens)

L'API utilise JSON Web Tokens pour l'authentification:

- **Algorithme**: HS256 (HMAC avec SHA-256)
- **Durée de vie**: 3 jours par défaut (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- **Claims standards**:
  - `sub`: ID utilisateur
  - `exp`: Date d'expiration 
  - `iat`: Date d'émission
  - `type`: Type de token ("access_token")

### Protection contre les attaques

- **Hachage des mots de passe**: Utilisation de bcrypt pour le stockage sécurisé
- **Rate limiting**: Limitations du nombre de requêtes pour prévenir le brute force
- **Validation des tokens**: Vérification stricte des signatures et de l'expiration

## Autorisation

### Middleware de contrôle d'accès

Le contrôle d'accès est implémenté via la dépendance `get_current_user`:

```python
@router.get("/protected")
async def protected_endpoint(current_user: dict = Depends(get_current_user)):
    # Accès uniquement si l'utilisateur est authentifié
    return {"message": "Accès autorisé"}
```

### Endpoints publics

Certains endpoints sont explicitement marqués comme publics et ne nécessitent pas d'authentification:

- `POST /api/v1/auth/login`
- `POST /api/v1/users/register`
- `GET /api/v1/users/profile/{user_id}`

## Gestion des données sensibles

### Données sensibles

- Les mots de passe ne sont jamais retournés dans les réponses API
- Les mots de passe sont toujours hachés avant d'être stockés en base de données
- Les informations sensibles comme les tokens sont transmises uniquement via HTTPS

### Clés et secrets

- La clé secrète JWT est configurable via la variable d'environnement `SECRET_KEY`
- En production, utiliser une clé forte et unique, générée aléatoirement
- Rotation régulière des clés recommandée (avec support pour la transition)

## Format des réponses

### Structure standardisée

Toutes les réponses suivent un format normalisé pour une meilleure gestion des erreurs:

```json
{
  "status": "success|error|warning|info",
  "code": 200,
  "message": "Description de la réponse",
  "data": { /* Données de la réponse */ },
  "meta": { /* Métadonnées (optionnel) */ },
  "errors": [ /* Liste des erreurs (optionnel) */ ]
}
```

### Gestion des erreurs

Les erreurs sont formatées de manière consistante, avec des informations détaillées sur le problème:

```json
{
  "status": "error",
  "code": 400,
  "message": "Erreur de validation des données",
  "data": null,
  "meta": null,
  "errors": [
    {
      "field": "email",
      "message": "Email invalide",
      "type": "validation_error"
    }
  ]
}
```

## Validation des entrées

### Validation Pydantic

Toutes les entrées utilisateur sont validées via les modèles Pydantic:

- Validation des types (string, int, etc.)
- Validation des formats (email, URL, etc.)
- Contraintes (longueur minimale/maximale, regex, etc.)

### Protection contre les injections

- Utilisation de requêtes paramétrées avec SQLAlchemy
- Validation stricte des UUID et autres identifiants
- Sanitization des entrées utilisateur

## Headers de sécurité

L'API utilise plusieurs headers de sécurité pour renforcer la protection:

- **CORS**: Configuration stricte pour limiter les domaines autorisés
- **X-Content-Type-Options**: Défini à "nosniff"
- **X-Frame-Options**: Défini à "DENY"
- **Content-Security-Policy**: Restrictions strictes pour prévenir les attaques XSS

## Meilleures pratiques

### Pour les développeurs

1. **Ne jamais hardcoder de secrets** dans le code source
2. **Toujours utiliser les outils d'authentification existants** plutôt que de créer des contournements
3. **Valider toutes les entrées utilisateur**, même si elles semblent inoffensives
4. **Suivre le principe du moindre privilège** pour chaque opération
5. **Journaliser les actions sensibles** pour faciliter l'audit de sécurité

### Pour les déploiements

1. **Activer HTTPS** en production
2. **Configurer des clés fortes** via les variables d'environnement
3. **Mettre en place une surveillance** des tentatives d'authentification échouées
4. **Effectuer des audits réguliers** des dépendances
5. **Mettre à jour régulièrement** les bibliothèques et frameworks

---

Pour toute question relative à la sécurité de l'API, contacter l'équipe de développement.