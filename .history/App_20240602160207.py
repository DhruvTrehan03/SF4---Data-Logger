import sys
import math
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QDial
from PyQt6.QtCore import Qt

    # def retranslateUi(self, MainWindow):
    #     _translate = QtCore.QCoreApplication.translate
    #     MainWindow.setWindowTitle(_translate("MainWindow", "Guitar Pro"))
    #     self.label_connection.setText(_translate("MainWindow", "Connection Status"))
    #     self.label_tuner.setText(_translate("MainWindow", "Note"))
    #     self.pushButton.setText(_translate("MainWindow", "Click Me"))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        
        # Set the window title and size policy
        self.setWindowTitle("Guitar Pro")
        self.setFixedSize(500, 500)  # Set a reasonable minimum size


        # Use QVBoxLayout for automatic resizing
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setObjectName("mainLayout")

        self.top_row = QtWidgets.QHBoxLayout()
        self.top_row.setObjectName("toprow")
        # Add the first label to theform layout
        self.label_connection = QtWidgets.QLabel("Connection Status")
        self.label_connection.setObjectName("label_connection")
        self.top_row.addWidget(self.label_connection)

        # Horizontal layout for the dials to keep them the same size
        self.dialLayout = QtWidgets.QHBoxLayout()
        self.dialLayout.setObjectName("dialLayout")

        self.dial = QtWidgets.QDial()
        self.dial.setObjectName("dial")
        self.dial.setNotchesVisible(True)
        self.dial.valueChanged.connect(self.on_dial_valueChanged)
        self.dial.setFixedSize(250,250)
        self.dial.setMinimum(1)
        self.dial.setMaximum(6)
        self.dial.setSingleStep(1)

        self.dialLayout.addWidget(self.dial)

        self.dial_2 = QtWidgets.QDial()
        self.dial_2.setObjectName("dial_2")
        self.dial_2.valueChanged.connect(self.on_dial_2_valueChanged)
        self.dial_2.setFixedSize(250,250)
        self.dial_2.setMaximum(6)
        self.dial_2.setMinimum(1)
        self.dial_2.setSingleStep(1)

        self.dialLayout.addWidget(self.dial_2)

        self.create_dial_labels(self.dial, self.dialLayout, [ "Clean", "Fuzz", "Tremelo", "Overdrive", "Delay", "Chorus"])
        self.create_dial_labels(self.dial_2, self.dialLayout, [ "Clean", "Fuzz", "Tremelo", "Overdrive", "Delay", "Chorus"])


        # Horizontal layout for the label and button to keep them the same size
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")

        self.label_tuner = QtWidgets.QLabel("Tuning")
        self.label_tuner.setObjectName("label")
        self.buttonLayout.addWidget(self.label_tuner)

        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.buttonLayout.addWidget(self.pushButton)

        self.mainLayout.addLayout(self.top_row)
        self.mainLayout.addLayout(self.dialLayout)
        self.mainLayout.addLayout(self.buttonLayout)

        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.setLayout(self.mainLayout)

        self.setCentralWidget(self.mainWidget)
        
        # Add the form layout to the main layout
        #self.mainLayout.addLayout(self.formLayout)

        # Set size policies for resizable widgets
        self.label_connection.setFixedSize(500,50)
        self.label_tuner.setFixedSize(400,200)
        self.pushButton.setFixedSize(100,150)

        # Connect signals to slots
        
    def create_dial_labels(self, dial, labels):
        dial_radius = dial.width() // 2
        center_x = dial.x() + dial_radius
        center_y = dial.y() + dial_radius

        num_labels = len(labels)
        angle_step = 360 / num_labels

        for i, label in enumerate(labels):
            angle = i * angle_step - 90  # Start from the top (-90 degrees)
            radians = math.radians(angle)
            x = center_x + (dial_radius + 30) * math.cos(radians) - 15
            y = center_y + (dial_radius + 30) * math.sin(radians) - 15

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
        print(f'Dial 1 value: {adjusted_value}')
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
