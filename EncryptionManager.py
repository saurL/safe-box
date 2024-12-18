from Sponge import Sponge
import random

def bitstring(n, minlen=1):
    """Translate n from integer to bitstring, padding it with 0s as
    necessary to reach the minimum length 'minlen'. 'n' must be >= 0 since
    the bitstring format is undefined for negative integers.  Note that,
    while the bitstring format can represent arbitrarily large numbers,
    this is not so for Python's normal integer type: on a 32-bit machine,
    values of n >= 2^31 need to be expressed as python long integers or
    they will "look" negative and won't work. E.g. 0x80000000 needs to be
    passed in as 0x80000000L, or it will be taken as -2147483648 instead of
    +2147483648L.

    EXAMPLE: bitstring(10, 8) -> "01010000"
    """

    if minlen < 1:
        raise ValueError("a bitstring must have at least 1 char")
    if n < 0:
        raise ValueError("bitstring representation undefined for neg numbers")

    result = ""
    while n > 0:
        if n & 1:
            result = result + "1"
        else:
            result = result + "0"
        n = n >> 1
    if len(result) < minlen:
        result = result + "0" * (minlen - len(result))
    return result


SBoxDecimalTable = [
	[ 3, 8,15, 1,10, 6, 5,11,14,13, 4, 2, 7, 0, 9,12 ], # S0
	[15,12, 2, 7, 9, 0, 5,10, 1,11,14, 8, 6,13, 3, 4 ], # S1
	[ 8, 6, 7, 9, 3,12,10,15,13, 1,14, 4, 0,11, 5, 2 ], # S2
	[ 0,15,11, 8,12, 9, 6, 3,13, 1, 2, 4,10, 7, 5,14 ], # S3
	[ 1,15, 8, 3,12, 0,11, 6, 2, 5, 4,10, 9,14, 7,13 ], # S4
	[15, 5, 2,11, 4,10, 9,12, 0, 3,14, 8,13, 6, 7, 1 ], # S5
	[ 7, 2,12, 5, 8, 4, 6,11,14, 9, 1,15,13, 3,10, 0 ], # S6
	[ 1,13,15, 0,14, 8, 2,11, 7, 4,12,10, 9, 3, 5, 6 ], # S7
    ] 

SBoxBitstring = []
SBoxBitstringInverse = []
for line in SBoxDecimalTable:
    dict = {}
    inverseDict = {}
    for i in range(len(line)):
        index = bitstring(i, 4)
        value = bitstring(line[i], 4)
        dict[index] = value
        inverseDict[value] = index
    SBoxBitstring.append(dict)
    SBoxBitstringInverse.append(inverseDict)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def are_coprime(a, b):
    return gcd(a, b) == 1

class EncryptionManager:

    def __init__(self) -> None:
        self.sponge = Sponge(1152, 448, 24)
        self.F={}
        for i in range(256):
            self.F[i] = self.mod_inverse(i + 1, 257) - 1
         

    def key_derivation(self, password: str) -> bytes:
        self.sponge.reset()
        iterations = 100

        key = password
        
        for _ in range(iterations):
            self.sponge.absorb(key)
            key = self.sponge.squeeze(2048)
        return key 
    def mod_inverse_key(self,hex_key, prime):
        """
        Calcule l'inverse modulaire d'une clé publique en hexadécimal avec un modulo premier.
        
        :param hex_key: Clé publique en hexadécimal (str)
        :param prime: Nombre premier utilisé pour le modulo (int)
        :return: Inverse modulaire (int) ou None si l'inverse n'existe pas
        """
        key = int(hex_key, 16)
        return self.mod_inverse(key, prime)
    def mod_inverse(self,input, prime):
        """
        Calcule l'inverse modulaire d'une clé publique en hexadécimal avec un modulo premier.
        
        :param hex_key: Clé publique en hexadécimal (str)
        :param prime: Nombre premier utilisé pour le modulo (int)
        :return: Inverse modulaire (int) ou None si l'inverse n'existe pas
        """

        gcd, x, y = self.extended_gcd(input, prime)

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

    def apply_sbox(self,block):
        result = ""
        for i in range(0, len(block), 4):
            input = block[i:i+4]
            """Applique une S-Box à un bloc de 128 bits divisé en 4 bits"""
            for _ in range(8):
                input = self.sbox(input,1)
            for _ in range(8):
                input = self.sbox(input,2)
            for _ in range(8):
                input = self.sbox(input,3)
            for _ in range(8):
                input = self.sbox(input,4)
            result += input
        return result

    def sbox(self,block, sbox):
        return SBoxBitstring[sbox%4][block]
    def add_round_key(self,block, key):
        """XOR le bloc avec la clé d'itération"""
        return ''.join(str(int(b, 2) ^ int(k, 2) )for b, k in zip(block, key))

    def reverse_bits(self,byte):
        """Reverse the bits of an 8-bit byte."""
        return int('{:08b}'.format(byte)[::-1], 2)

    def feistel_step(self,block, round_key):
        """Implémente une étape simplifiée de Feistel"""
        L, R = block[:64], block[64:]  # Division en deux moitiés
        print("block",block)
        # Étape 1 : Inversion des bits
        R_parts = [(int(R) >> (8 * i)) & 0xFF for i in range(len(R) // 8)]
       
        Z_parts = [self.F[self.reverse_bits(part)] for part in R_parts]

        Z = ''.join(bitstring(part,8)for part in Z_parts)

        # Étape 1.5 : Application de la fonction f
    
        print("Z",Z)
        print("len Z",len(Z))
        # Étape 2 : Permutation des bits
        p = [45, 21, 20, 19, 32, 27, 38, 55, 14, 18, 59, 63, 1, 25, 13, 62, 33, 7, 50, 24, 56, 28, 26, 11, 53, 3, 22, 51, 9, 5, 58, 41, 29, 49, 23, 46, 17, 4, 44, 6, 16, 15, 36, 37, 34, 12, 60, 61, 8, 42, 54, 2, 43, 0, 52, 39, 31, 57, 35, 10, 40, 47, 48, 30]
        print("Z",Z)
        Y = ''.join(Z[p[i]] for i in range(len(Z)))
        print("Y",Y)
        # Étape 3 : Génération pseudo-aléatoire
        random.seed(int(round_key, 2))  # Graine à partir de la clé d'itération
        prng_values = [format(random.randint(0, 255), '08b') for _ in range(len(Y) // 8)]
        prng_result = ''.join(prng_values)
        # XOR avec la clé dérivée
        new_R = ''.join(format(int(Y[i:i+8], 2) ^ int(prng_result[i:i+8], 2), '08b') for i in range(0, len(Y), 8))
        new_L = R
        return new_L + new_R

    def serpent_iteration(self,block, round_key):
        """Une itération de l'algorithme Serpent"""
        print("itération")
        """print("block",block)
        block = bitstring(int(block, 2), 128)
        print("block after bitstring",block)"""
        # Étape 1 : Add Round Key
        block = self.add_round_key(block, round_key)

        # Étape 2 : Substitution avec S-Box
        block = self.apply_sbox(block)

        # Étape 3 : Feistel
        block = self.feistel_step(block, round_key)

        return block
    def cobra(self,input,key):
        result = ""
        input = ''.join(format(ord(c), '08b') for c in input)
        key = ''.join(format(ord(c), '08b') for c in key)

        for i in range(0,len(input),128):
            end = min(i+128,len(input))
            result += self.serpent_iteration(input[i:end], key)
        return result


                             

if __name__ == "__main__":
    print("dans main")
    password = "mon_super_mot_de_passe"
    enc=EncryptionManager()
    key = "1234567890ABCDEF"
    block = enc.cobra(password,key)
    # Diviser la chaîne binaire en groupes de 8 bits
    byte_chunks = [block[i:i+8] for i in range(0, len(block), 8)]

    # Convertir chaque groupe de 8 bits en caractère ASCII
    text = ''.join(chr(int(byte, 2)) for byte in byte_chunks)

    print(f"Texte converti : {text}")
    