from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QListWidget, QVBoxLayout, QWidget
from UserManagement import UserManager  # Corrected import

class MenuWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.user_manager = UserManager()  # Corrected class name
        self.layout = QVBoxLayout()

    def populate_file_list(self):
        self.file_list.clear()
        files = self.user_manager.get_files()
        print(files)
        for file in files:
            self.file_list.addItem(file)
    def build_layout(self):
        while self.layout.count(): 
            item = self.layout.takeAt(0)
            widget = item.widget() 
            if widget is not None:
                widget.deleteLater()
        self.initUI()
        
    def initUI(self):
        print("dans initUI de menu") 



        self.file_list = QListWidget(self)
        self.file_list.itemDoubleClicked.connect(lambda item: self.main_window.go_to_open_file(item.text()))
        self.populate_file_list()
        self.layout.addWidget(self.file_list)

        
        # Un bouton qui permet d'accéder à la page pour créer un fichier
        createFileButton = QPushButton('Create File')
        createFileButton.clicked.connect(self.main_window.go_to_new_file)
        self.layout.addWidget(createFileButton)

        self.setLayout(self.layout)

