import pathlib

class FileWriter:
    def __init__(self):
        self.fh = None

    def open(self, dirname, filename):
        self.fh = open(str(pathlib.Path(dirname) / filename), 'w+')

    def append(self, data, timestamp):
        for i in range(len(data)):
            self.fh.write(str(timestamp[i]) + ', ' + ', '.join(map(str, data[i])) + '\n')

    def close(self):
        self.fh.close()