import numpy as np


class QualityChecker:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self.buffer = None

    def append(self, samples):
        samples = np.array(samples)[:, ::-1]  # just convert to np
        if self.buffer is None:
            self.buffer = samples
        else:
            self.buffer = np.vstack([self.buffer, samples])

        self.slice(int(self.sample_rate))

    def slice(self, last_n_samples):
        if last_n_samples < self.buffer.size:
            self.buffer = self.buffer[-last_n_samples:]

    def calc_quality(self):
        #print('mean', self.buffer.mean(axis=0))
        #print('normalized', self.buffer - self.buffer.mean(axis=0))
        sd = np.std((self.buffer - self.buffer.mean(axis=0)) / 500, axis=0) * 500

        co = np.int32(np.tanh((sd - 30) / 15) * 5 + 5)
        return co
