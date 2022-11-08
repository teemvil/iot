from device.sensors.Sensor import Sensor


class RngSensor(Sensor):
    def __init__(self):
        super().__init__()

    def measure_stuff(self):
        print('measure')
        print(self.config)

    def start():
        
