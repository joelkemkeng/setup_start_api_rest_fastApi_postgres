
```markdown
# TuneLink Backend

Ce README fournit des instructions détaillées pour cloner, déployer et développer le projet TuneLink Backend à l'aide de VS Code et des Dev Containers.

## Table des matières

- [Prérequis](#prérequis)
- [Clonage du projet](#clonage-du-projet)
- [Configuration de l'environnement de développement](#configuration-de-lenvironnement-de-développement)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [Développement avec Dev Containers](#développement-avec-dev-containers)
- [Structure du projet](#structure-du-projet)
- [Workflow de développement](#workflow-de-développement)
- [Documentation API](#documentation-api)
- [Dépannage](#dépannage)

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les outils suivants :

- [Git](https://git-scm.com/downloads) (version 2.30.0 ou supérieure)
- [Visual Studio Code](https://code.visualstudio.com/) (version la plus récente)
- [Docker Desktop](https://www.docker.com/products/docker-desktop) (version 20.10.0 ou supérieure)
- Extension VS Code : [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)

## Clonage du projet

Pour cloner le projet, exécutez la commande suivante dans votre terminal :

```bash
git clone https://github.com/joelkemkeng/event_connect_back_end_api_python.git
cd event_connect_back_end_api_python
```

## Configuration de l'environnement de développement

### Pour tous les systèmes d'exploitation

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

## Structure du projet

```
event_connect_back_end_api_python/  # Répertoire racine du projet après clonage
├── .devcontainer/                # Configuration Dev Container
│   ├── devcontainer.json        # Configuration VS Code et conteneur
│   └── docker-compose.yml       # Configuration des services
├── backend/                     # Code source du backend
│   ├── app/                    
│   │   ├── api/                # Endpoints de l'API
│   │   ├── core/              # Configuration et utilitaires
│   │   ├── db/                # Modèles et migrations de base de données
│   │   ├── models/            # Modèles Pydantic
│   │   ├── schemas/           # Schémas de validation
│   │   └── services/          # Logique métier
│   ├── docs/                  # Documentation
│   ├── scripts/               # Scripts utilitaires
│   ├── static/               # Fichiers statiques
│   ├── tests/                # Tests unitaires et d'intégration
│   ├── .env.example          # Exemple de fichier d'environnement
│   └── requirements.txt      # Dépendances Python
├── Dockerfile.backend        # Dockerfile pour le backend
└── docker-compose.yml        # Configuration Docker Compose racine
```

## Développement avec Dev Containers

Le projet utilise VS Code Dev Containers, ce qui signifie que tout l'environnement de développement est conteneurisé et configuré automatiquement.

### Fonctionnalités préconfigurées

- **Linting et formatage** :
  - Black pour le formatage de code
  - Flake8 pour le linting
  - isort pour l'organisation des imports
  - mypy pour la vérification des types

- **Extensions VS Code** :
  - Support Python
  - Pylance pour l'analyse de code
  - Docker
  - GitHub Copilot
  - Support Markdown

### Workflow de développement

1. **Démarrage du développement** :
   - Ouvrez VS Code
   - Ouvrez le dossier du projet (répertoire racine après clonage)
   - VS Code détectera automatiquement la configuration Dev Container
   - Cliquez sur "Reopen in Container" quand proposé

2. **Modifications du code** :
   - Le code est automatiquement formaté à la sauvegarde
   - Les imports sont automatiquement organisés
   - La vérification des types est active
   - Les suggestions de Copilot sont disponibles

3. **Exécution de l'application** :
   Pour lancer l'application depuis le répertoire racine :
   ```bash
   cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   Ou en utilisant Docker Compose (depuis le répertoire racine) :
   ```bash
   docker-compose up
   ```

4. **Exécution des tests** :
   ```bash
   cd backend && pytest
   ```

## Documentation API

L'API est documentée automatiquement et accessible via :

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc
- **RapiDoc** : http://localhost:8000/rapidoc

## Dépannage

### Problèmes courants

1. **VS Code ne détecte pas le Dev Container** :
   - Vérifiez que l'extension Remote Development est installée
   - Redémarrez VS Code
   - Assurez-vous que Docker Desktop est en cours d'exécution

2. **Le conteneur ne se construit pas** :
   - Vérifiez les logs Docker
   - Assurez-vous que Docker Desktop a suffisamment de ressources
   - Essayez de reconstruire avec : "Remote-Containers: Rebuild Container"

3. **Problèmes d'importation des modules Python** :
   - Si vous rencontrez des erreurs du type "No module named 'app'", assurez-vous d'exécuter les commandes depuis le bon répertoire
   - Pour les commandes uvicorn, exécutez-les depuis le répertoire `backend`
   - Pour Docker Compose, la commande correcte est configurée dans le fichier docker-compose.yml

4. **Problèmes de permissions** :
   - Le conteneur s'exécute en tant que root par défaut
   - Si vous rencontrez des problèmes, vérifiez les permissions des fichiers

### Obtenir de l'aide

Si vous rencontrez des problèmes :

1. Consultez les [issues](https://github.com/joelkemkeng/event_connect_back_end_api_python/issues) existantes
2. Créez une nouvelle issue avec :
   - Description détaillée du problème
   - Logs d'erreur
   - Étapes pour reproduire
   - Configuration de votre environnement
```

