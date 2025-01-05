from Sponge import Sponge
import random
# Constants
phi = 0x9e3779b9
r = 32

IPTable = [
    0, 32, 64, 96, 1, 33, 65, 97, 2, 34, 66, 98, 3, 35, 67, 99,
    4, 36, 68, 100, 5, 37, 69, 101, 6, 38, 70, 102, 7, 39, 71, 103,
    8, 40, 72, 104, 9, 41, 73, 105, 10, 42, 74, 106, 11, 43, 75, 107,
    12, 44, 76, 108, 13, 45, 77, 109, 14, 46, 78, 110, 15, 47, 79, 111,
    16, 48, 80, 112, 17, 49, 81, 113, 18, 50, 82, 114, 19, 51, 83, 115,
    20, 52, 84, 116, 21, 53, 85, 117, 22, 54, 86, 118, 23, 55, 87, 119,
    24, 56, 88, 120, 25, 57, 89, 121, 26, 58, 90, 122, 27, 59, 91, 123,
    28, 60, 92, 124, 29, 61, 93, 125, 30, 62, 94, 126, 31, 63, 95, 127,
    ]

def S(box, input):
    """Apply S-box number 'box' to 4-bit bitstring 'input' and return a
    4-bit bitstring as the result."""

    return SBoxBitstring[box%8][input]
    # There used to be 32 different S-boxes in serpent-0. Now there are
    # only 8, each of which is used 4 times (Sboxes 8, 16, 24 are all
    # identical to Sbox 0, etc). Hence the %8.


def IP(input):
    """Apply the Initial Permutation to the 128-bit bitstring 'input'
    and return a 128-bit bitstring as the result."""

    return applyPermutation(IPTable, input)

def applyPermutation(permutationTable, input):
    """Apply the permutation specified by the 128-element list
    'permutationTable' to the 128-bit bitstring 'input' and return a
    128-bit bitstring as the result."""

    if len(input) != len(permutationTable):
        raise ValueError (f"input size {len(input)} doesn't match perm table size {len(permutationTable)}")

    result = ""
    for i in range(len(permutationTable)):
        result = result + input[permutationTable[i]]
    return result


def binaryXor(n1, n2):
    """Return the xor of two bitstrings of equal length as another
    bitstring of the same length.

    EXAMPLE: binaryXor("10010", "00011") -> "10001"
    """

    if len(n1) != len(n2):
        raise ValueError("can't xor bitstrings of different " + \
              "lengths (%d and %d)" % (len(n1), len(n2)))
    # We assume that they are genuine bitstrings instead of just random
    # character strings.

    result = ""
    for i in range(len(n1)):
        if n1[i] == n2[i]:
            result = result + "0"
        else:
            result = result + "1"
    return result

def xor(*args):
    """Return the xor of an arbitrary number of bitstrings of the same
    length as another bitstring of the same length.

    EXAMPLE: xor("01", "11", "10") -> "00"
    """

    if args == []:
        raise ValueError("at least one argument needed")

    result = args[0]
    for arg in args[1:]:
        result = binaryXor(result, arg)
    return result

def rotateLeft(input, places):
    """Take a bitstring 'input' of arbitrary length. Rotate it left by
    'places' places. Left means that the 'places' most significant bits are
    taken out and reinserted as the least significant bits. Note that,
    because the bitstring representation is little-endian, the visual
    effect is actually that of rotating the string to the right.

    EXAMPLE: rotateLeft("000111", 2) -> "110001"
    """

    p = places % len(input)
    return input[-p:] + input[:-p]


def makeSubkeys(userKey):
    """Given the 256-bit bitstring 'userKey' (shown as K in the paper, but
    we can't use that name because of a collision with K[i] used later for
    something else), return two lists (conceptually K and KHat) of 33
    128-bit bitstrings each."""

    # Because in Python I can't index a list from anything other than 0,
    # I use a dictionary instead to legibly represent the w_i that are
    # indexed from -8.

    # We write the key as 8 32-bit words w-8 ... w-1
    # ENOTE: w-8 is the least significant word

    w = {}
    for i in range(-8, 0):
        w[i] = userKey[(i+8)*32:(i+9)*32]
    # We expand these to a prekey w0 ... w131 with the affine recurrence
    for i in range(132):
        w[i] = rotateLeft(
            xor(w[i-8], w[i-5], w[i-3], w[i-1],
                bitstring(phi, 32), bitstring(i,32)),
            11)

    # The round keys are now calculated from the prekeys using the S-boxes
    # in bitslice mode. Each k[i] is a 32-bit bitstring.
    k = {}
    for i in range(r+1):
        whichS = (r + 3 - i) % r
        k[0+4*i] = ""
        k[1+4*i] = ""
        k[2+4*i] = ""
        k[3+4*i] = ""
        for j in range(32): # for every bit in the k and w words
            # ENOTE: w0 and k0 are the least significant words, w99 and k99
            # the most.
            input = w[0+4*i][j] + w[1+4*i][j] + w[2+4*i][j] + w[3+4*i][j]
            output = S(whichS, input)
            for l in range(4):
                k[l+4*i] = k[l+4*i] + output[l]

    # We then renumber the 32 bit values k_j as 128 bit subkeys K_i.
    K = []
    for i in range(33):
        # ENOTE: k4i is the least significant word, k4i+3 the most.
        K.append(k[4*i] + k[4*i+1] + k[4*i+2] + k[4*i+3])

    # We now apply IP to the round key in order to place the key bits in
    # the correct column
    KHat = []
    for i in range(33):
        KHat.append(IP(K[i]))
        
    return K, KHat

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
    def hmac(self,input,session_key):
        return self.key_derivation(input+session_key)

    def __init__(self) -> None:
        self.sponge = Sponge(1152, 448, 24)
        self.F={}
        for i in range(256):
            self.F[bitstring(i,8)] = bitstring(self.mod_inverse(i + 1, 257) - 1,8)
         

    def key_derivation(self, password: str,size=2048) -> bytes:
        self.sponge.reset()
        iterations = 100

        key = password
        
        for _ in range(iterations):
            self.sponge.absorb(key)
            key = self.sponge.squeeze(size)
        return key 
    def mod_inverse_key(self,hex_key, prime):
        """
        Calcule l'inverse modulaire d'une clé publique en hexadécimal avec un modulo premier.
        
        :param hex_key: Clé publique en hexadécimal (str) ou un int 
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
    
    def inverse_sbox(self,block):
        result = ""
        for i in range(0, len(block), 4):
            input = block[i:i+4]
            """Applique une S-Box à un bloc de 128 bits divisé en 4 bits"""
            for _ in range(8):
                input = self.inv_sbox(input,1)
            for _ in range(8):
                input = self.inv_sbox(input,2)
            for _ in range(8):
                input = self.inv_sbox(input,3)
            for _ in range(8):
                input = self.inv_sbox(input,4)
            result += input
        return result

    def sbox(self,block, sbox):
        return SBoxBitstring[sbox%4][block]
    
    def inv_sbox(self,block, sbox):
        return SBoxBitstringInverse[sbox%4][block]
    
    def add_round_key(self,block, key):
        """XOR le bloc avec la clé d'itération"""
        return self.xor(block,key)
    
    def xor(self,a,b):
        return ''.join(str(int(b, 2) ^ int(k, 2) )for b, k in zip(a, b))
    
    def reverse_bits(self,byte):
        """Reverse the bits of an 8-bit byte."""
        return byte[::-1]
    
    def shift_binary_string(self,binary_string, shift):
        """
        Décale une chaîne binaire vers la gauche ou la droite en fonction du décalage.
        
        Args:
            binary_string (str): Chaîne binaire composée uniquement de '0' et '1'.
            shift (int): Décalage à effectuer. Si positif, décale vers la gauche.
                        Si négatif, décale vers la droite.
        
        Returns:
            str: La chaîne binaire après décalage.
        """
        # Vérification de l'entrée
        if not all(c in '01' for c in binary_string):
            raise ValueError("La chaîne doit contenir uniquement des '0' et '1'.")
        
        length = len(binary_string)
        
        # Normalisation du décalage pour éviter les dépassements
        shift = shift % length if length > 0 else 0  # Si la longueur est 0, évite une division par 0

        if shift == 0:
            return binary_string  # Aucun décalage nécessaire
        
        # Décalage gauche (shift positif)
        if shift > 0:
            return binary_string[shift:] + binary_string[:shift]
        
        # Décalage droit (shift négatif)
        else:
            shift = abs(shift)
            return binary_string[-shift:] + binary_string[:-shift]


    def feistel_step(self,L, R , inv = False):

        """Implémente une étape simplifiée de Feistel"""
        # Étape 1 : Inversion des bits et application de la fonction F=(x + 1)^-1 mod257 −1
        R_parts = [R[i:i+8] for i in range(len(R) // 8)]
        Z_parts = [self.F[self.reverse_bits(part)] for part in R_parts]
        Z = ''.join(Z_parts)
        
        # Étape 2 : Permutation des bits
        p = [45, 21, 20, 19, 32, 27, 38, 55, 14, 18, 59, 63, 1, 25, 13, 62, 33, 7, 50, 24, 56, 28, 26, 11, 53, 3, 22, 51, 9, 5, 58, 41, 29, 49, 23, 46, 17, 4, 44, 6, 16, 15, 36, 37, 34, 12, 60, 61, 8, 42, 54, 2, 43, 0, 52, 39, 31, 57, 35, 10, 40, 47, 48, 30] 
        
        Y = ''.join(Z[p[i]] for i in range(len(p)))
        # Étape 3 : Génération pseudo-aléatoire
        prng_values = []

        for i in range(0, len(Y), 8):
            block = Y[i:i+8]
            """
            cette façon de faire est beacoup trop couteuse en resrouce
            prng_value = self.key_derivation(block, 64)
            prng_value = ''.join(format(byte, '08b') for byte in prng_value)"""
            block_int = int(block, 2)
            random.seed(block_int)
            prng_value = format(random.randint(0, 255), '08b')
            prng_values.append(prng_value)
            prng_values.append(prng_value)

        prng_result = ''.join(prng_values)
        # XOR avec la clé dérivée
        xored = ''.join(format(int(Y[i:i+8], 2) ^ int(prng_result[i:i+8], 2), '08b') for i in range(0, len(Y), 8))

        new_R = ''.join(format(int(Y[i:i+8], 2) ^ int(L[i:i+8], 2), '08b') for i in range(0, len(xored), 8))
        new_L = R

        return new_L , new_R

    def serpent_iteration(self,block, keys):
        while len(block)!=128:
            block+="0"
       

        """Une itération de l'algorithme Serpent"""
        L, R = block[:64], block[64:]  # Division en deux moitiés
      
        for i in range(32):
            # Étape 1 : Add Round Key
            block = self.add_round_key(block, keys[i])
            # Étape 2 : Substitution avec S-Box
            block = self.apply_sbox(block)
            # Étape 3 : Feistel

            for _ in range(4): 
                L , R = self.feistel_step(L, R)
        
        return f"{L}{R}"
    
    def serpent_iteration_inverse(self,block, keys):
        while len(block)!=128:
            block+="0"
        L, R = block[:64], block[64:]  # Division en deux moitiés
        

        for i in range(31,-1,-1):

            for _ in range(4): 
                R , L = self.feistel_step(R, L)
        

            # Étape 2 : Substitution avec S-Box
            block = self.inverse_sbox(block)
            # Étape 1 : Add Round Key
            block = self.add_round_key(block, keys[i])

        block= f"{L}{R}"
        return block
    
    def cobra(self,input,key):
        result = ""
        input = ''.join(format(ord(c), '08b') for c in input)
        key = ''.join(format(ord(c), '08b') for c in key)
        _, keys = makeSubkeys(key)

        for i in range(0,len(input),128):
            end = min(i+128,len(input))
            result += self.cobra_itération(input[i:end], keys)

        byte_chunks = [result[i:i+8] for i in range(0, len(result), 8)]
        return ''.join(chr(int(byte, 2)) for byte in byte_chunks)
    
    def cobra_itération(self,input,keys):

        serpent_result = self.serpent_iteration(input,keys)
        
        A = serpent_result[:32]
        B = serpent_result[32:64]
        C = serpent_result[64:96]
        D = serpent_result[96:]  

        A = self.shift_binary_string(A,-13)
        C = self.shift_binary_string(C,-3)

        
        B = self.xor(B,self.xor(A,C))
        Tmp_A = self.shift_binary_string(A,-3)

        D = self.xor(D,self.xor(C,Tmp_A))

        B = self.shift_binary_string(B,-1)
        old_d=D
        D = self.shift_binary_string(D,-7)




        A = self.xor(A,self.xor(B,D))
        tmp_B = self.shift_binary_string(B,-7)

        C = self.xor(C,self.xor(tmp_B,D))

        A = self.shift_binary_string(A, -5)
        C = self.shift_binary_string(C , -22)

        return A +B + C + D

    def cobra_itération_inverse(self, input, keys ):
        A = input[:32]
        B = input[32:64]
        C = input[64:96]
        D = input[96:] 


            # Étape 1 : Inverser les décalages finaux sur A et C
        C = self.shift_binary_string(C, 22)
        A = self.shift_binary_string(A, 5)

        # Étape 2 : Inverser les XOR sur C
        tmp_B = self.shift_binary_string(B,- 7)  # Défaire le décalage précédent sur B
        C = self.xor(C, self.xor(tmp_B, D))
        

        # Étape 3 : Inverser les XOR sur A
        A = self.xor(A, self.xor(B, D))


        # Étape 4 : Inverser les décalages sur D et B
        D = self.shift_binary_string(D, 7)
        B = self.shift_binary_string(B, 1)

        


        # Étape 5 : Inverser les XOR sur D
        Tmp_A = self.shift_binary_string(A,- 3)

        D = self.xor(D, self.xor(C, Tmp_A))

        # Étape 6 : Inverser les XOR sur B
        B = self.xor(B, self.xor(A, C))

        

        # Étape 7 : Inverser les décalages sur C et A
        C = self.shift_binary_string(C, 3)
        A = self.shift_binary_string(A, 13)


        
        serpent_result = self.serpent_iteration_inverse(A+B+C+D, keys)
        
        

        # Reconstruction des blocs et retour
        return serpent_result
        
    def decrypt_cobra(self, input, key):
        result = ""
        input = ''.join(format(ord(c), '08b') for c in input)
        key = ''.join(format(ord(c), '08b') for c in key)
        _, keys = makeSubkeys(key)

        for i in range(0,len(input),128):
            end = min(i+128,len(input))
            result += self.cobra_itération_inverse(input[i:end], keys)

        byte_chunks = [result[i:i+8] for i in range(0, len(result), 8)]

        xeit = ''.join(chr(int(byte, 2)) if set(byte) == {'0', '1'} else '' for byte in byte_chunks)
        return  xeit

    