import matplotlib
from muselsl import stream, list_muses, view
#import pyqt5

from device_controller import container
from device_controller.datareceiver import Datareceiver, eeg_preset, gyro_preset, acc_preset


class TestSubscriber:
    def __init__(self):
        self.buffer = []
        self.time_buffer = []

    def on_event(self, evtype, data, timestamp):
        print('%s received time: %s data: %s' % (evtype, timestamp, data))
        self.buffer.append(data)
        self.time_buffer.append(timestamp)


#list devices
devices = container.Container()
devices.update_devlist()

#get single muse device
single_muse = devices.get_all_devices()[0]
single_muse.stream.start()

receiver = Datareceiver(settings=eeg_preset)
acc_receiver = Datareceiver(settings=acc_preset)
subscriber = TestSubscriber()
receiver.subscription.add_subscriber(subscriber)
acc_receiver.subscription.add_subscriber(subscriber)
receiver.receive_parallel()
acc_receiver.receive_parallel()

# receive is not working with view
#view(backend="Qt5Agg")
