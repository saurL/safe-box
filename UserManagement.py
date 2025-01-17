from ServerManager import ServerManager
from EncryptionManager import EncryptionManager
import random
import sympy


class UserManager:
    _instance = None

    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super(UserManager, self).__new__(self, *args, **kwargs)
        return self._instance
    
    def __init__(self):
        self.encryption_manager = EncryptionManager()
        self.serverManager = ServerManager()
        self.connected = False
        self.session_key = "iauzerhiqsjdbfqisdfhiuhfiuzeahriuazhe"
        self.g = 5
        self.p = 2**127 - 1

    def connect(self,loggin , password):
        if not self.serverManager.verify_certificat():
            return
        # début de l'échange diffie hellman
        key= self.encryption_manager.key_derivation(password).hex()
        key_int = int(key,16)
        shared_hald = pow(self.g, key_int, self.p)
        
        server_half = self.serverManager.diffle_hellman(shared_hald)
        self.session_key =hex(pow(server_half, key_int, self.p))[2:]
                # Extend the session key to 256 characters
        while len(self.session_key) < 256:
            self.session_key += self.session_key
        self.session_key = self.session_key[:256]
        print("Clé de session coté utilisateur : ",self.session_key)
        encrypted_loggin , hasmac_loggin = self.encrypt_communication(loggin)
        encrypted_password , hasmac_password = self.encrypt_communication(password)
        self.connected = self.serverManager.connect_user(encrypted_loggin, encrypted_password,hasmac_loggin,hasmac_password)
        return self.connected
        
    def save_file(self, filename, content):
        print("Sauvegarde du fichier : ",filename)
        filename , hasmac_filename = self.encrypt_communication(filename)
        content , hasmac_content = self.encrypt_communication(content)
        self.serverManager.save_file(filename, content,hasmac_filename, hasmac_content)

    def get_files(self):
        #il faudra décrypter les noms du fichier avec Cobra et la clé de sessiosn
        print ("Récupération des fichiers")
        encrypted_files_names = self.serverManager.list_files_in_folder()
        print("Nom des fichiers chiffrés : ",[file[0] for file in encrypted_files_names])
        decrypted_files = [self.décrypt_communication(file[0],file[1]) for file in encrypted_files_names]
        decrypted_files_names = [file[0] for file in decrypted_files if file[1]]

        print("Nom des fichiers déchiffré coté utilisateur : ",decrypted_files_names)
        return decrypted_files_names
    
    def get_file_content(self, filename):
        print("Récupération du contenus du fichier : ",filename)
        encrypted_filename , hasmac = self.encrypt_communication(filename)
        content= self.serverManager.get_file_content(encrypted_filename , hasmac)
        decrypted_content , hasmac_ok= self.décrypt_communication(content[0],content[1])
        if not hasmac_ok:
            return ""
        print("Contenu du fichier : ",decrypted_content)
        
        return decrypted_content
        # décriptage du fichier du cryptage avec Cobra et la clé de session
    def create(self, loggin, password):
        if not self.serverManager.verify_certificat():
            return
        
        if not loggin or not password:
            return
        # début de l'échange diffie hellman
        key= self.encryption_manager.key_derivation(password).hex()
        key_int = int(key,16)
        shared_hald = pow(self.g, key_int, self.p)
        
        server_half = self.serverManager.diffle_hellman(shared_hald)
        self.session_key =hex(pow(server_half, key_int, self.p))[2:]
                # Extend the session key to 256 characters
        while len(self.session_key) < 256:
            self.session_key += self.session_key
        self.session_key = self.session_key[:256]
        print("Clé de session coté utilisateur : ",self.session_key)
        encrypted_loggin , hasmac_loggin= self.encrypt_communication(loggin)
        encrypted_password , hasmac_password= self.encrypt_communication(password)

        return self.serverManager.create_access(encrypted_loggin,encrypted_password,hasmac_loggin,hasmac_password)
    
    
    def décrypt_communication(self,input,hasmac):
        # décryptage de la communication envoyé par le client CObra clé de session

        print("Déchifrrement de la communication")

        print("input : ",input)
        outpout = self.encryption_manager.decrypt_cobra(input,self.session_key)
        print ("outpout : " , outpout)
        print("vérification du hashmac")
        hasmac_ok = self.encryption_manager.hmac(input,self.session_key) == hasmac
        print("hashmac correct : ",hasmac_ok)
        return outpout , hasmac_ok
    
    
    def encrypt_communication(self,input):
        # cryptage de la communication envoyé par le serveur Cobra clé de session

        print("Chiffrement de la communication")

        print("input : ",input)
        outpout = self.encryption_manager.cobra(input,self.session_key)
        print ("outpout : " , outpout)
        hasmac = self.encryption_manager.hmac(outpout,self.session_key)
        print("hasmac : ",hasmac)
        return outpout, hasmac