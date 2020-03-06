import matplotlib
from muselsl import stream, list_muses, view
#import pyqt5

from device_controller import container

#matplotlib.use("Qt5Agg")

#list devices
devices = container.Container()
devices.update_devlist()

#get single muse device
single_muse = devices.get_all_devices()[0]
single_muse.stream.start()

view(backend="Qt5Agg")
