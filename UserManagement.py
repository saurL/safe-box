from ServerManager import ServerManager

class UserManager:
    _instance = None

    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super(UserManager, self).__new__(self, *args, **kwargs)
        return self._instance
    def __init__(self):
        self.serverManager = ServerManager()
        self.connected = False

    def connect(self,password):

        self.connected = self.serverManager.connect_user(password)
        return self.connected
        
    def save_file(self, filename, content):
        self.serverManager.save_file(filename, content)

    def get_files(self):
        #il faudra décrypter les noms du fichier avec Cobra et la clé de sessiosn
        return self.serverManager.list_files_in_folder()
    
    def get_file_content(self, filename):
        return self.serverManager.get_file_content(filename)
        # décriptage du fichier du cryptage avec Cobra et la clé de session
    def create(self,password):
        return self.serverManager.create_access(password)
    
    def connect_to_serveur(self):
        # Demande de certificat 

        # Réception de la clé de session

        return
