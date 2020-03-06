from muselsl import list_muses
from .datastream import Datastream


class Device:
    def __init__(self, name="", address=""):
        self.name = name
        self.address = address
        self.stream = Datastream(address)


class Container:
    def __init__(self):
        self.devices = []

    def update_devlist(self):
        muses = list_muses()
        self.devices = []
        for muse in muses:
            self.devices.append(Device(name=muse['name'], address=muse['address']))

    def get_device(self, name):
        for device in self.devices:
            if device.name == name:
                return device
        print("Device %s not found" % name)
        return None

    def get_all_devices(self):
        return self.devices

