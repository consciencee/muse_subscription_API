import matplotlib
from muselsl import stream, list_muses, view, viewer_v2
# import pyqt5

from device_controller import container
from device_controller.datareceiver import Datareceiver, eeg_preset, gyro_preset, acc_preset
from plugins.sensor_quality import QualityChecker


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
        if evtype == eeg_preset.type:
            if self.qualityChecker is None:
                self.qualityChecker = QualityChecker(channel.sample_rate)
            self.qualityChecker.append(data)
            print('Quality:')
            print(self.qualityChecker.calc_quality())


# list devices
devices = container.Container()
devices.update_devlist()

# get single muse device
single_muse = devices.get_all_devices()[0]
single_muse.stream.start()

receiver = Datareceiver(settings=eeg_preset)
subscriber = ChannelSubscriber()
receiver.subscription.add_subscriber(subscriber)
#receiver.receive_parallel()
receiver.receive()

# receive is not working with view
# view(backend="Qt5Agg")

# viewer_v2.view()
