from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import numpy as np
import sys  # We need sys so that we can pass argv to QApplication
import os


class BaseChart(QtWidgets.QWidget):
    def __init__(self, y_name="", x_name="", color=(0, 0, 0), maxpoints=10000):
        super(BaseChart, self).__init__()

        self.chartWidget = pg.PlotWidget()
        self.chartWidget.setLabel('left', y_name, color=color)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.chartWidget)

        self.chartWidget.setBackground('w')
        self.maxpoints = maxpoints

        self.x = np.zeros(maxpoints)
        self.y = np.zeros(maxpoints)

        self.chart_data = self.chartWidget.plot(self.x, self.y, pen=pg.mkPen(color=color))

    @pyqtSlot('double')
    def on_data_update(self, data):
        leastx = self.x[-1]
        self.x[0:-1] = self.x[1:]
        self.y[0:-1] = self.y[1:]
        self.x[self.maxpoints - 1] = leastx + 1
        self.y[self.maxpoints - 1] = data
        # if len(self.x) == self.maxpoints:
        #     self.x = self.x[1:]
        #     self.y = self.y[1:]
        # self.x = np.append(self.x, self.x[-1]+1)
        # self.y = np.append(self.y, data)
        # self.x.append(self.x[-1] + 1)
        # self.y.append(data)
        self.chart_data.setData(self.x, self.y)
