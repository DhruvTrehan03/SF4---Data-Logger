import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import QSize

# Import the generated UI class
from MainWindow import Ui_MainWindow  # Assuming the generated UI file is named 'AppUI.py'

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Set the window title and size policy
        self.setWindowTitle("Resizable PyQt6 App")
        self.setMinimumSize(QSize(800, 600))

        # Set size policies for resizable widgets
        self.label_2.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.dial.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.dial_2.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.pushButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
