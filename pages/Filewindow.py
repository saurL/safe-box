import sys
from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget, QLineEdit, QTextEdit, QPushButton
from UserManagement import UserManager

class FileWindow(QWidget):
    def __init__(self,main_window):
        super().__init__()
        self.user_manager = UserManager()
        self.main_window = main_window
        self.filename = ""
        self.layout = QVBoxLayout()
    
    def set_file(self, filename):
        self.filename = filename
    def build_layout(self):
        while self.layout.count(): 
            item = self.layout.takeAt(0)
            widget = item.widget() 
            if widget is not None:
                widget.deleteLater()
        self.initUI()
    def initUI(self):
        print(self.filename)
        # Set the main widget and layout

        

        # Create a line edit for the file name
        self.file_name_edit = QLineEdit(self)
        self.file_name_edit.setPlaceholderText("File name")
        self.layout.addWidget(self.file_name_edit)
       
        # Create a text edit for the file content
        self.file_content_edit = QTextEdit(self)
        self.file_content_edit.setPlaceholderText("File content")
        self.layout.addWidget(self.file_content_edit)

        # si ouvre un fichier on ajoute son nom et son contenus  
        if self.filename:
            self.file_name_edit.setText(self.filename)
            filecontent= self.user_manager.get_file_content(self.filename)
            self.file_content_edit.setText(filecontent)
        else:
            
            self.file_name_edit.clear()
            self.file_content_edit.clear()
            self.file_content_edit.setText("")
        # Create a save button
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_file)
        self.layout.addWidget(save_button)

        # return boutton to go back to menuWindow
        return_button = QPushButton("Return", self)
        return_button.clicked.connect(self.return_to_menu)
        self.layout.addWidget(return_button)

        self.setLayout(self.layout)
        self.show()

    def return_to_menu(self):
        self.main_window.go_to_menu()

    def save_file(self):
        file_name = self.file_name_edit.text()
        file_content = self.file_content_edit.toPlainText()
        if file_name:
            self.user_manager.save_file(file_name, file_content)
            print(f"File '{file_name}' saved successfully.")
        else:
            print("Please enter a file name.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileWindow()
    sys.exit(app.exec_())