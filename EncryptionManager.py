import hashlib

class EncryptionManager:

    def __init__(self) -> None:
        pass 

    def key_derivation(self, password: str) -> bytes:

        key_length = 32
        iterations  = 100000
        salt = b''

        #si l'on souhaite ajouter du sel aléatoire plus tard
        #if salt is None: # Générer un sel aléatoire 
        #    salt = os.urandom(16)

        key = hashlib.pbkdf2_hmac(
            'sha256',                    # Algorithme de hachage
            password.encode('utf-8'),    # Mot de passe en bytes
            salt,                         # Pas de sel (string vide)
            iterations,                  # Nombre d'itérations
            dklen=key_length             # Longueur de la clé souhaitée
        )

        return key                          

if __name__ == "__main__":
    password = "mon_super_mot_de_passe"
    enc=EncryptionManager()
    derived_key = enc.key_derivation(password)
    print(f"Clé dérivée : {derived_key.hex()}")