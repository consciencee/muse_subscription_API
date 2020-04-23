import pathlib

class FileWriter:
    def __init__(self):
        self.fh = None

    def open(self, dirname, filename):
        self.fh = open(str(pathlib.Path(dirname) / filename), 'w+')

    def append(self, data):
        for sample in data:
            self.fh.write(', '.join(map(str, sample)) + '\n')

    def close(self):
        self.fh.close()