import pathlib

class FileWriter:
    def __init__(self):
        self.fh = None
        self.headers_written = False

    def open(self, dirname, filename):
        self.fh = open(str(pathlib.Path(dirname) / filename), 'w+')
        self.headers_written = False

    def append(self, data, timestamp, headers):
        if not self.headers_written:
            self.fh.write('Timestamp, ' + ', '.join(map(str, headers)) + '\n')
            self.headers_written = True
        for i in range(len(data)):
            self.fh.write(str(timestamp[i]) + ', ' + ', '.join(map(str, data[i])) + '\n')

    def close(self):
        self.fh.close()