from passlib.context import CryptContext  # Librairie de hachage sécurisée (bcrypt)

# Configuration de l'algorithme de hachage
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fonction qui permet de hacher un mot de passe
def get_password_hash(password: str) -> str:
    """
    Cette fonction prend un mot de passe en clair comme argument 
    et le hache (le chiffre) en utilisant l'algorithme bcrypt.
    
    :param password: Mot de passe en clair
    :return: Mot de passe haché sécurisé
    """
    return pwd_context.hash(password)  # Renvoie le mot de passe haché
