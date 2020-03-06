from muselsl import stream
from multiprocessing import set_start_method, Process

RUNNING = 1
STOPPED = 0
NON_INIT = -1


class Datastream:
    def __init__(self, address):
        self.process = None
        self.state = NON_INIT
        self.address = address
        print("Created stream for %s" % address)

    def start(self):
        self.process = Process(target=stream, args=(self.address,))
        self.state = STOPPED
        self.process.start()
        self.state = RUNNING
        print("Running stream for %s" % self.address)

    def stop(self):
        self.process.terminate()
        self.state = STOPPED
