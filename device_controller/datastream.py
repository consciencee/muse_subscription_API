from muselsl import stream
from multiprocessing import set_start_method, Process
from collections import namedtuple

RUNNING = 1
STOPPED = 0
NON_INIT = -1

SensorPreset = namedtuple('SensorPreset', 'gyro_enabled acc_enabled ppg_enabled eeg_disabled')


class Datastream:
    def __init__(self, address, sensor_preset=SensorPreset(False, False, False, False)):
        self.process = None
        self.state = NON_INIT
        self.address = address
        self.sensor_preset = sensor_preset
        print("Created stream for %s" % address)

    def set_acc_enabled(self, enabled):
        self.sensor_preset = SensorPreset(
            self.sensor_preset.gyro_enabled,
            enabled,  # acc
            self.sensor_preset.ppg_enabled,
            self.sensor_preset.eeg_disabled
        )

    def set_gyro_enabled(self, enabled):
        self.sensor_preset = SensorPreset(
            enabled,  # gyro
            self.sensor_preset.acc_enabled,
            self.sensor_preset.ppg_enabled,
            self.sensor_preset.eeg_disabled
        )

    def set_ppg_enabled(self, enabled):
        self.sensor_preset = SensorPreset(
            self.sensor_preset.gyro_enabled,
            self.sensor_preset.acc_enabled,
            enabled,  # ppg
            self.sensor_preset.eeg_disabled
        )

    def set_eeg_enabled(self, enabled):
        self.sensor_preset = SensorPreset(
            self.sensor_preset.gyro_enabled,
            self.sensor_preset.acc_enabled,
            self.sensor_preset.ppg_enabled,
            not enabled  # eeg disabled
        )

    def start(self):
        self.process = Process(target=stream,
                               args=(
                                   self.address,  # address
                                   'auto',  # backend
                                   None,  # interface
                                   None,  # name
                                   self.sensor_preset.ppg_enabled,
                                   self.sensor_preset.acc_enabled,
                                   self.sensor_preset.gyro_enabled,
                                   self.sensor_preset.eeg_disabled
                               ))
        self.state = STOPPED
        self.process.start()
        self.state = RUNNING
        print("Running stream for %s" % self.address)

    def stop(self):
        self.process.terminate()
        self.state = STOPPED
