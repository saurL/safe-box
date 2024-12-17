from Sponge import Sponge

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def are_coprime(a, b):
    return gcd(a, b) == 1

class EncryptionManager:

    def __init__(self) -> None:
        self.sponge = Sponge(1152, 448, 24)
        pass 

    def key_derivation(self, password: str) -> bytes:
        self.sponge.reset()
        iterations = 100

        key = password
        
        for _ in range(iterations):
            self.sponge.absorb(key)
            key = self.sponge.squeeze(2048)
        return key 
    def mod_inverse(self,hex_key, prime):
        """
        Calcule l'inverse modulaire d'une clé publique en hexadécimal avec un modulo premier.
        
        :param hex_key: Clé publique en hexadécimal (str)
        :param prime: Nombre premier utilisé pour le modulo (int)
        :return: Inverse modulaire (int) ou None si l'inverse n'existe pas
        """
        key = int(hex_key, 16)  # Convertir la clé hexadécimale en entier
        m = 2**521 - 1
        p = 2**127 - 1
        print("Key and prime_number_1 are coprime:", are_coprime(key, m-1))
        print("Key and prime_number_2 are coprime:", are_coprime(key, p-1))
        gcd, x, y = self.extended_gcd(key, prime)
        print("le pgcd est : ",gcd ,x,y)
        if gcd != 1:
            return None  # L'inverse n'existe pas si gcd(key, prime) != 1
        else:
            return x % prime

    def extended_gcd(self,a, b):
        x0, x1, y0, y1 = 1, 0, 0, 1
        while b != 0:
            q, a, b = a // b, b, a % b
            x0, x1 = x1, x0 - q * x1
            y0, y1 = y1, y0 - q * y1
        return a, x0, y0



                             

if __name__ == "__main__":
    password = "mon_super_mot_de_passe"
    enc=EncryptionManager()
    derived_key = enc.key_derivation(password)
    print(f"Clé dérivée : {derived_key.hex()}")