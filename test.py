from filemanager import FileManager
from EncryptionManager import EncryptionManager

if __name__ == "__main__":
    file_manager = FileManager()
    enc = EncryptionManager()
    mdp =  "aezrqdfazerazfygqsuidgfuzagyrfuveyzaué"
    public_key = enc.key_derivation(mdp).hex()
    mod = (2**127 - 1 )* (2**521 - 1)
    private_key =hex(enc.mod_inverse_key(public_key, mod))[2:]
    public_key = enc.key_derivation(mdp).hex()

    file_manager.create_folder("test")
    file_manager.save_file("test/test.txt", "Hello, World!",[public_key,mod])
    print(file_manager.read_file("test/test.txt",[private_key,mod]))