import os 

from Accesmanager import AccessManager
from filemanager import FileManager

class UserManager:
    _instance = None

    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super(UserManager, self).__new__(self, *args, **kwargs)
        return self._instance
    def __init__(self):
        self.access_manager = AccessManager()
        self.file_manager = FileManager()
        self.user_dir = ""
        self.connected = False

    def connect(self,password):
        print(password)
        self.connected = self.access_manager.connect(password)
        if self.connected:
            self.user_dir = password
            print(f"Connected to user '{self.user_dir}'.")
        
        return self.connected
        
    def save_file(self, filename, content):
        print(f"{self.user_dir} , {filename}")
        file_path = os.path.join(self.user_dir, filename)
        print(f"Saving file '{file_path}'...")
        self.file_manager.save_file(file_path,content)

    def get_files(self):
        if not self.connected:
            return []
        print(f"gettin files in {self.user_dir}")
        return self.file_manager.list_files_in_folder(self.user_dir)
    
    def get_file_content(self, filename):
        if not self.connected:
            return ""
        file_path = os.path.join(self.user_dir, filename)
        print(f"Getting file content from '{file_path}'...")
        return self.file_manager.read_file(file_path)
