# Mobile Musician App - Spécifications Backend

Ce document détaille les fonctionnalités et sous-fonctionnalités à implémenter côté backend pour l'application *Mobile Musician App*, un projet réalisé dans le cadre d'un travail d'équipe de 5 jours à HETIC. Le backend est au cœur du système, gérant les utilisateurs, les événements, la messagerie, les notifications et les données de référence, tout en respectant des contraintes strictes de sécurité, de documentation et de déploiement. L'objectif est de fournir une API robuste, sécurisée et bien documentée, intégrable avec une application mobile (développée en React Native ou autre technologie mobile).

---

## Contexte Général

### Présentation
L'application *Mobile Musician App* vise à connecter des musiciens en leur permettant de :
- S'inscrire et se connecter à la plateforme.
- Créer et participer à des événements musicaux (jams, concerts, répétitions).
- Échanger des messages en direct ou en groupe.
- Utiliser une géolocalisation pour repérer les événements à proximité.
Le backend doit fournir une API RESTful pour gérer ces interactions, avec une base de données pour stocker les données et des mécanismes sécurisés pour l'authentification et la gestion des sessions.

### Contraintes Techniques
- **Technologie Backend** : FastAPI (choisi pour sa rapidité, sa simplicité et son support natif des API asynchrones) ou Symfony.
- **ORM** : Utilisation recommandée d'un ORM (SQLAlchemy pour FastAPI) pour gérer les données.
- **Sécurité** : Authentification via JWT, validation des entrées, protection contre les injections SQL, XSS, et CSRF.
- **Versionnage** : Gestion via GitHub/GitLab avec GitFlow (branches par fonctionnalité, Pull Requests).
- **Containerisation** : Utilisation de Docker pour encapsuler le backend et la base de données.
- **Documentation** : Code commenté et documentation complète des endpoints et processus.
- **Délais** : Prototype fonctionnel à présenter dans 5 jours, avec une gestion rigoureuse des tâches.

### Objectifs Backend
- Fournir une API fonctionnelle pour les fonctionnalités de base (inscription, messagerie, événements).
- Assurer une intégration fluide avec l'application mobile.
- Respecter les normes de sécurité et les bonnes pratiques de développement.

---

## Fonctionnalités et Sous-Fonctionnalités Backend

### 1. Gestion des Utilisateurs
#### Contexte
Les musiciens doivent pouvoir s'inscrire, se connecter, gérer leur profil, leurs compétences (instruments joués), et leurs préférences musicales (genres). Cette fonctionnalité est essentielle pour identifier les utilisateurs et personnaliser leur expérience.

#### Besoins Fonctionnels
1. **Inscription (Utilisateur.s_inscrire)**
   - **Description** : Permet à un nouvel utilisateur de créer un compte.
   - **Entrées** : `nom_utilisateur`, `email`, `mot_de_passe`.
   - **Sortie** : Statut de succès (booléen) et création d’un utilisateur dans la base.
   - **Sous-Fonctionnalités** :
     - Validation de l’unicité de `nom_utilisateur` et `email`.
     - Hachage sécurisé du mot de passe (ex. : bcrypt).
     - Génération d’un `id` UUID unique.
     - Initialisation des attributs (`latitude`, `longitude`, etc.) avec des valeurs par défaut si non fournies.
   - **Bonne Pratique** : Validation des entrées (taille, format email), protection contre les injections SQL via ORM.

2. **Connexion (Utilisateur.connexion)**
   - **Description** : Authentifie un utilisateur et génère un token JWT.
   - **Entrées** : `email`, `mot_de_passe`.
   - **Sortie** : Token JWT (chaîne).
   - **Sous-Fonctionnalités** :
     - Vérification des identifiants (email/mot de passe).
     - Mise à jour de `derniere_connexion`.
     - Génération d’un token JWT avec expiration (ex. : 24h).
   - **Bonne Pratique** : Utilisation de JWT signé avec une clé secrète, stockage sécurisé du secret.

3. **Déconnexion (Utilisateur.deconnexion)**
   - **Description** : Invalide la session active de l’utilisateur.
   - **Entrées** : Token JWT.
   - **Sortie** : Statut de succès (booléen).
   - **Sous-Fonctionnalités** :
     - Vérification de la validité du token.
     - Suppression ou invalidation du token côté serveur (ex. : liste noire).
   - **Bonne Pratique** : Gestion sécurisée des tokens pour éviter leur réutilisation.

4. **Mise à jour du profil (Utilisateur.maj_profil)**
   - **Description** : Permet à l’utilisateur de modifier ses informations.
   - **Entrées** : `photo_profil`, `biographie`, `latitude`, `longitude`.
   - **Sortie** : Statut de succès (booléen).
   - **Sous-Fonctionnalités** :
     - Validation des nouvelles données (ex. : format URL pour `photo_profil`).
     - Mise à jour partielle (seuls les champs fournis sont modifiés).
   - **Bonne Pratique** : Autorisation via JWT, journalisation des modifications.

5. **Suppression du compte (Utilisateur.supprimer_compte)**
   - **Description** : Supprime définitivement le compte de l’utilisateur.
   - **Entrées** : Token JWT.
   - **Sortie** : Statut de succès (booléen).
   - **Sous-Fonctionnalités** :
     - Désactivation (`actif = False`) ou suppression physique selon les besoins.
     - Suppression des données associées (instruments, genres, participations).
   - **Bonne Pratique** : Confirmation sécurisée avant suppression, respect RGPD.

6. **Changement de mot de passe (Utilisateur.changer_mot_de_passe)**
   - **Description** : Permet à l’utilisateur de modifier son mot de passe.
   - **Entrées** : Ancien mot de passe, nouveau mot de passe, token JWT.
   - **Sortie** : Statut de succès (booléen).
   - **Sous-Fonctionnalités** :
     - Vérification de l’ancien mot de passe.
     - Hachage du nouveau mot de passe.
   - **Bonne Pratique** : Validation de la complexité du mot de passe, sécurisation via HTTPS.

7. **Récupération du profil (Utilisateur.obtenir_profil)**
   - **Description** : Retourne les informations du profil de l’utilisateur.
   - **Entrées** : Token JWT.
   - **Sortie** : Dictionnaire avec les attributs de l’utilisateur.
   - **Sous-Fonctionnalités** :
     - Inclusion des instruments et genres associés via requêtes jointes.
   - **Bonne Pratique** : Limitation des données sensibles exposées (ex. : pas de mot de passe).

8. **Gestion des instruments (UtilisateurInstrument)**
   - **Description** : Associe des instruments à un utilisateur avec un niveau de compétence.
   - **Sous-Fonctionnalités** :
     - `ajouter()` : Ajoute un instrument (`instrument_id`, `niveau`).
     - `maj_niveau()` : Met à jour le niveau de compétence.
     - `supprimer()` : Retire un instrument.
   - **Bonne Pratique** : Vérification de l’existence de `instrument_id` dans le catalogue.

9. **Gestion des genres (UtilisateurGenre)**
   - **Description** : Associe des genres musicaux préférés à un utilisateur.
   - **Sous-Fonctionnalités** :
     - `ajouter()` : Ajoute un genre (`genre_id`).
     - `supprimer()` : Retire un genre.
   - **Bonne Pratique** : Vérification de l’existence de `genre_id` dans le catalogue.

---

### 2. Gestion des Événements
#### Contexte
Les utilisateurs doivent pouvoir créer, gérer et participer à des événements musicaux, avec une recherche basée sur la localisation, la date ou le type d’événement. Le backend doit gérer les données des événements et leurs participants.

#### Besoins Fonctionnels
1. **Création d’un événement (Evenement.creer)**
   - **Description** : Permet à un utilisateur de créer un événement musical.
   - **Entrées** : `titre`, `description`, `date_debut`, `date_fin`, `latitude`, `longitude`, `adresse`, `type`, `capacite_max`, `url_image`.
   - **Sortie** : Statut de succès (booléen).
   - **Sous-Fonctionnalités** :
     - Attribution de `createur_id` à l’utilisateur authentifié.
     - Génération d’un `id` UUID.
     - Validation des dates (`date_debut < date_fin`).
   - **Bonne Pratique** : Autorisation via JWT, validation des coordonnées géographiques.

2. **Mise à jour d’un événement (Evenement.mettre_a_jour)**
   - **Description** : Permet au créateur de modifier un événement.
   - **Entrées** : Champs modifiables, token JWT.
   - **Sortie** : Statut de succès (booléen).
   - **Sous-Fonctionnalités** :
     - Vérification que l’utilisateur est le créateur (`createur_id`).
     - Mise à jour partielle des champs.
   - **Bonne Pratique** : Journalisation des modifications, restriction aux créateurs.

3. **Annulation d’un événement (Evenement.annuler)**
   - **Description** : Annule un événement et notifie les participants.
   - **Entrées** : Token JWT.
   - **Sortie** : Statut de succès (booléen).
   - **Sous-Fonctionnalités** :
     - Mise à jour de `statut` à "annulé".
     - Création de notifications pour les participants.
   - **Bonne Pratique** : Vérification des autorisations, gestion des notifications.

4. **Récupération des participants (Evenement.obtenir_participants)**
   - **Description** : Retourne la liste des participants d’un événement.
   - **Entrées** : `evenement_id`, token JWT.
   - **Sortie** : Liste des utilisateurs participants.
   - **Sous-Fonctionnalités** :
     - Jointure avec *Participation* pour inclure les instruments joués.
   - **Bonne Pratique** : Pagination pour les grands événements.

5. **Détails d’un événement (Evenement.obtenir_details)**
   - **Description** : Retourne les informations complètes d’un événement.
   - **Entrées** : `evenement_id`.
   - **Sortie** : Dictionnaire avec tous les attributs.
   - **Sous-Fonctionnalités** :
     - Inclusion des instruments requis via *EvenementInstrument*.
   - **Bonne Pratique** : Cache pour les requêtes fréquentes.

6. **Recherche d’événements**
   - **recherche_par_lieu(lat, long, rayon)** :
     - **Description** : Recherche les événements dans un rayon géographique.
     - **Entrées** : Coordonnées (`lat`, `long`), rayon en km.
     - **Sortie** : Liste d’événements proches.
     - **Sous-Fonctionnalités** : Calcul de distance via formule de Haversine ou extension GIS (ex. : PostGIS).
   - **recherche_par_date(debut, fin)** :
     - **Description** : Recherche les événements dans une plage de dates.
     - **Entrées** : Dates de début et fin.
     - **Sortie** : Liste d’événements.
   - **recherche_par_type(type)** :
     - **Description** : Recherche les événements par type (ex. : jam).
     - **Entrées** : Type d’événement.
     - **Sortie** : Liste d’événements.
   - **Bonne Pratique** : Indexation des champs `latitude`, `longitude`, `date_debut` pour optimiser les recherches.

7. **Inscription à un événement (Participation.s_inscrire)**
   - **Description** : Permet à un utilisateur de s’inscrire à un événement.
   - **Entrées** : `evenement_id`, `instrument_id`, token JWT.
   - **Sortie** : Statut de succès (booléen).
   - **Sous-Fonctionnalités** :
     - Vérification de la capacité maximale (`capacite_max`).
     - Ajout dans *Participation* avec `statut` initial (ex. : "confirmé").
   - **Bonne Pratique** : Gestion des conflits (ex. : double inscription).

8. **Mise à jour de la participation (Participation.maj_statut)**
   - **Description** : Modifie le statut de la participation (ex. : annulé).
   - **Entrées** : `participation_id`, `statut`, token JWT.
   - **Sortie** : Statut de succès (booléen).
   - **Bonne Pratique** : Restriction à l’utilisateur concerné.

9. **Annulation de la participation (Participation.annuler)**
   - **Description** : Retire un utilisateur d’un événement.
   - **Entrées** : `participation_id`, token JWT.
   - **Sortie** : Statut de succès (booléen).
   - **Sous-Fonctionnalités** : Notification au créateur de l’événement.
   - **Bonne Pratique** : Vérification des autorisations.

10. **Gestion des instruments requis (EvenementInstrument)**
    - **Description** : Définit les instruments nécessaires pour un événement.
    - **Sous-Fonctionnalités** :
      - `ajouter()` : Ajoute un instrument requis.
      - `supprimer()` : Retire un instrument requis.
    - **Bonne Pratique** : Restriction au créateur de l’événement.

---

### 3. Système de Messagerie
#### Contexte
Les utilisateurs doivent pouvoir communiquer via des conversations individuelles ou de groupe pour coordonner leurs activités musicales.

#### Besoins Fonctionnels
1. **Création d’une conversation (Conversation.creer)**
   - **Description** : Initialise une nouvelle conversation entre utilisateurs.
   - **Entrées** : Liste d’`utilisateur_id`, token JWT.
   - **Sortie** : Statut de succès (booléen).
   - **Sous-Fonctionnalités** :
     - Ajout des participants dans *ConversationUtilisateur*.
     - Génération d’un `id` UUID.
   - **Bonne Pratique** : Vérification des utilisateurs existants.

2. **Récupération des messages (Conversation.obtenir_messages)**
   - **Description** : Retourne l’historique des messages d’une conversation.
   - **Entrées** : `conversation_id`, token JWT.
   - **Sortie** : Liste de messages.
   - **Sous-Fonctionnalités** : Pagination pour les longues conversations.
   - **Bonne Pratique** : Autorisation pour les participants uniquement.

3. **Récupération des participants (Conversation.obtenir_participants)**
   - **Description** : Liste les utilisateurs d’une conversation.
   - **Entrées** : `conversation_id`, token JWT.
   - **Sortie** : Liste d’utilisateurs.
   - **Bonne Pratique** : Restriction aux membres de la conversation.

4. **Ajout/Suppression de participants**
   - **ajouter_participant(id)** : Ajoute un utilisateur à la conversation.
   - **supprimer_participant(id)** : Retire un utilisateur.
   - **Bonne Pratique** : Autorisation pour les créateurs ou gestion par rôle.

5. **Envoi d’un message (Message.envoyer)**
   - **Description** : Envoie un message dans une conversation.
   - **Entrées** : `conversation_id`, `contenu`, token JWT.
   - **Sortie** : Statut de succès (booléen).
   - **Sous-Fonctionnalités** :
     - Mise à jour de `dernier_message` dans *Conversation*.
     - Création de notifications pour les participants.
   - **Bonne Pratique** : Validation du contenu (longueur max, filtres XSS).

6. **Gestion des messages**
   - **marquer_comme_lu()** : Met à jour le statut d’un message à "lu".
   - **supprimer()** : Supprime un message.
   - **obtenir_details()** : Retourne les détails d’un message.
   - **Bonne Pratique** : Restriction aux expéditeurs/destinataires.

---

### 4. Système de Notifications
#### Contexte
Les utilisateurs doivent être alertés des actions importantes (nouveaux messages, changements d’événements, participations).

#### Besoins Fonctionnels
1. **Création d’une notification (Notification.creer)**
   - **Description** : Génère une notification pour un utilisateur.
   - **Entrées** : `utilisateur_id`, `type`, `contenu`, `reference_id`.
   - **Sortie** : Statut de succès (booléen).
   - **Sous-Fonctionnalités** :
     - Génération d’un `id` UUID.
     - Statut initialisé à "non lue".
   - **Bonne Pratique** : Déclenchement automatique (ex. : via événements système).

2. **Gestion des notifications**
   - **marquer_comme_lu()** : Met à jour le statut à "lue".
   - **supprimer()** : Supprime une notification.
   - **obtenir_details()** : Retourne les détails d’une notification.
   - **Bonne Pratique** : Pagination pour la liste des notifications.

---

### 5. Données de Référence
#### Contexte
Un catalogue d’instruments et de genres musicaux doit être maintenu pour associer les utilisateurs et événements.

#### Besoins Fonctionnels
1. **Gestion des instruments (Instrument)**
   - **creer()** : Ajoute un instrument au catalogue.
   - **maj()** : Met à jour un instrument.
   - **supprimer()** : Supprime un instrument.
   - **obtenir_details()** : Retourne les détails d’un instrument.
   - **obtenir_utilisateurs_par_instrument()** : Liste les utilisateurs jouant cet instrument.
   - **Bonne Pratique** : Données pré-remplies via un Faker.

2. **Gestion des genres (Genre)**
   - **creer()** : Ajoute un genre au catalogue.
   - **maj()** : Met à jour un genre.
   - **supprimer()** : Supprime un genre.
   - **obtenir_details()** : Retourne les détails d’un genre.
   - **obtenir_utilisateurs_par_genre()** : Liste les utilisateurs aimant ce genre.
   - **Bonne Pratique** : Données statiques ou dynamiques selon les besoins.

---

## Bonnes Pratiques Globales
- **Sécurité** : JWT pour l’authentification, HTTPS obligatoire, validation stricte des entrées, protection des données sensibles.
- **Documentation** : OpenAPI/Swagger pour documenter les endpoints, commentaires dans le code (docstrings Python).
- **Versionnage** : Branches GitFlow (`feature/`, `main`), commits clairs, Pull Requests avec revue.
- **Containerisation** : Docker pour le backend et la base de données (ex. : PostgreSQL), fichiers `Dockerfile` et `docker-compose.yml`.
- **Tests** : Tests unitaires (avec pytest pour FastAPI) pour chaque endpoint, tests fonctionnels pour les flux critiques.
- **Déploiement** : AlwaysData pour le backend, configuration HTTPS gratuite.

---

## Conclusion
Ce document couvre toutes les fonctionnalités backend nécessaires pour *Mobile Musician App*, avec un niveau de détail permettant une compréhension précise et une implémentation rigoureuse. Les bonnes pratiques sont intégrées à chaque étape pour garantir un système sécurisé, maintenable et performant. Prochaine étape : implémentation des modèles avec FastAPI et SQLAlchemy, configuration Docker, ou définition des endpoints API. Indiquez-moi la suite souhaitée !