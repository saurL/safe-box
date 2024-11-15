import os

from Accesmanager import AccessManager
from filemanager import FileManager

class ServerManager:

    _instance = None

    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super(ServerManager, self).__new__(self, *args, **kwargs)
        return self._instance

    def __init__(self) -> None:
        self.access_manager = AccessManager()
        self.file_manager = FileManager()
        self.connected = False
        self.user_dir = ""

    def connect_user(self, password):
        self.décrypt_communication()
        # dérivation du mot de passe pour avoir la clé privé et on la stocke

        # A partir de la clé privé on obtient la clé publique et on vérifie qu'elle existe dans nos dossier
        self.connected = self.access_manager.connect(password)
        if self.connected:
            self.user_dir = password
            print(f"Connected to user '{self.user_dir}'.")
        return self.connected
    
    def connect_app(self):
        # veérification des certificats 

        #envoit de la clef de session envoyé au client


        return 

    def save_file(self, filename, content):

        self.décrypt_communication()

        print(f"{self.user_dir} , {filename}")
        file_path = os.path.join(self.user_dir, filename)
        print(f"Saving file '{file_path}'...")

        self.file_manager.save_file(file_path,content)

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

        return self.file_manager.read_file(file_path)
    
    def create_access(self, password):
        return self.access_manager.create_access(password)
    # dérivation du mot de passe pour avoir la clé privé  et publique

    def décrypt_communication(self):
        # décryptage de la communication envoyé par le client CObra clé de session

        return
    
    def encrypt_communication(self):
        # cryptage de la communication envoyé par le serveur Cobra clé de session
        return
    
