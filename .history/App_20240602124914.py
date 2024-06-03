import sys
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QDial
class Dial(QtGui.QDial):
    MinValue, MidValue, MaxValue = -1, 0, 1
    __valueChanged = QtCore.pyqtSignal(int)

    def __init__(self, valueRange=120):
        QtGui.QDial.__init__(self)
        self.setWrapping(True)
        self.setRange(0, 359)
        self.valueChanged.connect(self.emitSanitizedValue)
        self.valueChanged = self.__valueChanged
        self.valueRange = valueRange
        self.__midValue = valueRange / 2
        self.setPageStep(valueRange)
        self.setSingleStep(valueRange)
        QtGui.QDial.setValue(self, 180)
        self.oldValue = None
        # uncomment this if you want to emit the changed value only when releasing the slider
        # self.setTracking(False)
        self.notchSize = 5
        self.notchPen = QtGui.QPen(QtCore.Qt.black, 2)
        self.actionTriggered.connect(self.checkAction)

    def emitSanitizedValue(self, value):
        if value < 180:
            self.valueChanged.emit(self.MinValue)
        elif value > 180:
            self.valueChanged.emit(self.MaxValue)
        else:
            self.valueChanged.emit(self.MidValue)

    def checkAction(self, action):
        value = self.sliderPosition()
        if action in (self.SliderSingleStepAdd, self.SliderPageStepAdd) and value < 180:
            value = 180 + self.valueRange
        elif action in (self.SliderSingleStepSub, self.SliderPageStepSub) and value > 180:
            value = 180 - self.valueRange
        elif value < 180:
            value = 180 - self.valueRange
        elif value > 180:
            value = 180 + self.valueRange
        else:
            value = 180
        self.setSliderPosition(value)

    def valueFromPosition(self, pos):
        y = self.height() / 2. - pos.y()
        x = pos.x() - self.width() / 2.
        angle = degrees(atan2(y, x))
        if angle > 90 + self.__midValue or angle < -90:
            value = self.MinValue
            final = 180 - self.valueRange
        elif angle >= 90 - self.__midValue:
            value = self.MidValue
            final = 180
        else:
            value = self.MaxValue
            final = 180 + self.valueRange
        self.blockSignals(True)
        QtGui.QDial.setValue(self, final)
        self.blockSignals(False)
        return value

    def value(self):
        rawValue = QtGui.QDial.value(self)
        if rawValue < 180:
            return self.MinValue
        elif rawValue > 180:
            return self.MaxValue
        return self.MidValue

    def setValue(self, value):
        if value < 0:
            QtGui.QDial.setValue(self, 180 - self.valueRange)
        elif value > 0:
            QtGui.QDial.setValue(self, 180 + self.valueRange)
        else:
            QtGui.QDial.setValue(self, 180)

    def mousePressEvent(self, event):
        self.oldValue = self.value()
        value = self.valueFromPosition(event.pos())
        if self.hasTracking() and self.oldValue != value:
            self.oldValue = value
            self.valueChanged.emit(value)

    def mouseMoveEvent(self, event):
        value = self.valueFromPosition(event.pos())
        if self.hasTracking() and self.oldValue != value:
            self.oldValue = value
            self.valueChanged.emit(value)

    def mouseReleaseEvent(self, event):
        value = self.valueFromPosition(event.pos())
        if self.oldValue != value:
            self.valueChanged.emit(value)

    def wheelEvent(self, event):
        delta = event.delta()
        oldValue = QtGui.QDial.value(self)
        if oldValue < 180:
            if delta < 0:
                outValue = self.MinValue
                value = 180 - self.valueRange
            else:
                outValue = self.MidValue
                value = 180
        elif oldValue == 180:
            if delta < 0:
                outValue = self.MinValue
                value = 180 - self.valueRange
            else:
                outValue = self.MaxValue
                value = 180 + self.valueRange
        else:
            if delta < 0:
                outValue = self.MidValue
                value = 180
            else:
                outValue = self.MaxValue
                value = 180 + self.valueRange
        self.blockSignals(True)
        QtGui.QDial.setValue(self, value)
        self.blockSignals(False)
        if oldValue != value:
            self.valueChanged.emit(outValue)

    def paintEvent(self, event):
        QtGui.QDial.paintEvent(self, event)
        qp = QtGui.QPainter(self)
        qp.setRenderHints(qp.Antialiasing)
        qp.translate(.5, .5)
        rad = radians(self.valueRange)
        qp.setPen(self.notchPen)
        c = -cos(rad)
        s = sin(rad)
        # use minimal size to ensure that the circle used for notches
        # is always adapted to the actual dial size if the widget has
        # width/height ratio very different from 1.0
        maxSize = min(self.width() / 2, self.height() / 2)
        minSize = maxSize - self.notchSize
        center = self.rect().center()
        qp.drawLine(center.x(), center.y() -minSize, center.x(), center.y() - maxSize)
        qp.drawLine(center.x() + s * minSize, center.y() + c * minSize, center.x() + s * maxSize, center.y() + c * maxSize)
        qp.drawLine(center.x() - s * minSize, center.y() + c * minSize, center.x() - s * maxSize, center.y() + c * maxSize)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 500)

        # Set up central widget and layout
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Use QVBoxLayout for automatic resizing
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName("mainLayout")

        self.top_row = QtWidgets.QHBoxLayout()
        self.top_row.setObjectName("toprow")
        # Add the first label to theform layout
        self.label_connection = QtWidgets.QLabel(self.centralwidget)
        self.label_connection.setObjectName("label_connection")
        self.top_row.addWidget(self.label_connection)

        # Horizontal layout for the dials to keep them the same size
        self.dialLayout = QtWidgets.QHBoxLayout()
        self.dialLayout.setObjectName("dialLayout")

        self.dial = QtWidgets.QDial(self.centralwidget)
        self.dial.setObjectName("dial")
        self.dialLayout.addWidget(self.dial)

        self.dial_2 = QtWidgets.QDial(self.centralwidget)
        self.dial_2.setObjectName("dial_2")
        self.dialLayout.addWidget(self.dial_2)

        # Horizontal layout for the label and button to keep them the same size
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")

        self.label_tuner = QtWidgets.QLabel(self.centralwidget)
        self.label_tuner.setObjectName("label")
        self.buttonLayout.addWidget(self.label_tuner)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.buttonLayout.addWidget(self.pushButton)

        self.mainLayout.addLayout(self.top_row)
        self.mainLayout.addLayout(self.dialLayout)
        self.mainLayout.addLayout(self.buttonLayout)
        

        # Add the form layout to the main layout
        #self.mainLayout.addLayout(self.formLayout)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Guitar Pro"))
        self.label_connection.setText(_translate("MainWindow", "Connection Status"))
        self.label_tuner.setText(_translate("MainWindow", "Note"))
        self.pushButton.setText(_translate("MainWindow", "Click Me"))

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Set the window title and size policy
        self.setWindowTitle("Guitar Pro")
        self.setFixedSize(QSize(500, 500))  # Set a reasonable minimum size

        # Set size policies for resizable widgets
        self.label_connection.setFixedSize(500,50)
        self.dial.setFixedSize(250,250)
        self.dial_2.setFixedSize(250,250)
        self.label_tuner.setFixedSize(400,200)
        self.pushButton.setFixedSize(100,150)

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
