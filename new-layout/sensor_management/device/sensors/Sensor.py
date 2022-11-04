from device.InitObject import InitObject
import json
import time
import math
import busio
import board
import adafruit_amg88xx
import time
import threading


class Sensor(InitObject):
    i2c = busio.I2C(board.SCL, board.SDA)
    amg = adafruit_amg88xx.AMG88XX(i2c)

    def __init__(self):
        super().__init__()

    def start_up(self):
        self.connect()
        self.client.publish('management', json.dumps(self.config))

        self.client.subscribe('management/iotpi014')
        self.client.on_message = self.on_message

        self.client.loop_forever()

    def measure(self):
        while True:
            #client.publish("sensor/temperature", payload=amg.temperature)
            #client.publish("pixel/temperature", payload=json.dumps(amg.pixels))

            mean = 0
            for column in self.amg.pixels:
                mean = sum(column) / len(self.amg.pixels)

            self.client.publish(
                "data/iotpi014/sensor/ir/pixels", payload=math.floor(mean))
            self.client.publish("data/iotpi014/sensor/ir/temperature",
                                payload=math.floor(mean))

            if mean > 24:
                self.client.publish("alert", payload="Hot!")
            time.sleep(2)


    def on_message(self, client, userdata, msg):
        x = threading.Thread(target=self.measure)
        x.start()
