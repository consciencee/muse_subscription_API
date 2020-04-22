from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
import numpy as np
from seaborn import color_palette


def qual_to_col(q):
    colors = [
        '#58ff33',
        '#9cff33',
        '#caff33',
        '#ecff33',
        '#fffc33',
        '#ffc133',
        '#ffa533',
        '#ff8633',
        '#ff6e33',
        '#ff3333',
        '#c70039',
    ]

    return colors[q] if q < len(colors) else '#ffffff'


class SensorWidget(QtWidgets.QWidget):
    def __init__(self, name='0'):
        super(SensorWidget, self).__init__()

        self.label = QtWidgets.QLabel(name)
        self.color_label = QtWidgets.QLabel('0')

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.color_label)

        self.color_label.resize(80, 80)
        self.color_label.setStyleSheet("border: 3px solid black;border - radius: 40px;")

    def update_data(self, data):
        col = qual_to_col(int(data))
        self.color_label.setText(str(data))
        self.color_label.setStyleSheet("QLabel { "
                                       "background-color: '" + str(col) + "';"
                                                                          "}")

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

    @pyqtSlot(np.ndarray, object)
    def update_data(self, data, channels):
        for i in range(data.size):
            self.sensors[i].update_data(data[i])
            self.sensors[i].set_name(channels.ch_names[i])
