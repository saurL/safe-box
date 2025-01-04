import sympy
import random

class AuthentificationUser:
    def __init__(self, p, alpha, s):
        self.p = p
        self.alpha = alpha
        self.s = s
        self.pub = pow(alpha, s, p)
    
    def generate_proof(self, r):
        m = random.randint(1, self.p - 1)
        M = pow(self.alpha, m, self.p)
        Preuve = (m - r * self.s) % (self.p - 1)
        return M, Preuve


class VerificationBySafebox:
    def __init__(self, p, alpha):
        self.p = p
        self.alpha = alpha

    def challenge(self):
        r = random.randint(1, self.p - 1)
        return r

    def verify(self, M, Preuve, pub, r):
        return M == (pow(self.alpha, Preuve, self.p) * pow(pub, r, self.p) % self.p)


class VerificationByUser:
    def __init__(self, p_premier=None, q_premier=None ):
        self.p_premier = p_premier
        self.q_premier = q_premier


    def generate_keys(self):
        if self.p_premier is None or self.q_premier is None : 
            p_premier = sympy.randprime(2**1023, 2**1024)  # Premier grand nombre premier
            q_premier = sympy.randprime(2**1023, 2**1024)  # Deuxième grand nombre premier
        print("p :", p_premier,"q",q_premier)
        n = p_premier * q_premier  
        phi = (p_premier - 1) * (q_premier - 1)  #
        e = 65537  # Valeur de e (choisie comme étant un grand nombre premier souvent utilisé)
        d = sympy.mod_inverse(e, phi)  
        return ((e, n), (d, n))  # Retourne la clé publique et la clé privée

    # Chiffrement avec la clé publique
    def encrypt(self, message, key):
        e, n = key
        cipher = [pow(ord(char), e, n) for char in message]
        return cipher

    # Déchiffrement avec la clé privée
    def decrypt(self, ciphertext, key):
        d, n = key
        message = ''.join([chr(pow(char, d, n)) for char in ciphertext])
        return message


class certificat:
    def __init__(self):
        self.p = 23  
        self.alpha = 5
        self.s = 7


##### Authentification de l'utilisateur par la safebox

    def authenticate_user(self):
        authentification_user = AuthentificationUser(self.p, self.alpha, self.s)
        verification_by_safebox = VerificationBySafebox(self.p, self.alpha)
        
        print("Authentification l'utilisateur auprès de la safebox : ")

        # Authentification de l'utilisateur
        r = verification_by_safebox.challenge()
        M, Preuve = authentification_user.generate_proof(r)
        print(f"Message M de l'utilisateur : {M}, Preuve : {Preuve}")

        if verification_by_safebox.verify(M, Preuve, authentification_user.pub, r):
            print("M de la safebox :", M)
            print("Authentification réussie de l'utilisateur auprès de la safebox.")
            return True
        else:
            print("Authentification échouée de l'utilisateur auprès de la safebox.")
            return False
        
##### Authentification de la safebox par l'utilisateur

    def authenticate_safebox(self):
        print("Authentification de la safebox auprès de l'utilisateur : ")

        verification_by_user = VerificationByUser()

        # Génération des clés pour la safebox
        public_key, private_key = verification_by_user.generate_keys()
        print("Clé publique de la safebox :", public_key)

        # Chiffrement du certificat avec la clé privée
        certificat = "Je suis un certificat d'un coffre fort numérique super valide pour GS15 en A24"
        ciphertext = verification_by_user.encrypt(certificat, private_key)
        print("Certificat chiffré :", ciphertext)

        # Déchiffrement du certificat avec la clé publique de l'utilisateur
        decrypted_message = verification_by_user.decrypt(ciphertext, public_key)
        print("Certificat attendu :", certificat)
        print("Certificat déchiffré :", decrypted_message)

        # Vérification de l'authentification
        if decrypted_message == certificat:
            print("Authentification réussie de la safebox auprès de l'utilisateur.")
            return True
        else:
            print("Authentification échouée de la safebox auprès de l'utilisateur.")
            return False
  
