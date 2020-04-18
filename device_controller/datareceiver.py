from muselsl.constants import LSL_SCAN_TIMEOUT, LSL_EEG_CHUNK, LSL_PPG_CHUNK, LSL_ACC_CHUNK, LSL_GYRO_CHUNK
from pylsl import StreamInlet, resolve_byprop
from collections import namedtuple
from time import time, sleep, strftime, gmtime
import threading
from .subscription import Subscription
import numpy as np
import pandas as pd

Preset = namedtuple('Preset', 'type chunk')

eeg_preset = Preset('EEG', LSL_EEG_CHUNK)
ppg_preset = Preset('PPG', LSL_PPG_CHUNK)
acc_preset = Preset('ACC', LSL_ACC_CHUNK)
gyro_preset = Preset('GYRO', LSL_GYRO_CHUNK)

ChannelDescriptor = namedtuple('ChannelDescriptor', 'type ch_names sample_rate')


class Datareceiver:
    def __init__(self, settings=eeg_preset):
        self.settings = settings
        self.subscription = Subscription()
        # self.n_channels = None
        # self.sample_rate = None
        # self.channels = []

    def receive_parallel(self):
        process = threading.Thread(target=self.receive)
        process.start()
        return process

    def receive(self):
        streams = resolve_byprop('type', self.settings.type, timeout=LSL_SCAN_TIMEOUT)

        if len(streams) == 0:
            print("Can't find %s stream." % self.settings.type)
            return

        print("Started acquiring data.")
        inlet = StreamInlet(streams[0], max_chunklen=self.settings.chunk)

        info = inlet.info()
        description = info.desc()
        n_channels = info.channel_count()

        ch = description.child('channels').first_child()
        ch_names = [ch.child_value('label')]
        for i in range(1, n_channels):
            ch = ch.next_sibling()
            ch_names.append(ch.child_value('label'))


        channel_descriptor = ChannelDescriptor(self.settings.type, ch_names, info.nominal_srate())

        res = []
        timestamps = []
        t_init = time()
        time_correction = inlet.time_correction()
        print('Start recording at time t=%.3f' % t_init)
        print('Time correction: ', time_correction)

        while (time() - t_init) < 5000:
            try:
                data, timestamp = inlet.pull_chunk(timeout=1.0,
                                                   max_samples=self.settings.chunk)

                if timestamp:
                    res.append(data)
                    self.subscription.notify_all_subscribers(self.settings.type, data, timestamp, channel_descriptor)
                    timestamps.extend(timestamp)
            except KeyboardInterrupt:
                break

        time_correction = inlet.time_correction()
        print('Time correction: ', time_correction)

        res = np.concatenate(res, axis=0)
        timestamps = np.array(timestamps) + time_correction

        print('Done .')
