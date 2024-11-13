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

    def create_access(self, Password):
        if self.accessAlreadyExists(Password):
            return False
        self.file_manager.create_folder(Password)
        return True
    
    def connect(self, Password):
        if Password == "":
            return False
        if self.accessAlreadyExists(Password):
            return True
        return False
