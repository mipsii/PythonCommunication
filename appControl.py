from PyQt5.QtWidgets import QFrame, QTableWidget, QSizePolicy
from PyQt5.QtCore import Qt, QRect
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor, QPainter


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(690, 411)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 370, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        
        
        self.stateSensorsFrame = QtWidgets.QFrame(Dialog)
        self.stateSensorsFrame.setGeometry(QtCore.QRect(530, 30, 141, 351))
        self.stateSensorsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.stateSensorsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.stateSensorsFrame.setObjectName("stateSensorsFrame")
    
        self.vertical_layout = QtWidgets.QVBoxLayout(self.stateSensorsFrame)
        # Dodajte QTableWidget za prikaz senzora
        self.circles = {}
        self.sensoresFrame = QFrame(Dialog)
        self.sensoresFrame.setObjectName(u"sensoresFrame")
        self.sensoresFrame.setGeometry(QRect(10, 30, 511, 81))
        self.sensoresFrame.setFrameShape(QFrame.StyledPanel)
        self.sensoresFrame.setFrameShadow(QFrame.Raised)
        self.nacrtajKrugove()
        
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(270, 10, 91, 18))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.controlFrame = QtWidgets.QFrame(Dialog)
        self.controlFrame.setGeometry(QtCore.QRect(10, 130, 171, 121))
        self.controlFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.controlFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.controlFrame.setObjectName("controlFrame")
        
        self.serverBox = QtWidgets.QCheckBox(self.controlFrame)
        self.serverBox.setGeometry(QtCore.QRect(30, 10, 111, 24))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.serverBox.setFont(font)
        self.serverBox.setObjectName("serverBox")
        self.plcBox = QtWidgets.QCheckBox(self.controlFrame)
        self.plcBox.setGeometry(QtCore.QRect(30, 40, 111, 24))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.plcBox.setFont(font)
        self.plcBox.setObjectName("plcBox")
        self.monitoringBox = QtWidgets.QCheckBox(self.controlFrame)
        self.monitoringBox.setGeometry(QtCore.QRect(30, 70, 111, 24))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.monitoringBox.setFont(font)
        self.monitoringBox.setObjectName("monitoringBox")
        self.runButton = QtWidgets.QPushButton(Dialog)
        self.runButton.setGeometry(QtCore.QRect(300, 190, 101, 61))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.runButton.setFont(font)
        self.runButton.setAutoExclusive(True)
        self.runButton.setObjectName("runButton")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def nacrtajKrugove(self):
        print("usao u def")
        painter = QPainter(self.sensoresFrame)
        painter.setRenderHint(QPainter.Antialiasing)
        circle_size = 30
        circle_spacing = 5
        x = 10
        y = 20
        
        for i in range(16):
            circle_name = f"circle_{i}"
            circle_color = QColor("black")  
            painter.setBrush(circle_color)
            painter.drawEllipse(x, y, circle_size, circle_size)
            self.circles[circle_name] = {"color": circle_color}  # Dodajemo informacije o krugu u rečnik
            x += circle_size + circle_spacing

    def changeCircleColor(self, circle_name, new_color):
        if circle_name in self.circles:
            self.circles[circle_name]["color"] = new_color
            self.update()  # Ponovno iscrtavanje prozora kako bi se promenila boja kruga
    
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Sensores"))
        self.serverBox.setText(_translate("Dialog", "Server"))
        self.plcBox.setText(_translate("Dialog", "PLC"))
        self.monitoringBox.setText(_translate("Dialog", "Monitoring"))
        self.runButton.setText(_translate("Dialog", "RUN"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
