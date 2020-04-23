from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
from gui.charts.multiplecharts import MultiChart
from gui.sensorspane import SensorPane
from gui.mainpanel import MainPanel
from threading import Thread

from device_controller import container
from device_controller.datareceiver import Datareceiver, eeg_preset, gyro_preset, acc_preset
from plugins.sensor_quality import QualityChecker
from plugins.filewriter import FileWriter

import numpy as np

from multiprocessing import set_start_method, Process

class ChannelSubscriber:
    def __init__(self):
        self.buffer = []
        self.time_buffer = []
        self.qualityChecker = None

    def on_event(self, evtype, data, timestamp, channel):
        #print('%s received time: %s data: %s' % (evtype, timestamp, data))
        print(channel)
        self.buffer.append(data)
        self.time_buffer.append(timestamp)
        # if evtype == eeg_preset.type:
        #     if self.qualityChecker is None:
        #         self.qualityChecker = QualityChecker(channel.sample_rate)
        #     self.qualityChecker.append(data)
        #     print('Quality:')
        #     print(self.qualityChecker.calc_quality())


class MuseRunner:
    def __init__(self):
        self.receiver = None

    def run(self):
        # list devices
        devices = container.Container()
        devices.update_devlist()

        # get single muse device
        single_muse = devices.get_all_devices()[0]
        single_muse.stream.start()

        self.receiver = Datareceiver(settings=eeg_preset)
        # subscriber = ChannelSubscriber()
        # self.receiver.subscription.add_subscriber(subscriber)
        # receiver.subscription.add_subscriber(subs)
        self.receiver.receive_parallel()

    def add_subscriber(self, subscriber):
        self.receiver.subscription.add_subscriber(subscriber)

class MuseQtHandler(QObject):

    data_received = pyqtSignal(np.ndarray)
    quality_received = pyqtSignal(np.ndarray, object)

    def __init__(self):
        super(MuseQtHandler, self).__init__()
        self.obj = None
        self.qualityChecker = None
        self.fileRecorder = FileWriter()
        self.is_recording = False

    def set_handling_obj(self, obj):
        self.obj = obj
        obj.add_subscriber(self)

    def start_record(self, dirname, filename):
        self.fileRecorder.open(dirname, filename)
        self.is_recording = True

    def stop_record(self):
        self.is_recording = False
        self.fileRecorder.close()

    def on_event(self, evtype, data, timestamp, channel):
        if self.qualityChecker is None:
            self.qualityChecker = QualityChecker(channel.sample_rate)
        self.qualityChecker.append(data)
        qualified_data = self.qualityChecker.calc_quality()
        # print('Quality:')
        # print(self.qualityChecker.calc_quality())
        self.quality_received.emit(qualified_data, channel)

        if self.is_recording:
            self.fileRecorder.append(data, timestamp)

class MainWindow(QtWidgets.QMainWindow):

    update_charts_data = pyqtSignal(np.ndarray)

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.chartWidget = MultiChart(["a", "b", "c", "d", "e"])
        # self.sensorPaneWidget = SensorPane(["a", "b", "c", "d", "e"])
        # self.setLayout(QtWidgets.QVBoxLayout())
        # self.layout().addWidget(self.sensorPaneWidget)
        self.mainPanel = MainPanel()
        self.setCentralWidget(self.mainPanel)
        #self.setCentralWidget(self.chartWidget)
        #self.update_charts_data.connect(self.chartWidget.on_data_update)

        self.mhandler = MuseQtHandler()
        self.mhandler.data_received.connect(self.update_charts_data)
        self.mhandler.quality_received.connect(self.mainPanel.sensorPaneWidget.update_data)

        self.mainPanel.dataRecordWidget.start_record.connect(self.mhandler.start_record)
        self.mainPanel.dataRecordWidget.stop_record.connect(self.mhandler.stop_record)

        # self.m_runner = MuseRunner()
        # self.m_runner.start()

        # self.init_muse()

        # process = Process(target=self.init_muse)
        # process.start()

    def on_event(self, evtype, data, timestamp, channel):
        print('%s received time: %s data: %s' % (evtype, timestamp, data))
        print(channel)
        if evtype == eeg_preset.type:
            self.update_charts_data.emit(data)
            # upd_process = Thread(target=self.chartWidget.on_data_update, args=(data,))
            # upd_process.start()
          #self.chartWidget.on_data_update(data)
        # if self.qualityChecker is None:
        #     self.qualityChecker = QualityChecker(channel.sample_rate)
        # self.qualityChecker.append(data)
        # print('Quality:')
        # print(self.qualityChecker.calc_quality())


def main():
    mrunner = MuseRunner()
    mrunner.run()
    #init_muse(0)
    app = QtWidgets.QApplication(sys.argv)


    mainw = MainWindow()
    mainw.mhandler.set_handling_obj(mrunner)
    # subscr = ChannelSubscriber()
    # mrunner.subscribe_stream(subscr)
    #mrunner.subscribe_stream(mainw)
    mainw.show()
    #init_muse(mainw)
    #init_muse(0)
    sys.exit(app.exec_())


def init_muse(subs):
    # list devices
    devices = container.Container()
    devices.update_devlist()

    # get single muse device
    single_muse = devices.get_all_devices()[0]
    single_muse.stream.start()

    receiver = Datareceiver(settings=eeg_preset)
    subscriber = ChannelSubscriber()
    receiver.subscription.add_subscriber(subscriber)
    # receiver.subscription.add_subscriber(subs)
    receiver.receive_parallel()


if __name__ == '__main__':
    main()
