# TuneLink Backend

Ce guide complet fournit toutes les informations nécessaires pour cloner, configurer, développer et contribuer au projet TuneLink Backend, que vous utilisiez VS Code avec Dev Containers ou un autre environnement de développement.

## Table des matières

- [TuneLink Backend](#tunelink-backend)
  - [Table des matières](#table-des-matières)
  - [Accès à pgAdmin](#accès-à-pgadmin)
  - [Prérequis](#prérequis)
  - [Clonage du projet](#clonage-du-projet)
  - [Configuration de l'environnement](#configuration-de-lenvironnement)
    - [Option 1 : Avec VS Code et Dev Containers](#option-1--avec-vs-code-et-dev-containers)
    - [Option 2 : Sans VS Code (Docker uniquement)](#option-2--sans-vs-code-docker-uniquement)
    - [Option 3 : Développement local avec Python](#option-3--développement-local-avec-python)
  - [Structure du projet](#structure-du-projet)
  - [Démarrage de l'application](#démarrage-de-lapplication)
    - [Avec VS Code Dev Containers](#avec-vs-code-dev-containers)
    - [Avec Docker Compose](#avec-docker-compose)
    - [Sans Docker (en local)](#sans-docker-en-local)
  - [Workflow de développement](#workflow-de-développement)
    - [Avec VS Code](#avec-vs-code)
    - [Avec un autre éditeur](#avec-un-autre-éditeur)
  - [Exécution des tests](#exécution-des-tests)
    - [Avec VS Code Dev Containers](#avec-vs-code-dev-containers-1)
    - [Avec Docker Compose](#avec-docker-compose-1)
    - [En local](#en-local)
  - [Documentation API](#documentation-api)
  - [Contribution au projet](#contribution-au-projet)
  - [Dépannage](#dépannage)
    - [Problèmes courants](#problèmes-courants)
      - [VS Code et Dev Containers](#vs-code-et-dev-containers)
      - [Docker et déploiement](#docker-et-déploiement)
    - [Commandes utiles](#commandes-utiles)
      - [Docker Compose](#docker-compose)
      - [VS Code Dev Containers](#vs-code-dev-containers)
    - [Obtenir de l'aide](#obtenir-de-laide)

## Accès à pgAdmin

Le projet inclut pgAdmin4 pour gérer la base de données PostgreSQL. Voici comment y accéder :

1. **Démarrez les conteneurs** :
   ```bash
   docker-compose up -d
   ```

2. **Accédez à pgAdmin** dans votre navigateur :
   - URL : http://localhost:5050

3. **Connectez-vous à pgAdmin** :
   - Email : admin@hetic.eu
   - Mot de passe : admin

4. **Connectez-vous au serveur de base de données** :
   - Le serveur est pré-configuré et devrait apparaître automatiquement
   - Si vous devez le configurer manuellement :
     - Host : db
     - Port : 5432
     - Maintenance database : mobile_musician
     - Username : postgres
     - Password : postgres

5. **Navigation dans pgAdmin** :
   Pour accéder aux tables de la base de données, suivez cette arborescence dans le panneau de gauche :
   ```
   Servers
   └── Mobile Musician DB
       └── Databases
           └── mobile_musician
               └── Schemas
                   └── public
                       └── Tables
   ```
   
   Vous pouvez alors :
   - Voir la structure des tables en cliquant sur une table
   - Exécuter des requêtes SQL en utilisant l'outil "Query Tool" (icône avec un symbole SQL)
   - Gérer les données (insérer, modifier, supprimer) via l'interface graphique
   - Exporter/importer des données

## Prérequis

Pour tous les environnements de développement :
- [Git](https://git-scm.com/downloads) (version 2.30.0 ou supérieure)
- [Docker](https://www.docker.com/products/docker-desktop) (version 20.10.0 ou supérieure)
- [Docker Compose](https://docs.docker.com/compose/install/) (généralement inclus avec Docker Desktop)

Pour l'environnement VS Code :
- [Visual Studio Code](https://code.visualstudio.com/) (version la plus récente)
- Extension VS Code : [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)

## Clonage du projet

Pour cloner le projet, exécutez la commande suivante dans votre terminal :

```bash
git clone https://github.com/joelkemkeng/event_connect_back_end_api_python.git
cd event_connect_back_end_api_python
```

## Configuration de l'environnement

### Option 1 : Avec VS Code et Dev Containers

1. **Installez l'extension Remote Development dans VS Code** :
   - Ouvrez VS Code
   - Allez dans l'onglet Extensions (Ctrl+Shift+X)
   - Recherchez "Remote Development"
   - Installez l'extension de Microsoft

2. **Ouvrez le projet dans VS Code** :
   ```bash
   code .
   ```

3. **Démarrez le Dev Container** :
   - Une notification devrait apparaître vous proposant d'ouvrir le projet dans un conteneur
   - Cliquez sur "Reopen in Container"
   - Ou utilisez la commande VS Code (F1) : "Remote-Containers: Reopen in Container"

Le conteneur va se construire automatiquement avec toutes les dépendances nécessaires définies dans le fichier `.devcontainer/devcontainer.json`.

### Option 2 : Sans VS Code (Docker uniquement)

1. **Créez une copie du fichier d'environnement** :
   ```bash
   cp backend/.env.example backend/.env
   ```

2. **Modifiez les variables d'environnement si nécessaire** :
   ```bash
   # Utilisez votre éditeur préféré
   nano backend/.env
   ```

3. **Construisez et démarrez les conteneurs** :
   ```bash
   docker-compose up --build
   ```

4. **Pour exécuter en arrière-plan** :
   ```bash
   docker-compose up -d
   ```

5. **Pour voir les logs quand l'application tourne en arrière-plan** :
   ```bash
   docker-compose logs -f
   ```

### Option 3 : Développement local avec Python

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

## Structure du projet

```
event_connect_back_end_api_python/
├── .devcontainer/                # Configuration Dev Container
│   ├── devcontainer.json        # Configuration VS Code et conteneur
│   └── docker-compose.yml       # Configuration des services Dev Container
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
│   ├── tests/                  # Tests unitaires et d'intégration
│   ├── .env.example            # Exemple de fichier d'environnement
│   └── requirements.txt        # Dépendances Python
├── docker-compose.yml          # Configuration Docker Compose principale
└── Dockerfile.backend          # Dockerfile pour le service backend
```

## Démarrage de l'application

### Avec VS Code Dev Containers
Une fois le conteneur démarré, vous pouvez lancer l'application depuis le terminal intégré de VS Code :
```bash
cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

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

### Avec VS Code
- Le code est automatiquement formaté à la sauvegarde
- Les imports sont automatiquement organisés
- La vérification des types est active
- Les suggestions de Copilot sont disponibles (si installé)

### Avec un autre éditeur
Utilisez les outils de formatage et de linting manuellement :
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

### Avec VS Code Dev Containers
```bash
cd backend && pytest
```

### Avec Docker Compose
```bash
docker-compose exec api pytest
```

### En local
```bash
cd backend
pytest
```

Avec couverture de code :
```bash
pytest --cov=app
```

## Documentation API

Une fois l'application démarrée, la documentation de l'API est accessible aux URLs suivantes :

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc
- **RapiDoc** : http://localhost:8000/rapidoc

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

#### VS Code et Dev Containers
1. **VS Code ne détecte pas le Dev Container** :
   - Vérifiez que l'extension Remote Development est installée
   - Redémarrez VS Code
   - Assurez-vous que Docker Desktop est en cours d'exécution

2. **Le conteneur ne se construit pas** :
   - Vérifiez les logs Docker
   - Assurez-vous que Docker Desktop a suffisamment de ressources
   - Essayez de reconstruire avec : "Remote-Containers: Rebuild Container"

#### Docker et déploiement
1. **L'application ne démarre pas** :
   ```bash
   # Vérifiez les logs Docker
   docker-compose logs
   
   # Vérifiez si les containers sont en cours d'exécution
   docker-compose ps
   ```

2. **Problèmes d'importation de modules Python** :
   - Si vous rencontrez des erreurs du type "No module named 'app'", assurez-vous d'exécuter les commandes depuis le bon répertoire
   - Pour les commandes uvicorn, exécutez-les depuis le répertoire `backend`
   - Pour Docker Compose, la commande correcte est configurée dans le fichier docker-compose.yml

3. **Erreurs de base de données** :
   ```bash
   # Réinitialisez la base de données
   docker-compose down -v
   docker-compose up -d
   ```

4. **Problèmes de permissions** :
   - Le conteneur s'exécute en tant que root par défaut
   - Si vous rencontrez des problèmes, vérifiez les permissions des fichiers

### Commandes utiles

#### Docker Compose
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

#### VS Code Dev Containers
- F1 → "Remote-Containers: Rebuild Container" : Reconstruire le conteneur
- F1 → "Remote-Containers: Reopen in Container" : Rouvrir dans le conteneur
- F1 → "Remote-Containers: Open Container Configuration File" : Modifier la configuration

### Obtenir de l'aide

Si vous rencontrez des problèmes :

1. Consultez les [issues](https://github.com/joelkemkeng/event_connect_back_end_api_python/issues) existantes
2. Créez une nouvelle issue avec :
   - Description détaillée du problème
   - Logs d'erreur
   - Étapes pour reproduire
   - Configuration de votre environnement (OS, versions de Docker, etc.)
