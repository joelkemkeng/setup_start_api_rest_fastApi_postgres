#!/bin/bash

# Création du dossier static s'il n'existe pas
mkdir -p static

# Version de Swagger UI à utiliser
SWAGGER_VERSION="4.15.5"

# Téléchargement des fichiers Swagger UI
wget -O static/swagger-ui-bundle.js https://cdn.jsdelivr.net/npm/swagger-ui-dist@$SWAGGER_VERSION/swagger-ui-bundle.js
wget -O static/swagger-ui.css https://cdn.jsdelivr.net/npm/swagger-ui-dist@$SWAGGER_VERSION/swagger-ui.css
wget -O static/swagger-ui-standalone-preset.js https://cdn.jsdelivr.net/npm/swagger-ui-dist@$SWAGGER_VERSION/swagger-ui-standalone-preset.js

# Téléchargement de ReDoc
wget -O static/redoc.standalone.js https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js

# Téléchargement des icônes et images
wget -O static/favicon.png https://fastapi.tiangolo.com/img/favicon.png
wget -O static/logo.png https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png

echo "Téléchargement des fichiers statiques terminé !" 