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

        slice(self.sample_rate)

    def slice(self, last_n_samples):
        if last_n_samples < self.buffer.size():
            self.buffer = self.buffer[-last_n_samples]

    def calc_quality(self):
        sd = np.std(self.buffer, axis=0)
        return sd
