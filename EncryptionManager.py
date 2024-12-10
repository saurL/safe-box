from Sponge import Sponge



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

if __name__ == "__main__":
    password = "mon_super_mot_de_passe"
    enc=EncryptionManager()
    derived_key = enc.key_derivation(password)
    print(f"Clé dérivée : {derived_key.hex()}")