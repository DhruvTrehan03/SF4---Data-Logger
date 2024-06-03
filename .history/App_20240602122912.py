import sys
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import QSize

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        # Set up central widget and layout
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Use QVBoxLayout for automatic resizing
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName("mainLayout")

        # Form layout for widgets
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")

        # Add the first label to the form layout
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)

        # Horizontal layout for the dials to keep them the same size
        self.dialLayout = QtWidgets.QHBoxLayout()
        self.dialLayout.setObjectName("dialLayout")

        self.dial = QtWidgets.QDial(self.centralwidget)
        self.dial.setObjectName("dial")
        self.dialLayout.addWidget(self.dial)

        self.dial_2 = QtWidgets.QDial(self.centralwidget)
        self.dial_2.setObjectName("dial_2")
        self.dialLayout.addWidget(self.dial_2)

        self.formLayout.setLayout(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.dialLayout)

        # Horizontal layout for the label and button to keep them the same size
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.buttonLayout.addWidget(self.label)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.buttonLayout.addWidget(self.pushButton)

        self.formLayout.setLayout(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.buttonLayout)

        # Add the form layout to the main layout
        self.mainLayout.addLayout(self.formLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        # Set up menu and status bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Resizable PyQt6 App"))
        self.label_2.setText(_translate("MainWindow", "Dial 1:"))
        self.label.setText(_translate("MainWindow", "Dial 2:"))
        self.pushButton.setText(_translate("MainWindow", "Click Me"))

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Set the window title and size policy
        self.setWindowTitle("Resizable PyQt6 App")
        self.setFixedSize(QSize(500, 500))  # Set a reasonable minimum size

        # Set size policies for resizable widgets
        self.label_2.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.dial.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.dial_2.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.pushButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        # Connect signals to slots
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.dial.valueChanged.connect(self.on_dial_valueChanged)
        self.dial_2.valueChanged.connect(self.on_dial_2_valueChanged)

    def on_pushButton_clicked(self):
        # Placeholder slot for button click
        print("Button clicked!")

    def on_dial_valueChanged(self, value):
        # Placeholder slot for dial value change
        print(f"Dial 1 value: {value}")

    def on_dial_2_valueChanged(self, value):
        # Placeholder slot for dial 2 value change
        print(f"Dial 2 value: {value}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
