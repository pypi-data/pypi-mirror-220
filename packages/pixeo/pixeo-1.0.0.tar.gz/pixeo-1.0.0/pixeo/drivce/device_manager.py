class DeviceManager:
    def __init__(self):
        self.devices = {}

    def add_device(self, device):
        device_type = device.get_device_type()
        if device_type not in self.devices:
            self.devices[device_type] = device

    def get_device(self, device_type):
        return self.devices.get(device_type, None)
