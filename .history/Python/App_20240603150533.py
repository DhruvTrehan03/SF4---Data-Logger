import sys
import math
import serial
import warnings
import serial.tools.list_ports
import time
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QDial
from PyQt6.QtCore import Qt,QTimer




    # def retranslateUi(self, MainWindow):
    #     _translate = QtCore.QCoreApplication.translate
    #     MainWindow.setWindowTitle(_translate("MainWindow", "Guitar Pro"))
    #     self.label_connection.setText(_translate("MainWindow", "Connection Status"))
    #     self.label_tuner.setText(_translate("MainWindow", "Note"))
    #     self.pushButton.setText(_translate("MainWindow", "Click Me"))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.Dial_1 = 0
        self.Dial_2 = 0
        self.connect_state = 0
        # Set the window title and size policy
        self.setWindowTitle("Guitar Pro")
        self.setFixedSize(600, 500)  # Set a reasonable minimum size


        # Use QVBoxLayout for automatic resizing
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setObjectName("mainLayout")

        self.top_row = QtWidgets.QHBoxLayout()
        self.top_row.setObjectName("toprow")
        # Add the first label to theform layout
        self.label_connection = QtWidgets.QLabel("Connection Status:")
        self.label_connection.setFixedSize(500,50)
        self.label_connection.setObjectName("label_connection")
        self.top_row.addWidget(self.label_connection)

        self.connection = QtWidgets.QPushButton("Connect")
        self.connection.setObjectName("connection")
        self.connection.clicked.connect(self.connection_make)
        self.top_row.addWidget(self.connection)


        self.light = QLabel()
        self.light.setFixedSize(20, 20)
        self.light.setStyleSheet("background-color: gray; border-radius: 10px;")
        self.top_row.addWidget(self.light)

        
        # Horizontal layout for the dials to keep them the same size
        self.dialLayout = QtWidgets.QHBoxLayout()
        self.dialLayout.setObjectName("dialLayout")

        self.dial = QtWidgets.QDial()
        self.dial.setObjectName("dial")
        self.dial.valueChanged.connect(self.on_dial_valueChanged)
        self.dial.setFixedSize(200,200)
        self.dial.setMinimum(1)
        self.dial.setMaximum(6)
        self.dial.setSingleStep(1)

        self.dialLayout.addWidget(self.dial)

        self.dial_2 = QtWidgets.QDial()
        self.dial_2.setObjectName("dial_2")
        self.dial_2.valueChanged.connect(self.on_dial_2_valueChanged)
        self.dial_2.setFixedSize(200,200)
        self.dial_2.setMaximum(6)
        self.dial_2.setMinimum(1)
        self.dial_2.setSingleStep(1)

        self.dialLayout.addWidget(self.dial_2)

        self.create_dial_labels_1(self.dial, [ "Clean", "Fuzz", "Tremelo", "Overdrive", "Delay", "Chorus"])
        self.create_dial_labels_2(self.dial_2,  [ "Clean", "Fuzz", "Tremelo", "Overdrive", "Delay", "Chorus"])


        # Horizontal layout for the label and button to keep them the same size
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")

        self.label_tuner = QtWidgets.QLabel("Tuning")
        self.label_tuner.setObjectName("label")
        self.label_tuner.setFixedSize(300,250)
        self.buttonLayout.addWidget(self.label_tuner)

        self.pushButton = QtWidgets.QPushButton("Upload")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setFixedSize(200,200)
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

        # Set timer for Serial Read
                # Create a QTimer to periodically read from the serial port
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_label)
        self.timer.start(100)  # Update every 1000 milliseconds (1 second)


        # Connect signals to slots
    def update_label(self):
        if self.connect_state == 1:
            if self.ser.in_waiting > 0:
                serial_data = self.ser.readline().decode('utf-8').strip()
                print(serial_data)
                self.label_tuner.setText(serial_data)
    

    def connection_make(self):
        print("Press")
        arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'Arduino' in p.description  # may need tweaking to match new arduinos
        ]
        print(arduino_ports)
        if not arduino_ports:
            self.light.setStyleSheet("background-color: red; border-radius: 10px;")
        if len(arduino_ports) > 1:
            warnings.warn('Multiple Arduinos found - using the first')
            self.light.setStyleSheet("background-color: green; border-radius: 10px;")

        try:
            self.ser = serial.Serial(arduino_ports[0], baudrate=9600)
        except:
            self.light.setStyleSheet("background-color: red; border-radius: 10px;")
            self.connect_state = 0
        else:
            self.light.setStyleSheet("background-color: green; border-radius: 10px;")
            self.connect_state = 1

    def create_dial_labels_1(self, dial, labels):
        radius = dial.width() // 2
        center_x = dial.x() + radius + 40
        center_y = dial.y() + radius -10

        num_labels = len(labels)
        angle_step = 320 / num_labels 

        for i, label in enumerate(labels):
            angle = i * angle_step - 225  # Start from the top (-90 degrees)
            radians = math.radians(angle)
            x = center_x + (radius+5) * math.cos(radians) - 15+15
            y = center_y + (radius+5) * math.sin(radians) - 15 +80

            lbl = QLabel(label, self)
            lbl.setFixedSize(60, 30)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.move(int(x), int(y))
            lbl.show()          

    def create_dial_labels_2(self, dial, labels):
        radius = dial.width() // 2
        center_x = dial.x() + radius + 315
        center_y = dial.y() + radius - 10

        num_labels = len(labels)
        angle_step = 320 / num_labels

        for i, label in enumerate(labels):
            angle = i * angle_step - 225  # Start from the top (-90 degrees)
            radians = math.radians(angle)
            x = center_x + (radius) * math.cos(radians) - 15
            y = center_y + (radius) * math.sin(radians) - 15 + 80

            lbl = QLabel(label, self)
            lbl.setFixedSize(60, 30)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.move(int(x), int(y))
            lbl.show()
            
    def on_pushButton_clicked(self):
        
        # Placeholder slot for button click
        
        self.ser.write(bytes(str(self.Dial_1) + str(self.Dial_2), 'utf-8'))
        print(bytes(str(self.Dial_1) + str(self.Dial_2), 'utf-8'))

    def on_dial_valueChanged(self, value):
              # Adjust value to nearest step
        step_1 = self.dial.singleStep()
        adjusted_value = round(value / step_1) * step_1
        self.dial.setValue(adjusted_value)
        self.Dial_1 = adjusted_value

    def on_dial_2_valueChanged(self, value):
            # Adjust value to nearest step
        step_2 = self.dial_2.singleStep()
        adjusted_value = round(value / step_2) * step_2
        self.dial_2.setValue(adjusted_value)
        self.Dial_2 = adjusted_value
    
    def closeEvent(self, event):
        self.ser.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
