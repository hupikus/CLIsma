import os
import fcntl


#reads all the devices from filepaths. Pahts are specified in devices arg.
class Device():

    def __init__(self, devices, controller):
        self.devices = {}
        self.controller = controller
        for path in devices:
            self.devices[path] = self.open(path)
        self.devicelist = list(self.devices.values())
        self.start()


    def start(self):
        pass

    def readevent(self):
        pass

    # in: path[]
    def edit(self, devices):
        newdevices = {}
        #newpaths = []
        for path in self.devices: #close removed
            device = self.devices[path]
            if path in devices:
                newdevices[path] = device
            else:
                self.close(device)
        self.devices = newdevices

        for path in devices: #open added
            if path not in self.devices:
                self.devices[path] = self.open(path)
                #newpaths.append(path)
        self.devicelist = list(self.devices.values())

    def lock(self, device, value):
        fcntl.ioctl(device, 0x40044590, int(value))

    # in: path; out: open() object
    def open(self, path):
        return os.open(path, os.O_RDONLY | os.O_NONBLOCK)

    # in: object
    def close(self, device):
        try:
            self.lock(device, 0)
        except: pass
        os.close(device)

    def abort(self):
        for device in self.devicelist:
            self.close(device)
