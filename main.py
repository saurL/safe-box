from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget
from Accesmanager import AccessManager

from pages.LoginWindow import LoginWindow
from pages.MenuWindow import MenuWindow
from pages.Filewindow import FileWindow

class Mainwindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(600, 600, 600, 150)
        self.setWindowTitle("Safebox")

        self.access_manager = AccessManager()

        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)

        self.stack = QStackedWidget()

        self.loggin_window = LoginWindow(self)
        self.menu_window = MenuWindow(self)
        self.file_window = FileWindow(self)
        self.stack.addWidget(self.loggin_window)
        self.stack.addWidget(self.menu_window)
        self.stack.addWidget(self.file_window)
        layout.addWidget(self.stack)
        self.go_to_login()

        self.setLayout(layout)

    
    def go_to_widget(self,widget):
        self.stack.setCurrentWidget(widget)
        self.stack.currentWidget().build_layout()
        print(f"switched to {widget}")

    def go_to_login(self):
        self.go_to_widget(self.loggin_window)

    def go_to_menu(self):
        self.go_to_widget(self.menu_window)

    def go_to_file(self):
        self.go_to_widget(self.file_window)

    def go_to_open_file(self,filename = ""):
        self.file_window.set_file(filename)
        self.go_to_widget(self.file_window)

if __name__ == "__main__":
    app = QApplication([])
    window = Mainwindow()
    window.show()
    app.exec_()