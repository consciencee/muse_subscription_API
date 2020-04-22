from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import numpy as np
from threading import Thread

from .basechart import BaseChart

color_set = [
    "#0048ba",
    "#af002a",
    "#84de02",
    "#8000ff",
    "#ff8000"
]


class MultiChart(QtWidgets.QWidget):
    chart_data_update = pyqtSignal('double')

    def __init__(self, y_names, maxpoints=100):
        super(MultiChart, self).__init__()

        self.setLayout(QtWidgets.QVBoxLayout())

        self.colors = color_set
        self.charts = []

        for y_name in y_names:
            chart = BaseChart(y_name=y_name, color=self.colors.pop(), maxpoints=maxpoints)
            self.layout().addWidget(chart)
            self.charts.append(chart)
            self.chart_data_update.connect(chart.on_data_update)
            #break

    @pyqtSlot(np.ndarray)
    def on_data_update(self, data):
        for i in range(data.size):
            # self.chart_data_update.emit(sample_list[i])
            t = Thread(target=self.charts[i].on_data_update, args=(data[i],))
            t.start()
        # for sample_list in data:
        #     for i in range(sample_list.size):
        #         #self.chart_data_update.emit(sample_list[i])
        #         t = Thread(target=self.charts[i].on_data_update, args=(sample_list[i],))
        #         t.start()
                #self.charts[i].on_data_update(sample_list[i])
                #break
                #self.charts[i].on_data_update(sample_list[i])
