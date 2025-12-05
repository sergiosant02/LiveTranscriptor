import sounddevice as sd

class DeviceProvider:
    
    @staticmethod
    def get_available_devices():
        return [(i["index"], i["name"]) for i in sd.query_devices()] # remember 'name' and 'index'