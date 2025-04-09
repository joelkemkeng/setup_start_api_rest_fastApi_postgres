Voici le diagramme de classes complet en PlantUML pour le projet Mobile Musician:

## Explication détaillée du diagramme de classes

### Entités principales

1. **Utilisateur**
   - Représente les musiciens inscrits sur l'application
   - Gère les informations de profil, authentification et localisation
   - Méthodes: inscription, connexion, gestion de profil, recherche d'événements à proximité

2. **Evenement**
   - Représente les jam sessions, concerts, répétitions et autres rencontres musicales
   - Inclut les coordonnées géographiques pour l'affichage sur carte
   - Méthodes: création, mise à jour, recherche par critères (lieu, date, type)

3. **Participation**
   - Relie utilisateurs et événements avec des informations supplémentaires
   - Indique quel instrument sera joué lors de l'événement
   - Suit le statut de participation (intéressé, confirmé, annulé)

4. **Message**
   - Gère les communications entre utilisateurs
   - Lié à un expéditeur, destinataire et conversation
   - Suit l'état des messages (envoyé, lu, supprimé)

5. **Conversation**
   - Regroupe les messages entre plusieurs utilisateurs
   - Permet la messagerie individuelle et de groupe
   - Conserve la date du dernier message pour l'affichage

6. **Notification**
   - Alerte les utilisateurs des activités importantes
   - Peut référencer différents objets (message, événement, invitation)
   - Suit l'état (non lue, lue, supprimée)

7. **Instrument**
   - Catalogue d'instruments musicaux avec catégorisation
   - Utilisé pour les profils musiciens et les besoins d'événements

8. **Genre**
   - Classification des styles musicaux
   - Facilite la mise en relation des musiciens par affinité musicale

### Tables de liaison

1. **UtilisateurInstrument**
   - Associe musiciens aux instruments qu'ils jouent
   - Inclut le niveau de compétence pour chaque instrument

2. **UtilisateurGenre**
   - Associe musiciens aux styles musicaux préférés

3. **EvenementInstrument**
   - Associe événements aux instruments recherchés

4. **ConversationUtilisateur**
   - Associe utilisateurs aux conversations auxquelles ils participent

### Fonctionnalités principales des relations

1. **Utilisateur → Evenement (création)**
   - Cardinalité: 1 à N
   - Permet de suivre qui a créé chaque événement
   - Base pour les permissions de modification d'événement

2. **Utilisateur ↔ Evenement (participation)**
   - Cardinalité: N à M via Participation
   - Permet aux musiciens de s'inscrire aux événements
   - Sert à afficher la liste des participants

3. **Utilisateur ↔ Instrument**
   - Cardinalité: N à M via UtilisateurInstrument
   - Permet la recherche de musiciens par instrument
   - Facilite le matching pour les événements

4. **Utilisateur ↔ Genre**
   - Cardinalité: N à M via UtilisateurGenre
   - Favorise la mise en relation par affinité musicale

5. **Evenement ↔ Instrument**
   - Cardinalité: N à M via EvenementInstrument
   - Permet de spécifier les instruments recherchés
   - Améliore la pertinence des recherches d'événements

6. **Utilisateur ↔ Conversation**
   - Cardinalité: N à M via ConversationUtilisateur
   - Permet la messagerie individuelle et de groupe
   - Base du système de communication entre musiciens

7. **Instrument ↔ Participation**
   - Cardinalité: 1 à N
   - Permet d'indiquer avec quel instrument on participe
   - Aide à constituer des groupes complets pour les jam sessions

Ce diagramme offre une vision complète de l'architecture nécessaire pour développer le backend FastAPI de l'application Mobile Musician, avec toutes les entités, attributs, méthodes et relations essentielles au fonctionnement de la plateforme.