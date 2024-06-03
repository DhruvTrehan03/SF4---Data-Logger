import sys
import math
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QDial
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title and size policy
        self.setWindowTitle("Guitar Pro")
        self.setFixedSize(500, 500)  # Set a reasonable minimum size

        # Use QVBoxLayout for automatic resizing
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setObjectName("mainLayout")

        self.top_row = QHBoxLayout()
        self.top_row.setObjectName("toprow")
        # Add the first label to the form layout
        self.label_connection = QLabel("Connection Status")
        self.label_connection.setObjectName("label_connection")
        self.top_row.addWidget(self.label_connection)

        # Horizontal layout for the dials to keep them the same size
        self.dialLayout = QHBoxLayout()
        self.dialLayout.setObjectName("dialLayout")

        self.dial = QDial()
        self.dial.setObjectName("dial")
        self.dial.setNotchesVisible(True)
        self.dial.valueChanged.connect(self.on_dial_valueChanged)
        self.dial.setFixedSize(250, 250)
        self.dial.setMinimum(1)
        self.dial.setMaximum(6)
        self.dial.setSingleStep(1)

        self.dialLayout.addWidget(self.dial)

        self.dial_2 = QDial()
        self.dial_2.setObjectName("dial_2")
        self.dial_2.setNotchesVisible(True)
        self.dial_2.valueChanged.connect(self.on_dial_2_valueChanged)
        self.dial_2.setFixedSize(250, 250)
        self.dial_2.setMinimum(1)
        self.dial_2.setMaximum(6)
        self.dial_2.setSingleStep(1)

        self.dialLayout.addWidget(self.dial_2)

        # Create a layout for the labels
        self.mainLayout.addLayout(self.top_row)
        self.mainLayout.addLayout(self.dialLayout)
        
        self.create_dial_labels(self.dial, ["Clean", "Fuzz", "Tremolo", "Overdrive", "Delay", "Chorus"])
        self.create_dial_labels(self.dial_2, ["Clean", "Fuzz", "Tremolo", "Overdrive", "Delay", "Chorus"])

        # Horizontal layout for the label and button to keep them the same size
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")

        self.label_tuner = QLabel("Tuning")
        self.label_tuner.setObjectName("label")
        self.buttonLayout.addWidget(self.label_tuner)

        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.buttonLayout.addWidget(self.pushButton)

        self.mainLayout.addLayout(self.buttonLayout)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)

        self.setCentralWidget(self.mainWidget)

        # Set size policies for resizable widgets
        self.label_connection.setFixedSize(500, 50)
        self.label_tuner.setFixedSize(400, 200)
        self.pushButton.setFixedSize(100, 150)

    def create_dial_labels(self, dial, labels):
        radius = dial.width() // 2
        center_x = dial.x() + radius
        center_y = dial.y() + radius

        num_labels = len(labels)
        angle_step = 360 / num_labels

        for i, label in enumerate(labels):
            angle = i * angle_step - 180  # Start from the top (-90 degrees)
            radians = math.radians(angle)
            x = center_x + (radius ) * math.cos(radians) - 15
            y = center_y + (radius-60) * math.sin(radians) - 60-100

            lbl = QLabel(label, self)
            lbl.setFixedSize(60, 30)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.move(int(x), int(y))
            lbl.show()

    def on_pushButton_clicked(self):
        # Placeholder slot for button click
        print("Button clicked!")

    def on_dial_valueChanged(self, value):
        # Adjust value to nearest step
        step_1 = self.dial.singleStep()
        adjusted_value = round(value / step_1) * step_1
        self.dial.setValue(adjusted_value)
        print(f'Dial 1 value: {adjusted_value}')

    def on_dial_2_valueChanged(self, value):
        # Adjust value to nearest step
        step_2 = self.dial_2.singleStep()
        adjusted_value = round(value / step_2) * step_2
        self.dial_2.setValue(adjusted_value)
        print(f'Dial 2 value: {adjusted_value}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
