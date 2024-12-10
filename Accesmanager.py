from filemanager import FileManager

class AccessManager:
    def __init__(self,):
        self.file_manager = FileManager()

    def get_access(self):
        # Implement logic to get access
        data = self.file_manager.read_file()
        # Process data to determine access
        return data

    def set_access(self, Password):
        # Implement logic to set access
        self.file_manager.write_file(Password)

    def accessAlreadyExists(self,Password):
        return self.file_manager.folder_exists(Password) 

    def create_access(self, loggin,public_key):
        if self.accessAlreadyExists(loggin):
            return False
        self.file_manager.create_folder(loggin)
        self.create_key(loggin,public_key)
        return True
    def create_key(self, loggin,key):
        print("creating key")
        if not self.accessAlreadyExists(loggin):
            return False
        self.file_manager.create_key(loggin,key)
    
    def get_key(self, loggin):
        if not self.accessAlreadyExists(loggin):
            return False
        return self.file_manager.get_key(loggin)
    
    def connect(self, loggin,public_key):
        if public_key == "" or loggin == "":
            return False
        if not self.accessAlreadyExists(loggin):
            return False
        return self.get_key(loggin) == public_key
