● Voici la liste des fonctionnalités demandées dans le cadre du projet
  TuneLink/Mobile Musician, regroupées par domaine fonctionnel:

  1. Gestion des Utilisateurs

  - Inscription: Création de compte utilisateur avec nom d'utilisateur unique, email,
   et mot de passe sécurisé
  - Connexion: Authentification utilisateur avec génération de token JWT
  - Déconnexion: Invalidation du token et terminaison de session
  - Mise à jour du profil: Modification des informations personnelles (photo, bio,
  localisation)
  - Suppression de compte: Désactivation ou suppression physique du compte
  - Changement de mot de passe: Modification sécurisée du mot de passe
  - Récupération du profil: Obtention des informations du profil utilisateur
  - Gestion des instruments: Association d'instruments avec niveau de compétence
  - Gestion des genres musicaux: Association de genres musicaux préférés

  2. Gestion des Événements

  - Création d'événement: Organisation d'événements musicaux avec titre, description,
   date, lieu
  - Mise à jour d'événement: Modification des détails d'un événement par son créateur
  - Annulation d'événement: Suppression d'un événement avec notification aux
  participants
  - Récupération des participants: Obtention de la liste des musiciens inscrits à un
  événement
  - Détails d'un événement: Consultation des informations complètes d'un événement
  - Recherche d'événements: Par lieu (géolocalisation), date ou type d'événement
  - Inscription à un événement: Participation à un événement avec l'instrument choisi
  - Gestion des participations: Modification ou annulation de participation
  - Gestion des instruments requis: Définition des instruments nécessaires pour un
  événement

  3. Système de Messagerie

  - Création de conversation: Initialisation de discussions entre utilisateurs
  - Récupération des messages: Obtention de l'historique des messages d'une
  conversation
  - Récupération des participants: Liste des utilisateurs d'une conversation
  - Ajout/Suppression de participants: Gestion des membres d'une conversation
  - Envoi de message: Communication dans une conversation existante
  - Gestion des messages: Marquage comme lu, suppression, consultation des détails

  4. Système de Notifications

  - Création de notification: Génération d'alertes pour les utilisateurs
  - Gestion des notifications: Marquage comme lu, suppression, consultation des
  détails

  5. Données de Référence

  - Gestion des instruments: Catalogue d'instruments (création, mise à jour,
  suppression)
  - Gestion des genres: Catalogue de genres musicaux (création, mise à jour,
  suppression)

  Caractéristiques techniques clés

  - Architecture API RESTful avec FastAPI
  - Authentification via JWT
  - Base de données PostgreSQL avec SQLAlchemy ORM
  - Documentation API complète avec OpenAPI/Swagger
  - Validation des données via Pydantic
  - Réponses API normalisées avec format standard
  - Gestion des relations entre entités avec SQLAlchemy
  - Tests unitaires et fonctionnels

  Le projet vise à créer une plateforme où les musiciens peuvent se connecter,
  trouver des événements musicaux à proximité, s'inscrire à ces événements avec
  l'instrument qu'ils souhaitent jouer, et communiquer avec d'autres musiciens via un
   système de messagerie.