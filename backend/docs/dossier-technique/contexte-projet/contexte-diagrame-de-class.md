# Diagramme de Classes - Mobile Musician App

Ce document décrit le diagramme de classes de l'application *Mobile Musician App*, une plateforme permettant aux musiciens de se connecter, organiser des événements musicaux, communiquer via messagerie, et gérer leurs profils, instruments et genres musicaux préférés. Chaque entité, attribut, méthode, relation et note est détaillé pour une compréhension complète et précise.

---

## Packages

Le modèle est organisé en cinq packages pour regrouper les fonctionnalités par domaine :

1. **Gestion des Utilisateurs** : Gère les profils, compétences et préférences des musiciens.
2. **Gestion des Événements** : Gère les événements musicaux et les participations.
3. **Système de Messagerie** : Gère les conversations et les messages entre utilisateurs.
4. **Système de Notification** : Gère les alertes envoyées aux utilisateurs.
5. **Données de Référence** : Gère les catalogues d'instruments et de genres musicaux.

---

## Entités et Détails

### Package : Gestion des Utilisateurs

#### Classe : Utilisateur
- **Description** : Entité centrale représentant un musicien dans l'application. Gère l'authentification, les informations de profil, la localisation géographique, et les interactions avec d'autres entités (événements, conversations).
- **Attributs** :
  - `id: UUID [PK]` : Identifiant unique de l'utilisateur (clé primaire).
  - `nom_utilisateur: str` : Pseudo choisi par l'utilisateur, affiché dans l'application.
  - `email: str` : Adresse email pour l'authentification et les notifications.
  - `mot_de_passe_hash: str` : Mot de passe haché pour sécuriser l'accès.
  - `photo_profil: str` : URL ou chemin vers la photo de profil de l'utilisateur.
  - `biographie: str` : Description personnelle ou artistique de l'utilisateur.
  - `latitude: float` : Coordonnée géographique (latitude) pour localiser l'utilisateur.
  - `longitude: float` : Coordonnée géographique (longitude) pour localiser l'utilisateur.
  - `date_creation: datetime` : Date et heure de création du compte.
  - `derniere_connexion: datetime` : Date et heure de la dernière connexion.
  - `actif: bool` : Indique si le compte est actif ou désactivé.
- **Méthodes** :
  - `s_inscrire(): bool` : Inscrit un nouvel utilisateur dans le système (retourne vrai si succès).
  - `connexion(): str` : Authentifie l'utilisateur et retourne un token ou identifiant de session.
  - `deconnexion(): bool` : Déconnecte l'utilisateur (retourne vrai si succès).
  - `maj_profil(): bool` : Met à jour les informations du profil (photo, bio, etc.).
  - `supprimer_compte(): bool` : Supprime définitivement le compte de l'utilisateur.
  - `changer_mot_de_passe(): bool` : Modifie le mot de passe de l'utilisateur.
  - `obtenir_profil(): dict` : Retourne les détails du profil sous forme de dictionnaire.
  - `obtenir_evenements(): list` : Retourne la liste des événements créés ou auxquels l'utilisateur participe.
  - `chercher_evenements_proches(): list` : Recherche les événements à proximité en fonction de la localisation.
  - `obtenir_conversations(): list` : Retourne la liste des conversations actives de l'utilisateur.

#### Classe : UtilisateurInstrument
- **Description** : Table de liaison entre *Utilisateur* et *Instrument*. Associe un utilisateur à un instrument qu'il joue, avec son niveau de compétence.
- **Attributs** :
  - `utilisateur_id: UUID [PK, FK]` : Référence à l'utilisateur (clé primaire et étrangère).
  - `instrument_id: UUID [PK, FK]` : Référence à l'instrument (clé primaire et étrangère).
  - `niveau: str` : Niveau de compétence (ex. : débutant, intermédiaire, expert).
- **Méthodes** :
  - `ajouter(): bool` : Ajoute un instrument à la liste de l'utilisateur.
  - `maj_niveau(): bool` : Met à jour le niveau de compétence pour un instrument.
  - `supprimer(): bool` : Supprime un instrument de la liste de l'utilisateur.

#### Classe : UtilisateurGenre
- **Description** : Table de liaison entre *Utilisateur* et *Genre*. Associe un utilisateur aux genres musicaux qu'il préfère.
- **Attributs** :
  - `utilisateur_id: UUID [PK, FK]` : Référence à l'utilisateur (clé primaire et étrangère).
  - `genre_id: UUID [PK, FK]` : Référence au genre musical (clé primaire et étrangère).
- **Méthodes** :
  - `ajouter(): bool` : Ajoute un genre à la liste des préférences de l'utilisateur.
  - `supprimer(): bool` : Supprime un genre des préférences de l'utilisateur.

---

### Package : Gestion des Événements

#### Classe : Evenement
- **Description** : Représente un événement musical (jam session, concert, répétition). Inclut des données de localisation pour l'affichage sur une carte.
- **Attributs** :
  - `id: UUID [PK]` : Identifiant unique de l'événement (clé primaire).
  - `titre: str` : Titre de l'événement (ex. : "Jam Session Paris").
  - `description: str` : Description détaillée de l'événement.
  - `date_debut: datetime` : Date et heure de début de l'événement.
  - `date_fin: datetime` : Date et heure de fin de l'événement.
  - `latitude: float` : Coordonnée géographique (latitude) de l'événement.
  - `longitude: float` : Coordonnée géographique (longitude) de l'événement.
  - `adresse: str` : Adresse physique de l'événement.
  - `createur_id: UUID [FK]` : Référence à l'utilisateur qui a créé l'événement (clé étrangère).
  - `type: str` : Type d'événement (ex. : concert, jam, répétition).
  - `statut: str` : Statut de l'événement (ex. : planifié, annulé, terminé).
  - `capacite_max: int` : Nombre maximum de participants.
  - `url_image: str` : URL de l'image associée à l'événement.
  - `date_creation: datetime` : Date et heure de création de l'événement.
- **Méthodes** :
  - `creer(): bool` : Crée un nouvel événement dans le système.
  - `mettre_a_jour(): bool` : Met à jour les détails de l'événement.
  - `annuler(): bool` : Annule l'événement.
  - `obtenir_participants(): list` : Retourne la liste des utilisateurs participants.
  - `obtenir_details(): dict` : Retourne les détails de l'événement sous forme de dictionnaire.
  - `recherche_par_lieu(lat, long, rayon): list` : Recherche les événements dans un rayon donné autour d'une position.
  - `recherche_par_date(debut, fin): list` : Recherche les événements dans une plage de dates.
  - `recherche_par_type(type): list` : Recherche les événements par type (ex. : concert).

#### Classe : Participation
- **Description** : Table de liaison entre *Utilisateur* et *Evenement*. Gère les inscriptions des utilisateurs aux événements avec des détails comme l'instrument joué.
- **Attributs** :
  - `id: UUID [PK]` : Identifiant unique de la participation (clé primaire).
  - `utilisateur_id: UUID [FK]` : Référence à l'utilisateur participant (clé étrangère).
  - `evenement_id: UUID [FK]` : Référence à l'événement (clé étrangère).
  - `statut: str` : Statut de la participation (ex. : confirmé, en attente, annulé).
  - `date_inscription: datetime` : Date et heure de l'inscription.
  - `instrument_id: UUID [FK]` : Référence à l'instrument que l'utilisateur jouera (clé étrangère).
- **Méthodes** :
  - `s_inscrire(): bool` : Inscrit un utilisateur à un événement.
  - `maj_statut(): bool` : Met à jour le statut de la participation.
  - `annuler(): bool` : Annule la participation de l'utilisateur.
  - `obtenir_details(): dict` : Retourne les détails de la participation.

#### Classe : EvenementInstrument
- **Description** : Table de liaison entre *Evenement* et *Instrument*. Indique les instruments requis pour un événement.
- **Attributs** :
  - `evenement_id: UUID [PK, FK]` : Référence à l'événement (clé primaire et étrangère).
  - `instrument_id: UUID [PK, FK]` : Référence à l'instrument requis (clé primaire et étrangère).
- **Méthodes** :
  - `ajouter(): bool` : Ajoute un instrument requis à l'événement.
  - `supprimer(): bool` : Supprime un instrument requis de l'événement.

---

### Package : Système de Messagerie

#### Classe : Conversation
- **Description** : Représente une conversation entre utilisateurs (individuelle ou en groupe). Gère les messages et les participants.
- **Attributs** :
  - `id: UUID [PK]` : Identifiant unique de la conversation (clé primaire).
  - `date_creation: datetime` : Date et heure de création de la conversation.
  - `dernier_message: datetime` : Date et heure du dernier message envoyé.
- **Méthodes** :
  - `creer(): bool` : Crée une nouvelle conversation.
  - `obtenir_messages(): list` : Retourne la liste des messages de la conversation.
  - `obtenir_participants(): list` : Retourne la liste des utilisateurs participants.
  - `ajouter_participant(id): bool` : Ajoute un utilisateur à la conversation.
  - `supprimer_participant(id): bool` : Supprime un utilisateur de la conversation.

#### Classe : ConversationUtilisateur
- **Description** : Table de liaison entre *Conversation* et *Utilisateur*. Gère les participants d'une conversation.
- **Attributs** :
  - `conversation_id: UUID [PK, FK]` : Référence à la conversation (clé primaire et étrangère).
  - `utilisateur_id: UUID [PK, FK]` : Référence à l'utilisateur participant (clé primaire et étrangère).
- **Méthodes** :
  - `rejoindre(): bool` : Ajoute un utilisateur à la conversation.
  - `quitter(): bool` : Retire un utilisateur de la conversation.

#### Classe : Message
- **Description** : Représente un message envoyé dans une conversation entre utilisateurs.
- **Attributs** :
  - `id: UUID [PK]` : Identifiant unique du message (clé primaire).
  - `expediteur_id: UUID [FK]` : Référence à l'utilisateur qui envoie le message (clé étrangère).
  - `destinataire_id: UUID [FK]` : Référence à l'utilisateur qui reçoit le message (clé étrangère).
  - `contenu: str` : Contenu textuel du message.
  - `date_envoi: datetime` : Date et heure d'envoi du message.
  - `statut: str` : Statut du message (ex. : envoyé, lu, supprimé).
  - `conversation_id: UUID [FK]` : Référence à la conversation à laquelle le message appartient (clé étrangère).
- **Méthodes** :
  - `envoyer(): bool` : Envoie le message dans la conversation.
  - `marquer_comme_lu(): bool` : Marque le message comme lu par le destinataire.
  - `supprimer(): bool` : Supprime le message.
  - `obtenir_details(): dict` : Retourne les détails du message.

---

### Package : Système de Notification

#### Classe : Notification
- **Description** : Gère les alertes envoyées aux utilisateurs pour des événements comme nouveaux messages ou changements d'événements.
- **Attributs** :
  - `id: UUID [PK]` : Identifiant unique de la notification (clé primaire).
  - `utilisateur_id: UUID [FK]` : Référence à l'utilisateur destinataire (clé étrangère).
  - `type: str` : Type de notification (ex. : message, événement, participation).
  - `contenu: str` : Contenu textuel de la notification.
  - `date_creation: datetime` : Date et heure de création de la notification.
  - `statut: str` : Statut de la notification (ex. : non lue, lue).
  - `reference_id: UUID` : Référence à l'entité liée (ex. : ID d’un message ou événement).
- **Méthodes** :
  - `creer(): bool` : Crée une nouvelle notification.
  - `marquer_comme_lu(): bool` : Marque la notification comme lue.
  - `supprimer(): bool` : Supprime la notification.
  - `obtenir_details(): dict` : Retourne les détails de la notification.

---

### Package : Données de Référence

#### Classe : Instrument
- **Description** : Catalogue des instruments musicaux disponibles dans l'application, avec catégorisation.
- **Attributs** :
  - `id: UUID [PK]` : Identifiant unique de l'instrument (clé primaire).
  - `nom: str` : Nom de l'instrument (ex. : guitare, piano).
  - `categorie: str` : Catégorie de l'instrument (ex. : cordes, claviers).
  - `icone_url: str` : URL de l'icône représentant l'instrument.
- **Méthodes** :
  - `creer(): bool` : Ajoute un nouvel instrument au catalogue.
  - `maj(): bool` : Met à jour les détails de l'instrument.
  - `supprimer(): bool` : Supprime un instrument du catalogue.
  - `obtenir_details(): dict` : Retourne les détails de l'instrument.
  - `obtenir_utilisateurs_par_instrument(): list` : Retourne la liste des utilisateurs jouant cet instrument.

#### Classe : Genre
- **Description** : Catalogue des genres musicaux pour associer les préférences des utilisateurs.
- **Attributs** :
  - `id: UUID [PK]` : Identifiant unique du genre (clé primaire).
  - `nom: str` : Nom du genre (ex. : rock, jazz).
  - `description: str` : Description du genre musical.
- **Méthodes** :
  - `creer(): bool` : Ajoute un nouveau genre au catalogue.
  - `maj(): bool` : Met à jour les détails du genre.
  - `supprimer(): bool` : Supprime un genre du catalogue.
  - `obtenir_details(): dict` : Retourne les détails du genre.
  - `obtenir_utilisateurs_par_genre(): list` : Retourne la liste des utilisateurs aimant ce genre.

---

## Relations entre Entités

### Relations Principales

1. **Utilisateur "1" -- "0..*" Evenement : "crée"**
   - **Cardinalité** : Un utilisateur peut créer zéro ou plusieurs événements.
   - **Rôle** : Établit une relation de propriété entre l'utilisateur et les événements qu'il organise.
   - **Fonctionnalité** : Permet à l'utilisateur de gérer (éditer, annuler) les événements qu'il a créés.

2. **Utilisateur "0..*" -- "0..*" Evenement : "participe à\nvia Participation"**
   - **Cardinalité** : Plusieurs utilisateurs peuvent participer à plusieurs événements (relation N à M).
   - **Rôle** : Gérée par la table *Participation* pour suivre les inscriptions.
   - **Fonctionnalité** : Permet aux utilisateurs de s'inscrire à des événements et aux créateurs de voir les participants.

3. **Utilisateur "1" -- "0..*" Participation : "possède"**
   - **Cardinalité** : Un utilisateur peut avoir zéro ou plusieurs participations.
   - **Rôle** : Relie un utilisateur à ses engagements dans des événements.
   - **Fonctionnalité** : Gère les détails des participations (statut, instrument) pour chaque utilisateur.

4. **Evenement "1" -- "0..*" Participation : "possède"**
   - **Cardinalité** : Un événement peut avoir zéro ou plusieurs participations.
   - **Rôle** : Relie un événement à la liste de ses participants.
   - **Fonctionnalité** : Permet de lister et gérer les participants d’un événement.

5. **Utilisateur "1" -- "0..*" Message : "envoie"**
   - **Cardinalité** : Un utilisateur peut envoyer zéro ou plusieurs messages.
   - **Rôle** : Identifie l’expéditeur de chaque message.
   - **Fonctionnalité** : Permet aux utilisateurs d’envoyer des messages dans les conversations.

6. **Utilisateur "1" -- "0..*" Message : "reçoit"**
   - **Cardinalité** : Un utilisateur peut recevoir zéro ou plusieurs messages.
   - **Rôle** : Identifie le destinataire de chaque message.
   - **Fonctionnalité** : Assure que les messages sont dirigés vers les bons utilisateurs.

7. **Utilisateur "1" -- "0..*" Notification : "reçoit"**
   - **Cardinalité** : Un utilisateur peut recevoir zéro ou plusieurs notifications.
   - **Rôle** : Relie les notifications à leur destinataire.
   - **Fonctionnalité** : Permet d’alerter les utilisateurs sur des événements (nouveaux messages, changements).

8. **Utilisateur "0..*" -- "0..*" Instrument : "joue\nvia UtilisateurInstrument"**
   - **Cardinalité** : Plusieurs utilisateurs peuvent jouer plusieurs instruments (N à M).
   - **Rôle** : Gérée par *UtilisateurInstrument* pour associer les compétences musicales.
   - **Fonctionnalité** : Permet de filtrer les utilisateurs par instrument et de répondre aux besoins des événements.

9. **Utilisateur "0..*" -- "0..*" Genre : "aime\nvia UtilisateurGenre"**
   - **Cardinalité** : Plusieurs utilisateurs peuvent aimer plusieurs genres (N à M).
   - **Rôle** : Gérée par *UtilisateurGenre* pour stocker les préférences musicales.
   - **Fonctionnalité** : Facilite la mise en relation des musiciens par goûts musicaux.

10. **Evenement "0..*" -- "0..*" Instrument : "requiert\nvia EvenementInstrument"**
    - **Cardinalité** : Plusieurs événements peuvent nécessiter plusieurs instruments (N à M).
    - **Rôle** : Gérée par *EvenementInstrument* pour définir les besoins instrumentaux.
    - **Fonctionnalité** : Permet aux créateurs de préciser les instruments recherchés.

11. **Utilisateur "0..*" -- "0..*" Conversation : "participe à\nvia ConversationUtilisateur"**
    - **Cardinalité** : Plusieurs utilisateurs peuvent participer à plusieurs conversations (N à M).
    - **Rôle** : Gérée par *ConversationUtilisateur* pour gérer les participants.
    - **Fonctionnalité** : Permet la messagerie individuelle ou en groupe.

12. **Conversation "1" -- "0..*" Message : "contient"**
    - **Cardinalité** : Une conversation peut contenir zéro ou plusieurs messages.
    - **Rôle** : Organise les messages dans une conversation spécifique.
    - **Fonctionnalité** : Permet de regrouper et d’afficher les échanges dans une conversation.

### Relations avec les Tables de Liaison

1. **Utilisateur "1" -- "0..*" UtilisateurInstrument : "possède"**
   - **Cardinalité** : Un utilisateur peut être associé à zéro ou plusieurs instruments.
   - **Rôle** : Stocke les compétences instrumentales de l’utilisateur.
   - **Fonctionnalité** : Permet à l’utilisateur de gérer ses instruments et niveaux.

2. **Instrument "1" -- "0..*" UtilisateurInstrument : "utilisé par"**
   - **Cardinalité** : Un instrument peut être joué par zéro ou plusieurs utilisateurs.
   - **Rôle** : Relie les instruments aux utilisateurs compétents.
   - **Fonctionnalité** : Facilite la recherche de musiciens par instrument.

3. **Utilisateur "1" -- "0..*" UtilisateurGenre : "préfère"**
   - **Cardinalité** : Un utilisateur peut préférer zéro ou plusieurs genres.
   - **Rôle** : Enregistre les préférences musicales de l’utilisateur.
   - **Fonctionnalité** : Permet de proposer des événements ou musiciens selon les goûts.

4. **Genre "1" -- "0..*" UtilisateurGenre : "aimé par"**
   - **Cardinalité** : Un genre peut être aimé par zéro ou plusieurs utilisateurs.
   - **Rôle** : Relie les genres aux utilisateurs.
   - **Fonctionnalité** : Aide à regrouper les utilisateurs par affinités musicales.

5. **Evenement "1" -- "0..*" EvenementInstrument : "nécessite"**
   - **Cardinalité** : Un événement peut nécessiter zéro ou plusieurs instruments.
   - **Rôle** : Définit les besoins instrumentaux d’un événement.
   - **Fonctionnalité** : Permet aux créateurs de préciser les instruments recherchés.

6. **Instrument "1" -- "0..*" EvenementInstrument : "requis dans"**
   - **Cardinalité** : Un instrument peut être requis par zéro ou plusieurs événements.
   - **Rôle** : Relie les instruments aux événements.
   - **Fonctionnalité** : Facilite la recherche d’événements par instrument.

7. **Conversation "1" -- "0..*" ConversationUtilisateur : "inclut"**
   - **Cardinalité** : Une conversation peut inclure zéro ou plusieurs utilisateurs.
   - **Rôle** : Gère les participants d’une conversation.
   - **Fonctionnalité** : Permet de lister les membres d’une conversation.

8. **Utilisateur "1" -- "0..*" ConversationUtilisateur : "impliqué dans"**
   - **Cardinalité** : Un utilisateur peut participer à zéro ou plusieurs conversations.
   - **Rôle** : Relie les utilisateurs à leurs conversations.
   - **Fonctionnalité** : Permet de suivre les discussions d’un utilisateur.

9. **Instrument "1" -- "0..*" Participation : "utilisé dans"**
   - **Cardinalité** : Un instrument peut être utilisé dans zéro ou plusieurs participations.
   - **Rôle** : Spécifie l’instrument choisi par un participant pour un événement.
   - **Fonctionnalité** : Permet de savoir quel instrument un utilisateur jouera.

---

## Notes Contextuelles

- **Utilisateur** : *"Entité centrale représentant les musiciens. Gère authentification, profil, et relations."*
  - Rôle clé dans toutes les interactions (création d’événements, messagerie, notifications).
- **Evenement** : *"Représente événements musicaux. Inclut données de localisation pour carte."*
  - Supporte la fonctionnalité de recherche géolocalisée.
- **Conversation** : *"Permet messagerie directe et groupe. Lie utilisateurs pour communication."*
  - Essentiel pour la collaboration entre musiciens.
- **Notification** : *"Alerte utilisateurs des nouveaux messages, changements d'événements, etc."*
  - Améliore l’expérience utilisateur avec des mises à jour en temps réel.
- **Participation** : *"Suit quels utilisateurs rejoignent quels événements et instruments joués."*
  - Gère les inscriptions et les besoins instrumentaux des événements.
- **Instrument** : *"Catalogue des instruments musicaux avec catégorisation."*
  - Base pour associer utilisateurs et événements selon les compétences.
- **Genre** : *"Classification des styles musicaux pour mise en relation des musiciens."*
  - Facilite les connexions basées sur les préférences musicales.

---

## Conclusion

Ce diagramme de classes est une représentation complète et détaillée de *Mobile Musician App*. Il inclut toutes les entités nécessaires, leurs attributs, méthodes, relations avec cardinalités, et des explications précises sur leur rôle et leur impact fonctionnel. Cette base de connaissance peut être utilisée par toute IA ou développeur pour implémenter le backend (ex. : FastAPI avec SQLAlchemy) ou concevoir l’interface utilisateur avec une compréhension parfaite du modèle.

Si vous avez besoin d'une implémentation spécifique ou d'une prochaine étape (modèles SQLAlchemy, endpoints API, Docker), faites-le-moi savoir !