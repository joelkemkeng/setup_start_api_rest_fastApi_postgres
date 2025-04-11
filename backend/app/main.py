# Fichier principal - Point d'entrée de l'application FastAPI
from typing import Any, Dict

# Imports FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles





# import outils dependance reseau
from fastapi import FastAPI, Request, status
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse





# Imports de nos modules
from app.api.router import api_router
from app.config import settings






# pour le middleware
from app.middlewares.normalized_response import NormalizedResponseMiddleware




#############################################
# pour le status code
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.common import StatusCode
#####################################################
 












#########################################################
# Création de l'instance de l'application FastAPI
#########################################################
app = FastAPI(
    title="Mobile Musician API",
    description="""
                # API Mobile Musician 🎵

                API pour l'application Mobile Musician - Mise en relation de musiciens.

                ## Fonctionnalités

                ### Utilisateurs 👤

                * **Inscription** : Créer un nouveau compte
                * **Connexion** : Authentification sécurisée
                * **Profil** : Gérer les informations personnelles
                * **Préférences** : Instruments et genres musicaux

                ### Événements 🎪

                * **Création** : Organiser des événements musicaux
                * **Recherche** : Trouver des événements par lieu/date
                * **Participation** : Rejoindre des événements
                * **Filtres** : Par type, genre musical, etc.

                ### Messagerie 💬

                * **Conversations** : Échanger avec d'autres musiciens
                * **Notifications** : Alertes pour nouveaux messages
                * **Groupes** : Discussions pour les événements

                ### Géolocalisation 🗺️

                * **Proximité** : Trouver des musiciens proches
                * **Carte** : Visualiser les événements
                * **Filtres** : Par distance et disponibilité
    """,
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url="/openapi.json",
)

#########################################################







#########################################################
# Configuration des CORS
#########################################################
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
#########################################################






#########################################################
# Montage des fichiers statiques
#########################################################
app.mount("/static", StaticFiles(directory="static"), name="static")
#########################################################





#########################################################
# Inclusion des routes API endpoint
#########################################################
app.include_router(api_router, prefix="/api/v1")
#########################################################






#########################################################
# Routes pour la documentation Swagger UI
#########################################################
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html() -> Any:
    """
    Route personnalisée pour la documentation Swagger UI.
    """
    html_content = get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - Documentation Swagger",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5.11.0/swagger-ui.css",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "docExpansion": "list",  # Changé pour une meilleure vue initiale
            "filter": True,
            "tryItOutEnabled": True,
            "persistAuthorization": True,
            "displayOperationId": False,
            "withCredentials": True,
            "defaultModelRendering": "example",
            "syntaxHighlight": {
                "activate": True,
                "theme": "monokai"
            },
            "operationsSorter": "method",
            "tagsSorter": "alpha",
            "requestSnippetsEnabled": True,
            "tryItOutEnabled": True
        },
    )
    
    # Ajouter les liens vers les autres documentations
    html_str = html_content.body.decode("utf-8")
    doc_links_html = '''
    <div style="position: absolute; top: 100px; right: 50px; z-index: 1000; display: flex; gap: 30px;">
        <a href="/rapidoc" style="color: white; text-decoration: none; font-weight: bold; font-size: 25px; padding: 5px 10px; border-radius: 4px; background-color: #60d22c;">RapiDoc</a>
        <a href="/redoc" style="color: white; text-decoration: none; font-weight: bold; font-size: 25px; padding: 5px 10px; border-radius: 4px; background-color: #3033e8;">ReDoc</a>
    </div>
    '''
    modified_html = html_str.replace("<body>", f"<body>\n{doc_links_html}")
    
    # Retourner la page HTML modifiée
    return HTMLResponse(content=modified_html)

####################################################







####################################################
# Routes pour la documentation redoc
####################################################
@app.get("/redoc", include_in_schema=False)
async def redoc_html() -> Any:
    """Route pour la documentation ReDoc."""
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=f"{app.title} - Documentation ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
        redoc_favicon_url="/static/favicon.png",
    )

####################################################








####################################################
# Routes pour la documentation RapiDoc
####################################################
@app.get("/rapidoc", include_in_schema=False)
async def rapidoc_html() -> HTMLResponse:
    """Route pour la documentation RapiDoc."""
    return HTMLResponse(
        """
        <!doctype html>
        <html>
        <head>
            <meta charset="utf-8">
            <script type="module" src="https://unpkg.com/rapidoc/dist/rapidoc-min.js"></script>
            <link rel="icon" type="image/png" href="/static/favicon.png"/>
            <title>Mobile Musician API - Documentation RapiDoc</title>
            <style>
                rapi-doc {
                    width: 100%;
                    height: 100vh;
                    display: flex;
                }
            </style>
        </head>
        <body>
            <rapi-doc
                spec-url="/openapi.json"
                theme="dark"
                bg-color="#1a1a1a"
                text-color="#fafafa"
                primary-color="#00ff00"
                render-style="read"
                show-header="false"
                show-info="true"
                allow-authentication="true"
                allow-try="true"
            > </rapi-doc>
        </body>
        </html>
        """
    )

####################################################









####################################################
# Route racine - accessible à l'URL de base de l'API
####################################################
@app.get("/", tags=["Informations"])
async def root() -> Dict[str, str]:
    """
    Page d'accueil de l'API Mobile Musician.
    """
    return {
        "message": "Bienvenue sur l'API Mobile Musician",
        "documentation": "/docs",
        "rapidoc": "/rapidoc",
        "redoc": "/redoc",
        "github": "https://github.com/joelkemkeng/event_connect_back_end_api_python",
    }
####################################################








####################################################
# Personnalisation du schéma OpenAPI
####################################################
def custom_openapi() -> Dict[str, Any]:
    
    
    """Personnalisation du schéma OpenAPI avec nos définitions de composants."""
    # Obtenir le schéma OpenAPI
    schema = getattr(app, "openapi_schema", None)
    
    # Si le schéma existe, le retourner
    if schema is not None:
        return dict(schema)

    # Obtenir le schéma OpenAPI
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Ajout de la version OpenAPI
    openapi_schema["openapi"] = "3.0.2"

    # S'assurer que la section components existe
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    
    # S'assurer que la section schemas existe
    if "schemas" not in openapi_schema["components"]:
        openapi_schema["components"]["schemas"] = {}
        

    # Ajouter le schéma de statut
    openapi_schema["components"]["schemas"]["StatusCode"] = {
        "type": "string",
        "enum": ["success", "error", "warning", "info"],
        "description": "Statut de la réponse API"
    }
    
    # Ajouter le schéma de réponse standard
    openapi_schema["components"]["schemas"]["StandardResponse"] = {
        "type": "object",
        "properties": {
            "status": {
                "$ref": "#/components/schemas/StatusCode"
            },
            "code": {
                "type": "integer",
                "description": "Code HTTP de la réponse"
            },
            "message": {
                "type": "string",
                "description": "Message descriptif de la réponse"
            },
            "data": {
                "type": "object",
                "nullable": True,
                "description": "Données de la réponse (si succès)"
            },
            "errors": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "field": {
                            "type": "string",
                            "description": "Champ concerné par l'erreur"
                        },
                        "message": {
                            "type": "string",
                            "description": "Description de l'erreur"
                        },
                        "type": {
                            "type": "string",
                            "description": "Type d'erreur"
                        }
                    }
                },
                "nullable": True,
                "description": "Liste des erreurs (si échec)"
            }
        },
        "required": ["status", "code", "message"]
    }
    
    # Ajouter la sécurité JWT
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": f"Entrez votre token JWT ici. Clé secrète (dev): {settings.SECRET_KEY}",
        }
    }
    
    # Ajouter la réponse pour les erreurs d'authentification
    openapi_schema["components"]["responses"] = {
        "UnauthorizedError": {
            "description": "Token d'accès manquant ou invalide",
            "content": {
                "application/json": {
                    "schema": {
                        "allOf": [
                            {"$ref": "#/components/schemas/StandardResponse"},
                            {
                                "example": {
                                    "status": "error",
                                    "code": 401,
                                    "message": "Non autorisé - Token invalide ou expiré",
                                    "data": None,
                                    "errors": [{"message": "Token JWT invalide ou expiré"}]
                                }
                            }
                        ]
                    }
                }
            }
        }
    }

    # Ajouter la sécurité JWT globalement pour tous les endpoints
    openapi_schema["security"] = [{"bearerAuth": []}]
    
    # Définir explicitement les routes qui nécessitent ou non l'authentification
    if "paths" in openapi_schema:
        # 1. D'abord, définir certaines routes comme publiques (pas d'authentification requise)
        for path in openapi_schema["paths"]:
            # Routes d'authentification et d'inscription publiques
            if path.endswith("/auth/login") or path.endswith("/users/register"):
                for method in openapi_schema["paths"][path]:
                    openapi_schema["paths"][path][method]["security"] = []
            
            # Route de profil public (accessible sans authentification)
            elif "/users/profile/" in path:
                for method in openapi_schema["paths"][path]:
                    openapi_schema["paths"][path][method]["security"] = []
            
            # 2. Ensuite, forcer l'authentification sur les endpoints protégés
            elif path.endswith("/users/me") or path.endswith("/users/me/instruments") or path.endswith("/users/me/genres") or path.endswith("/auth/logout"):
                for method in openapi_schema["paths"][path]:
                    openapi_schema["paths"][path][method]["security"] = [{"bearerAuth": []}]

    # Ajouter le schéma OpenAPI à l'instance de l'application
    app.openapi_schema = openapi_schema
    
    # Retourner le schéma OpenAPI
    return openapi_schema

####################################################








####################################################
# Après les autres middlewares
####################################################
app.add_middleware(NormalizedResponseMiddleware)
####################################################













#####################################################
# pour le status code
#####################################################

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Gère les exceptions HTTP avec notre format de réponse normalisé."""
    # Vérifier si l'exception a déjà un détail normalisé
    if isinstance(exc.detail, dict) and "status" in exc.detail and "code" in exc.detail:
        return JSONResponse(
            content=exc.detail,
            status_code=exc.status_code,
            headers=exc.headers
        )
    
    # Normaliser la réponse d'erreur
    content = {
        "status": StatusCode.ERROR,
        "code": exc.status_code,
        "message": str(exc.detail),
        "data": None,
        "meta": None,
        "errors": None
    }
    
    return JSONResponse(
        content=content,
        status_code=exc.status_code,
        headers=exc.headers
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Gère les erreurs de validation Pydantic avec notre format normalisé."""
    # Formater les erreurs de validation
    errors = []
    for error in exc.errors():
        location = error.get("loc", [])
        field = location[-1] if len(location) > 0 else "unknown"
        error_type = error.get("type", "")
        
        errors.append({
            "field": field,
            "type": error_type,
            "message": error.get("msg", "Erreur de validation")
        })
    
    content = {
        "status": StatusCode.ERROR,
        "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "message": "Erreur de validation des données",
        "data": None,
        "meta": None,
        "errors": errors
    }
    
    return JSONResponse(
        content=content,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )

#####################################################
# FIN pour le status code
#####################################################















app.openapi = custom_openapi