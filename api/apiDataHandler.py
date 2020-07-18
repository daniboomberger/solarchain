from api.config import api_channel

class apiDataHandler():
    
    def __init__(self):
        self.consumption = []
        self.devices = []

    def handleDevices(self, data):
        device_names = []
        for device in data["header"]["epoch_devices"]:
            epoch = device

        names = data["header"]["epoch_devices"][epoch]
        for i in range(0, len(names) - 2):
            device_names.append(names[str(i + 1)]["name"])
        
        self.devices = device_names

    def handleConsumption(self, data, date_time):
        string_datetime = str(date_time)
        device_counter = 0
        apartment_consumption = {}

        for entry in data["body"][string_datetime]:
            if device_counter < len(self.devices):
                consumption_amount = data["body"][string_datetime][entry][api_channel]
                apartment_consumption[self.devices[device_counter]] = consumption_amount
                device_counter = device_counter + 1
        return apartment_consumption, self.devices

        
