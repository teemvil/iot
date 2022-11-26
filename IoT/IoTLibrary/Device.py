from IoTLibrary.IoTElement import IoTElement
import json
import time
import datetime


class Device(IoTElement):
    def __init__(self):
        super().__init__()
    """
    Send device startup message to the management channel on the MQTT broker.
    """

    def startup(self):
        self.message["device"]["starttimestamp"] = self.get_time_stamp()
        self.message["event"] = "device startup"
        self.message["message"] = f"hello world. i'm {self.hostname}"

        self.client.subscribe("management")
        self.client.on_message = self.on_message
        self.client.loop_start()
        self.client.publish('management', json.dumps(self.message))

    """
    This one should probably be listening for management messages. The messages 
    tells this device what to do.
    """

    def on_message(self, client, nonetype, msg):
        print(
            f"Received message with topic: '{msg.topic}' and message: '{msg.payload.decode()}'")
