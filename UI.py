from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide2.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(600, 600, 600, 150)
        layout = QVBoxLayout()

        self.label_password = QLabel("Password:")
        layout.addWidget(self.label_password)
        self.label_password.setAlignment(Qt.AlignCenter)
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_password)

        self.button_login = QPushButton("Se connecter")
        layout.addWidget(self.button_login)

        self.button_signin = QPushButton("Se créer un compte")
        layout.addWidget(self.button_login)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    window = LoginWindow()
    window.show()
    app.exec_()