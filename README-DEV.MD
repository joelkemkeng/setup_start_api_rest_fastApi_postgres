# TuneLink Backend - Manuel du développeur sans VS Code

Ce guide détaille comment configurer, développer et contribuer au projet TuneLink Backend sans utiliser VS Code, en se basant uniquement sur Docker et les outils en ligne de commande.

## Table des matières

- [TuneLink Backend - Manuel du développeur sans VS Code](#tunelink-backend---manuel-du-développeur-sans-vs-code)
  - [Table des matières](#table-des-matières)
  - [Prérequis](#prérequis)
  - [Installation](#installation)
  - [Configuration du projet](#configuration-du-projet)
    - [Option 1 : Utilisation de Docker Compose (recommandé)](#option-1--utilisation-de-docker-compose-recommandé)
    - [Option 2 : Exécution locale avec Python](#option-2--exécution-locale-avec-python)
  - [Démarrage de l'application](#démarrage-de-lapplication)
    - [Avec Docker Compose](#avec-docker-compose)
    - [Sans Docker (en local)](#sans-docker-en-local)
  - [Workflow de développement](#workflow-de-développement)
  - [Exécution des tests](#exécution-des-tests)
  - [Documentation API](#documentation-api)
  - [Contribution au projet](#contribution-au-projet)
  - [Dépannage](#dépannage)
    - [Problèmes courants](#problèmes-courants)
    - [Commandes Docker utiles](#commandes-docker-utiles)
    - [Obtenir de l'aide](#obtenir-de-laide)

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les outils suivants :

- [Git](https://git-scm.com/downloads) (version 2.30.0 ou supérieure)
- [Docker](https://www.docker.com/products/docker-desktop) (version 20.10.0 ou supérieure)
- [Docker Compose](https://docs.docker.com/compose/install/) (généralement inclus avec Docker Desktop)

## Installation

1. **Clonez le dépôt GitHub** :
   ```bash
   git clone https://github.com/joelkemkeng/event_connect_back_end_api_python.git
   cd event_connect_back_end_api_python
   ```

2. **Créez une copie du fichier d'environnement** :
   ```bash
   cp backend/.env.example backend/.env
   ```

3. **Modifiez les variables d'environnement si nécessaire** :
   ```bash
   # Utilisez votre éditeur préféré
   nano backend/.env
   # ou
   vim backend/.env
   ```

## Configuration du projet

### Option 1 : Utilisation de Docker Compose (recommandé)

Cette méthode utilise Docker Compose pour configurer tous les services nécessaires.

1. **Construisez et démarrez les conteneurs** :
   ```bash
   docker-compose up --build
   ```

2. **Pour exécuter en arrière-plan** :
   ```bash
   docker-compose up -d
   ```

3. **Pour voir les logs quand l'application tourne en arrière-plan** :
   ```bash
   docker-compose logs -f
   ```

### Option 2 : Exécution locale avec Python

Si vous préférez exécuter l'application directement sur votre machine :

1. **Créez un environnement virtuel Python** :
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Sur Linux/macOS
   # ou
   venv\Scripts\activate     # Sur Windows
   ```

2. **Installez les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

## Démarrage de l'application

### Avec Docker Compose

Si les conteneurs sont déjà démarrés avec `docker-compose up`, l'application est accessible à http://localhost:8000.

Pour redémarrer les services après des modifications :
```bash
docker-compose restart
```

### Sans Docker (en local)

Pour démarrer l'application directement sur votre machine :
```bash
cd backend
source venv/bin/activate  # Si vous utilisez un environnement virtuel
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Workflow de développement

1. **Structure du projet** :
   ```
   event_connect_back_end_api_python/
   ├── backend/
   │   ├── app/                    
   │   │   ├── api/                # Endpoints de l'API
   │   │   ├── core/               # Configuration et utilitaires
   │   │   ├── models/             # Modèles de données
   │   │   ├── schemas/            # Schémas de validation
   │   │   ├── services/           # Logique métier
   │   │   └── main.py             # Point d'entrée de l'application
   │   ├── docs/                   # Documentation
   │   ├── scripts/                # Scripts utilitaires
   │   ├── static/                 # Fichiers statiques
   │   ├── tests/                  # Tests
   │   └── requirements.txt        # Dépendances Python
   ├── docker-compose.yml          # Configuration Docker Compose
   └── Dockerfile.backend          # Dockerfile pour le service backend
   ```

2. **Cycle de développement** :
   - Modifiez le code avec votre éditeur préféré
   - Appliquez les bonnes pratiques de formatage (voir ci-dessous)
   - Testez vos modifications
   - Soumettez vos changements via Git

3. **Formatage et linting** :
   ```bash
   cd backend
   # Formatage du code avec Black
   black .
   
   # Tri des imports avec isort
   isort .
   
   # Linting avec flake8
   flake8
   
   # Vérification des types avec mypy
   mypy .
   ```

## Exécution des tests

1. **Avec Docker** :
   ```bash
   docker-compose exec api pytest
   ```

2. **En local** :
   ```bash
   cd backend
   pytest
   ```

3. **Avec couverture de code** :
   ```bash
   cd backend
   pytest --cov=app
   ```

## Documentation API

Une fois l'application démarrée, la documentation de l'API est accessible aux URLs suivantes :

- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc
- RapiDoc : http://localhost:8000/rapidoc

## Contribution au projet

1. **Créez une branche pour vos fonctionnalités** :
   ```bash
   git checkout -b feature/nom-de-votre-fonctionnalité
   ```

2. **Committez vos changements** :
   ```bash
   git add .
   git commit -m "Description claire de vos modifications"
   ```

3. **Poussez vos changements vers GitHub** :
   ```bash
   git push origin feature/nom-de-votre-fonctionnalité
   ```

4. **Créez une Pull Request** :
   - Allez sur [le dépôt GitHub](https://github.com/joelkemkeng/event_connect_back_end_api_python)
   - Cliquez sur "Compare & pull request"
   - Remplissez le formulaire avec une description détaillée de vos modifications
   - Soumettez la Pull Request

5. **Meilleures pratiques de contribution** :
   - Assurez-vous que tous les tests passent
   - Suivez les conventions de codage du projet
   - Documentez les nouvelles fonctionnalités
   - Ajoutez des tests pour les nouvelles fonctionnalités

## Dépannage

### Problèmes courants

1. **L'application ne démarre pas** :
   ```bash
   # Vérifiez les logs Docker
   docker-compose logs
   
   # Vérifiez si les containers sont en cours d'exécution
   docker-compose ps
   ```

2. **Problèmes d'importation de modules Python** :
   - Assurez-vous d'exécuter les commandes depuis le bon répertoire (généralement `backend`)
   - Vérifiez que votre PYTHONPATH est correctement configuré

3. **Erreurs de base de données** :
   ```bash
   # Réinitialisez la base de données
   docker-compose down -v
   docker-compose up -d
   ```

4. **Problèmes d'accès aux fichiers** :
   - Vérifiez les permissions des fichiers et dossiers
   - Dans Docker, les fichiers sont souvent créés en tant que `root`

### Commandes Docker utiles

```bash
# Voir les conteneurs en cours d'exécution
docker-compose ps

# Arrêter tous les conteneurs
docker-compose down

# Supprimer les volumes (réinitialise les données)
docker-compose down -v

# Accéder au shell du conteneur backend
docker-compose exec api bash

# Voir les logs en temps réel
docker-compose logs -f

# Redémarrer un service spécifique
docker-compose restart api
```

### Obtenir de l'aide

Si vous rencontrez des problèmes :

1. Consultez les [issues](https://github.com/joelkemkeng/event_connect_back_end_api_python/issues) existantes
2. Créez une nouvelle issue avec :
   - Description détaillée du problème
   - Logs d'erreur
   - Étapes pour reproduire
   - Environnement (OS, versions de Docker, etc.)
