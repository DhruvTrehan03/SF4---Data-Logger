import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtGui import QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Red Light Example")
        self.setGeometry(100, 100, 400, 200)

        # Create main layout
        self.main_layout = QVBoxLayout()

        # Create label and light layout
        self.label_layout = QHBoxLayout()

        # Label
        self.label = QLabel("Status:")
        self.label_layout.addWidget(self.label)

        # Light
        self.light = QLabel()
        self.light.setFixedSize(20, 20)
        self.light.setStyleSheet("background-color: gray; border-radius: 10px;")
        self.label_layout.addWidget(self.light)

        # Add label and light layout to main layout
        self.main_layout.addLayout(self.label_layout)

        # Button to toggle light
        self.toggle_button = QPushButton("Toggle Light")
        self.toggle_button.clicked.connect(self.toggle_light)
        self.main_layout.addWidget(self.toggle_button)

        # Create central widget
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.light_on = False

    def toggle_light(self):
        if self.light_on:
            self.light.setStyleSheet("background-color: gray; border-radius: 10px;")
        else:
            self.light.setStyleSheet("background-color: red; border-radius: 10px;")

        self.light_on = not self.light_on

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
