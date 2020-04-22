from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
from gui.sensorspane import SensorPane


class MainPanel(QtWidgets.QWidget):
    def __init__(self):
        super(MainPanel, self).__init__()

        self.sensorPaneWidget = SensorPane(["a", "b", "c", "d", "e"])
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.sensorPaneWidget)