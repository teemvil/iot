from .IoTElement import IoTElement
import json
import time
import datetime


class Device(IoTElement):
    def __init__(self):
        super().__init__()

        self.device_config = self.read_config_file("device_config.json")
        self.itemid = self.device_config["itemid"]
        self.hostname = self.device_config["device"]["hostname"]
        self.address = self.device_config["device"]["address"]

        self.message["device"]["itemid"] = self.itemid
        self.message["device"]["hostname"] = self.hostname
        self.message["device"]["address"] = self.address


        self.startup()

        try:
            while True:
                #self.client.publish("management", json.dumps({'message': 'doing stuff'}))
                print("doing stuff")
                time.sleep(1)
        # TODO: Specify an exception class to catch or reraise the exception...:q
        except:
            print("Exception during while loop, exiting...")
            self.client.loop_stop()
            self.client.disconnect()

    def startup(self):
        self.message["device"]["starttimestamp"] = self.__get_time_stamp()
        self.message["event"] = "device startup"
        self.message["message"] = f"hello world. i'm {self.hostname}"

        self.client.subscribe("management")
        self.client.on_message = self.on_message
        self.client.loop_start()
        self.client.publish('management', json.dumps(self.message))

    def on_message(self, client, nonetype, msg):
        print(
            f"Received message with topic: '{msg.topic}' and message: '{msg.payload.decode()}'")

    def __get_time_stamp(self):
        now = datetime.now()
        date_time = now.strftime("%d.%m.%Y, %H:%M:%S")
        return date_time