import os
import random

from Accesmanager import AccessManager
from filemanager import FileManager
from EncryptionManager import EncryptionManager
from certificat import certificat

class ServerManager:

    _instance = None

    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super(ServerManager, self).__new__(self, *args, **kwargs)
        return self._instance

    def __init__(self) -> None:
        self.access_manager = AccessManager()
        self.file_manager = FileManager()
        self.encryption_manager = EncryptionManager()
        self.certificat = certificat()
        self.connected = False
        self.user_dir = ""
        self.user_public_key = None
        self.user_private_key = None
        self.prime_number_one = 2**127 - 1
        self.prime_number_two = 2**521 - 1
        self.mod = self.prime_number_one*self.prime_number_two

    def connect_user(self, loggin,password):
        self.décrypt_communication()
        # dérivation du mot de passe pour avoir la clé privé et on la stocke
        
        print("Vérification des certificats : ")

        # Authentification de l'utilisateur par le coffre
        if not self.certificat.authenticate_user():
            print("Authentification de l'utilisateur échouée")
            return False
        
        # Authentification du coffre par l'utilisateur
        if not self.certificat.authenticate_safebox():
            print("Authentification du coffre échouée.")
            return False
        
        print("Fin vérification des certificats \n")

    
        # A partir de la clé privé on obtient la clé publique et on vérifie qu'elle existe dans nos dossier
        public_key = self.encryption_manager.key_derivation(password).hex()
        # pulbic_key = password_hash

        self.connected = self.access_manager.connect(loggin,public_key)
        if self.connected:
            self.user_public_key = [public_key,self.mod]
            print("User public key : ", public_key)

            self.user_private_key = [hex( self.encryption_manager.mod_inverse_key(self.user_public_key[0],self.mod))[2:],self.mod]
            print("User private key : ", self.user_private_key)
            self.user_dir = password
            print(f"Connected to user '{self.user_dir}'.")
        return self.connected
    
    def connect_app(self):
        # vérification des certificats (A VOIR : pourquoi là ??)
        
        #envoit de la clef de session envoyé au client


        return 

    def save_file(self, filename, content):

        self.décrypt_communication()

        print(f"{self.user_dir} , {filename}")
        file_path = os.path.join(self.user_dir, filename)
        print(f"Saving file '{file_path}'...")

        self.file_manager.save_file(file_path,content,self.user_public_key)

    def list_files_in_folder(self):
        if not self.connected:
            return []
        print(f"gettin files in {self.user_dir}")

        self.encrypt_communication()

        return self.file_manager.list_files_in_folder(self.user_dir)
    
    def get_file_content(self, filename):

        self.décrypt_communication()

        if not self.connected:
            return ""
        file_path = os.path.join(self.user_dir, filename)
        print(f"Getting file content from '{file_path}'...")

        self.encrypt_communication()

        return self.file_manager.read_file(file_path,self.user_private_key)
    
    def create_access(self,loggin, password):
        print("key derivation with password",password)
        public_key = self.encryption_manager.key_derivation(password)
        print(f"Creating access for user {password} with public key :'{public_key.hex()}'...")
        return self.access_manager.create_access(loggin,public_key)
    # dérivation du mot de passe pour avoir la clé privé  et publique

    def décrypt_communication(self):
        # décryptage de la communication envoyé par le client CObra clé de session

        return
    
    def encrypt_communication(self):
        # cryptage de la communication envoyé par le serveur Cobra clé de session
        return
    
