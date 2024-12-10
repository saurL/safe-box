class SHA256:
    def __init__(self):
        self.K = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xeffa0b69, 0x9159015a, 0x68fc31a4, 0x2b713151, 0x23bce6a0, 0x619f1510, 0x4a3f1a61,
            0x1e1f7ed7, 0x36ac1b0b, 0x47ae8e11, 0x19a4c116, 0x81ac8a99, 0x58d4ee7d, 0xdff8e1fa, 0xa85d3e00
        ]
        self.H = [
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        ]
    def reset(self):
        self.K = [
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xeffa0b69, 0x9159015a, 0x68fc31a4, 0x2b713151, 0x23bce6a0, 0x619f1510, 0x4a3f1a61,
            0x1e1f7ed7, 0x36ac1b0b, 0x47ae8e11, 0x19a4c116, 0x81ac8a99, 0x58d4ee7d, 0xdff8e1fa, 0xa85d3e00
        ]
        self.H = [
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        ]
    
    def pad(self, message):
        # Calcul de la longueur du message en bits
        length = len(message) * 8
        # Ajouter un bit '1' suivi de suffisamment de zéros
        message += b'\x80'
        while len(message) % 64 != 56:
            message += b'\x00'
        # Ajouter la longueur du message
        message += length.to_bytes(8, byteorder='big')
        return message

    def rotate_right(self, x, n):
        return (x >> n) | (x << (32 - n)) & 0xFFFFFFFF

    def process_chunk(self, chunk):
        W = [0] * 64
        for i in range(16):
            W[i] = int.from_bytes(chunk[i*4:i*4+4], byteorder='big')

        for i in range(16, 64):
            s0 = self.rotate_right(W[i-15], 7) ^ self.rotate_right(W[i-15], 18) ^ (W[i-15] >> 3)
            s1 = self.rotate_right(W[i-2], 17) ^ self.rotate_right(W[i-2], 19) ^ (W[i-2] >> 10)
            W[i] = (W[i-16] + s0 + W[i-7] + s1) & 0xFFFFFFFF

        a, b, c, d, e, f, g, h = self.H

        for i in range(64):
            S1 = self.rotate_right(e, 6) ^ self.rotate_right(e, 11) ^ self.rotate_right(e, 25)
            ch = (e & f) ^ (~e & g)
            temp1 = (h + S1 + ch + self.K[i%32] + W[i]) & 0xFFFFFFFF
            S0 = self.rotate_right(a, 2) ^ self.rotate_right(a, 13) ^ self.rotate_right(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF

        self.H = [(x + y) & 0xFFFFFFFF for x, y in zip(self.H, [a, b, c, d, e, f, g, h])]

    def digest(self, message):
        message = self.pad(message)
        for i in range(0, len(message), 64):
            self.process_chunk(message[i:i+64])

        return ''.join(f'{x:08x}' for x in self.H)

