import os

"""
File manager correspond au serveur qui stocke les données
"""
class FileManager:
    def __init__(self):
        self.keydir="keys"
        self.dirpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'safebox')
        if not os.path.exists(self.dirpath):
            os.makedirs(self.dirpath)

    def create_folder(self, foldername):
        folder_path = os.path.join(self.dirpath, foldername)
        os.makedirs(folder_path)
    def create_key(self, foldername,key):
        print("wrinting key")
        folder_path = os.path.join(self.dirpath, foldername,self.keydir)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with open(os.path.join(folder_path, "key"), 'w') as file:
            file.write(key.hex())
        return
    def get_key(self, foldername):
        folder_path = os.path.join(self.dirpath,  foldername,self.keydir)
        with open(os.path.join(folder_path, "key"), 'r') as file:
            return file.read()
        return
    def folder_exists(self, foldername):
        folder_path = os.path.join(self.dirpath, foldername)
        return os.path.exists(folder_path)

    def save_file(self, filename, content,public_key):
        #encrypt pour filename aussi
        encrypted_content = self.encrypt_file(content,public_key)
        with open(os.path.join(self.dirpath, filename), 'wb') as file:
            file.write(encrypted_content)

    def read_file(self, filename,private_key):
        #decrypt pour filename aussi
        with open(os.path.join(self.dirpath, filename), 'rb') as file:
            return self.decrypt_file(file.read(),private_key)

    def delete_file(self, filename):
        os.remove(os.path.join(self.dirpath, filename))

    """
    Chaque nom de dossier correspond à une clef public donc à un utilisateur
    """
    def list_Dir(self):
        return os.listdir(self.dirpath)
    
    def list_files_in_folder(self, foldername):
        files =[]
        folder_path = os.path.join(self.dirpath, foldername)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            files= os.listdir(folder_path)
        files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
        print("files",files)
        return files

    def decrypt_file(self, content,private_key):
        #décryptage du fichier sauvegardé sur le serveur avec RSA clé privé
        key = int(private_key[0],16)
        print("key: " ,key)
        mod = private_key[1] 
        block_size=(mod.bit_length() + 7) // 8   # Calculate block size based on the length of the modulus
        print(mod,block_size,content,len(content))
        decrypted_content = bytearray()

        for i in range(0, len(content), block_size):
            end = min(i + block_size, len(content))
            block = content[i:end]
            block_int = int.from_bytes(block, byteorder='big')
            encrypted_block_int = pow(block_int, key, mod)
            encrypted_block = encrypted_block_int.to_bytes(block_size, byteorder='big')
            decrypted_content.extend(encrypted_block)
        print("valeur décrypté:" ,decrypted_content)
        return decrypted_content.decode()
    
    def encrypt_file(self, content , public_key):
        #décryptage du fichier sauvegardé sur le serveur avec RSA clé privé
        bytes_content = content.encode()
        print("valeur des bytes     ",bytearray( bytes_content))
        key = int(public_key[0],16)
        mod = public_key[1] 
        print("key: " ,key)

        block_size=(mod.bit_length() + 7) // 8   # Calculate block size based on the length of the modulus
        print(mod,block_size,content,len(bytes_content))
        encrypted_content = bytearray()

        for i in range(0, len(bytes_content), block_size):
            end = min(i + block_size, len(bytes_content))
            print("end",end , "i + block_size",i + block_size, "len(bytes_content)",len(bytes_content))
            block = bytes_content[i:end]
            block_int = int.from_bytes(block, byteorder='big')
            encrypted_block_int = pow(block_int, key, mod)
            encrypted_block = encrypted_block_int.to_bytes(block_size, byteorder='big')
            encrypted_content.extend(encrypted_block)
        print("valeur encrypté:" ,encrypted_content)
        return encrypted_content
