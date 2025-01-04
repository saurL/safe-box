import os
import random

from Accesmanager import AccessManager
from filemanager import FileManager
from EncryptionManager import EncryptionManager
from certificat import certificat
import sympy

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
        self.prime_number_one = None
        self.prime_number_two = None
        self.e = 65537
        self.mod = None
        self.session_key =  None
        self.g = 5
        self.p = 2**127 - 1

    def connect_user(self, loggin,password):
        loggin = self.décrypt_communication(loggin)
        password = self.décrypt_communication(password)
        # dérivation du mot de passe pour avoir la clé privé et on la stocke
        
        public_key = self.encryption_manager.key_derivation(password).hex()

        random.seed(public_key)
        prime_number_one = sympy.randprime(2**120, 2**121)
        prime_number_two = sympy.randprime(2**120, 2**121)
        print("p :", prime_number_one,"q",prime_number_two)
        self.mod = prime_number_one * prime_number_two
        mod = (prime_number_one-1)*(prime_number_two-1)
        self.connected = self.access_manager.connect(loggin,public_key)
        if self.connected:
            self.user_public_key = [hex(self.e)[2:],self.mod]
            self.user_private_key = [hex( self.encryption_manager.mod_inverse_key(self.user_public_key[0],mod))[2:],self.mod]
            print("User public key : ", self.user_public_key)
            test_value = 521765217
                          
            print(int(self.user_private_key[0],16) ==sympy.mod_inverse(self.e,mod) )
            print(test_value)
            enc_test_value = pow(test_value,self.e,self.mod)
            print("Encrypted test value : ", enc_test_value)
            dec_test_value = pow(enc_test_value,int(self.user_private_key[0],16),self.mod)
            print ("Decrypted test value : ", dec_test_value)
            
            print(int(self.user_private_key[0],16))
            print("User private key : ", self.user_private_key)
            self.user_dir = loggin
            print(f"Connected to user '{self.user_dir}'.")
        return self.connected
    
    def verify_certificat(self):
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

    
    def diffle_hellman(self,user_half):
    
        # Echange de diffle hellman coté serveur
        key = "f7c3ecf1d6c7e2b84d7321f3a4e5b0d28d4f1b5e1c6b94e1c8f5e7d9b0f8d7e4d7c1b9a0c9a4d2f4a9e8b7d1c3e1f0a8e6d0f9b7e2c3b0e4c7a5f2e9d1f5b6c8e2f1a4c6b8d0e6f7b8c2d5b1f3a4b9d2e7c6f3d1a9e7c4b8f1d7b4a0d9b5e2c3f6b1a7e3d9f8c7b0e2f1c3b7d8a1f4e5d3a9c7e4b2c5f0d1a4c3b7d8e1f3b9c4a2b1e6f7c0d9b5a4c2f7b0d8c1e9f6b4a5b2f3a8e9d1c0f7b8"
        int_key = int(key,16)
        shared_half = pow(self.g, int_key, self.p)
        self.session_key = hex(pow(user_half,int_key, self.p))[2:]

        # Extend the session key to 256 characters
        while len(self.session_key) < 256:
            self.session_key += self.session_key
        self.session_key = self.session_key[:256]
        print ("Clé de session coté serveur : ",self.session_key)
        return shared_half

    


    def save_file(self, filename, content):

        filename = self.décrypt_communication(filename)
        content = self.décrypt_communication(content)

        print(f"{self.user_dir} , {filename}")
        file_path = os.path.join(self.user_dir, filename)
        print(f"Saving file '{file_path}'...")
        print("content : ",content)
        self.file_manager.save_file(file_path,content,self.user_public_key)

    def list_files_in_folder(self):
        if not self.connected:
            return []
        print(f"gettin files in {self.user_dir}")

        list_files = self.file_manager.list_files_in_folder(self.user_dir)
        encrypted_files =[self.encrypt_communication(file) for file in list_files]
        return encrypted_files
    
    def get_file_content(self, filename):

        filename = self.décrypt_communication(filename)

        if not self.connected:
            return ""
        file_path = os.path.join(self.user_dir, filename)
        print(f"Getting file content from '{file_path}'...")

        content = self.file_manager.read_file(file_path,self.user_private_key)
        return self.encrypt_communication(content)

    

    def create_access(self,loggin, password):
        print("key derivation with password",password)
        public_key = self.encryption_manager.key_derivation(password)
        print(f"Creating access for user {password} with public key :'{public_key.hex()}'...")
        return self.access_manager.create_access(loggin,public_key)
    # dérivation du mot de passe pour avoir la clé privé  et publique

    def décrypt_communication(self,input):
        # décryptage de la communication envoyé par le client CObra clé de session

        print("Déchifrrement de la communication")

        print("input : ",input)
        outpout = self.encryption_manager.decrypt_cobra(input,self.session_key)
        print ("outpout : " , outpout)
        return outpout
    
    
    def encrypt_communication(self,input):
        # cryptage de la communication envoyé par le serveur Cobra clé de session

        print("Chiffrement de la communication")

        print("input : ",input)
        outpout = self.encryption_manager.cobra(input,self.session_key)
        print ("outpout : " , outpout)
        return outpout
    
