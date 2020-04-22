from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
import numpy as np
from seaborn import color_palette


class SensorWidget(QtWidgets.QWidget):
    def __init__(self, name='0'):
        super(SensorWidget, self).__init__()

        self.label = QtWidgets.QLabel(name)
        self.color_label = QtWidgets.QLabel('')
        self.data_label = QtWidgets.QLabel('0')

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.color_label)
        self.layout().addWidget(self.data_label)

        color = color_palette("RdBu_r", 11)

        self.quality_colors = color_palette("RdYlGn", 11)[::-1]

    def update_data(self, data):
        self.data_label.setText(str(data))
        col = self.quality_colors[int(data)]
        self.color_label.setStyleSheet("QLabel {background-color: rgb" + str(col) + ";}")

    def set_name(self, name):
        self.label.setText(name)


class SensorPane(QtWidgets.QWidget):
    def __init__(self, chnames):
        super(SensorPane, self).__init__()

        self.setLayout(QtWidgets.QVBoxLayout())

        self.sensors = []

        for name in chnames:
            sensor = SensorWidget(name)
            self.layout().addWidget(sensor)
            self.sensors.append(sensor)

    @pyqtSlot(np.ndarray)
    def update_data(self, data):
        for i in range(data.size):
            self.sensors[i].update_data(data[i])
