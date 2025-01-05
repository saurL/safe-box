from PySide2.QtWidgets import  QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide2.QtCore import Qt
from UserManagement import UserManager
from PySide2.QtWidgets import QMessageBox

class LoginWindow(QWidget):
    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window
        self.user_manager = UserManager()


    def initUI(self):
        self.setWindowTitle("Login")
        self.setGeometry(600, 600, 600, 150)
        layout = QVBoxLayout()
        self.label_login = QLabel("Login:")
        layout.addWidget(self.label_login)
        self.label_login.setAlignment(Qt.AlignCenter)
        self.input_login = QLineEdit()
        layout.addWidget(self.input_login)

        self.label_password = QLabel("Password:")
        layout.addWidget(self.label_password)
        self.label_password.setAlignment(Qt.AlignCenter)
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_password)

        self.button_login = QPushButton("Se connecter")
        self.button_login.clicked.connect(self.connectAccount)
        layout.addWidget(self.button_login)

        self.button_signin = QPushButton("Se créer un compte")
        self.button_signin.clicked.connect(self.createAccount)
        layout.addWidget(self.button_signin)

        self.setLayout(layout)
    def build_layout(self):
        self.initUI()
        

    def createAccount(self):
        if not self.user_manager.create(self.input_login.text(),self.input_password.text()):
            print("Le compte n'a pas été créé car il exsite déjà")
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText("Nom d'utilisateur déjà utilisé")
            error_dialog.setWindowTitle("Erreur")
            error_dialog.exec_()
        else:
            print("Le compte a été créé avec succèes")
            
    def connectAccount(self):
        print(self.input_password.text())
        if not self.user_manager.connect(self.input_login.text(),self.input_password.text()):
            return
        print("connection réusse")
        self.main_window.go_to_menu()