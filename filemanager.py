import os


class FileManager:
    def __init__(self):
        self.dirpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'safebox')
        if not os.path.exists(self.dirpath):
            os.makedirs(self.dirpath)

    def create_folder(self, foldername):
        folder_path = os.path.join(self.dirpath, foldername)
        os.makedirs(folder_path)

    def folder_exists(self, foldername):
        folder_path = os.path.join(self.dirpath, foldername)
        return os.path.exists(folder_path)

    def save_file(self, filename, content):
        with open(os.path.join(self.dirpath, filename), 'w') as file:
            file.write(content)

    def read_file(self, filename):
        with open(os.path.join(self.dirpath, filename), 'r') as file:
            return file.read()

    def delete_file(self, filename):
        os.remove(os.path.join(self.dirpath, filename))

    """
    Chaque nom de dossier correspond à une clef public donc à un utilisateur
    """
    def list_Dir(self):
        return os.listdir(self.dirpath)
    
    def list_files_in_folder(self, foldername):
        folder_path = os.path.join(self.dirpath, foldername)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            return os.listdir(folder_path)
        return []
