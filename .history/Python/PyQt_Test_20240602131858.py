import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDial, QVBoxLayout, QWidget, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dial Example")

        # Create a QDial
        self.dial = QDial()
        self.dial.setMinimum(0)
        self.dial.setMaximum(100)
        self.dial.setSingleStep(10)  # Adjusts step size to lock to every 10 units

        # Create a QLabel to display the dial's value
        self.label = QLabel("Current Value: 0")

        # Connect the valueChanged signal to a custom slot
        self.dial.valueChanged.connect(self.update_label)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.dial)
        layout.addWidget(self.label)

        # Set the central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_label(self, value):
        # Adjust value to nearest step
        step = self.dial.singleStep()
        adjusted_value = round(value / step) * step
        self.dial.setValue(adjusted_value)
        self.label.setText(f"Current Value: {adjusted_value}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())