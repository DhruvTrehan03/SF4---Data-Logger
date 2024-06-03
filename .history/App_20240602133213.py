import sys
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import QSize


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
        self.setFixedSize(QSize(500, 500))  # Set a reasonable minimum size


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
        self.dial.setFixedSize(250,250)
        self.dial.setMinimum(0)
        self.dial.setMaximum(100)
        self.dial.setSingleStep(10)
        self.dialLayout.addWidget(self.dial)

        self.dial_2 = QtWidgets.QDial()
        self.dial_2.setObjectName("dial_2")
        self.dial_2.setNotchesVisible(True)
        
        self.dial_2.setFixedSize(250,250)
        self.dial_2.setMaximum(0)
        self.dial_2.setMinimum(100)
        self.dial_2.setSingleStep(10)
        self.dial_2.valueChanged.connect(self.on_dial_2_valueChanged)
        self.dialLayout.addWidget(self.dial_2)

        # Horizontal layout for the label and button to keep them the same size
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")

        self.label_tuner = QtWidgets.QLabel("Tuning")
        self.label_tuner.setObjectName("label")
        self.buttonLayout.addWidget(self.label_tuner)

        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setObjectName("pushButton")
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
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.dial.valueChanged.connect(self.on_dial_valueChanged)
        

    def on_pushButton_clicked(self):
        # Placeholder slot for button click
        print("Button clicked!")

    def on_dial_valueChanged(self, value):
        # Placeholder slot for dial value change
        print(f"Dial 1 value: {value}")

    def on_dial_2_valueChanged(self, value):
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
