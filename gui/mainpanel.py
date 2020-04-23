from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import *
from gui.sensorspane import SensorPane
from gui.recordform import RecordForm

import os


class MainPanel(QtWidgets.QFrame):
    def __init__(self):
        super(MainPanel, self).__init__()

        self.sensorPaneWidget = SensorPane(["", "", "", "", ""])
        self.dataRecordWidget = RecordForm()
        self.dataRecordWidget.setObjectName('recordForm')
        self.sensorPaneWidget.setObjectName('sensorForm')
        self.setLayout(QtWidgets.QVBoxLayout())

        sensinfo_lbl = QtWidgets.QLabel("Sensor info")
        self.layout().addWidget(sensinfo_lbl)
        self.layout().setAlignment(sensinfo_lbl, Qt.AlignLeft)
        sensinfo_lbl.setProperty('class', 'header')

        self.layout().addWidget(self.sensorPaneWidget)
        self.layout().addWidget(QtWidgets.QLabel())

        datarec_lbl = QtWidgets.QLabel("Data recording")
        self.layout().addWidget(datarec_lbl)
        self.layout().setAlignment(datarec_lbl, Qt.AlignLeft)
        datarec_lbl.setProperty('class', 'header')

        self.layout().addWidget(self.dataRecordWidget)
        self.layout().setSpacing(0)

        self.setObjectName('mainForm')

        QtGui.QFontDatabase.addApplicationFont('gui/resources/Roboto-Light.ttf')
        QtGui.QFontDatabase.addApplicationFont('gui/resources/Roboto-Regular.ttf')

        qssFile = 'gui/resources/style.qss'
        with open(qssFile, 'r') as fh:
            self.setStyleSheet(fh.read())

        #print(QtGui.QFontDatabase.families())
