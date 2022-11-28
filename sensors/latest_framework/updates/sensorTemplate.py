from IoTLibrary.BasicSensor import BasicSensor
import time
# Import sensor/etc. specific dependencies

class N(BasicSensor): #Replace N with your chosen name
    # Sensor specific variables
    data = 1 # An example

    def __init__(self) -> None:
        super().__init__()

    def run(self):
        # Write your code here and inside the while-loop use self.publis_data to publish data
        while True:
            self.publish_data(self.data, self.prefix) # Use this method to publis data
            time.sleep(self.frequency) # Frequency determinded in sensor.config