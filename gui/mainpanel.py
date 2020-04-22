from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
from gui.sensorspane import SensorPane
from gui.recordform import RecordForm


class MainPanel(QtWidgets.QWidget):
    def __init__(self):
        super(MainPanel, self).__init__()

        self.sensorPaneWidget = SensorPane(["", "", "", "", ""])
        self.dataRecordWidget = RecordForm()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(QtWidgets.QLabel("Sensor info"))
        self.layout().addWidget(self.sensorPaneWidget)
        self.layout().addWidget(QtWidgets.QLabel())
        self.layout().addWidget(QtWidgets.QLabel("Data recording"))
        self.layout().addWidget(self.dataRecordWidget)