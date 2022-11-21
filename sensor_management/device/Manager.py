from IoTElement import IoTElement
from datetime import datetime
import controller.attest as att
import json
import threading


class Manager(IoTElement):
    def __init__(self):
        super().__init__()

    def __attest_validate(self, json_update):
        # Attest validate needs to be determined how we do it
        json_object = json_update
        json_object["event"] = "validating device"
        json_object["message"] = "Device validation in process"
        self.client.publish(f"management/verify", json.dumps(json_object))

    def __on_connect(self, client, userdata, flags, rc):
        print("devmanager connected with result code " + str(rc))
        json_object = self.config
        json_object["message"] = "Sensor manager running"
        json_object["event"] = "starting sensor manager"
        json_object["timestamp"] = self.__get_time_stamp()
        self.client.publish("management", json.dumps(json_object))
        # print(json_object)

    def handle_management_message(self, client, userdata, msg):
        decoded_message = str(msg.payload.decode("utf-8"))
        json_object = json.loads(decoded_message)
        # print(json_object)

        if json_object["hostname"] == "iotpi012":
            print("iotpi12 functionality")
            # Here comes the specific functions for validation and all other necessary things like reset etc.

        if json_object["hostname"] == "iotpi014":
            print("iotpi14 functionality")
            # Here comes the specific functions for validation and all other necessary things like reset etc.

        if json_object["hostname"] == "iotpi015":
            print("iotpi15 functionality")
            # Here comes the specific functions for validation and all other necessary things like reset etc.

        if json_object["hostname"] == "iotpi016":
            print("iotpi16 functionality")
            obj = att.check_validity(json_object)
            print(obj)
            # Here comes the specific functions for validation and all other necessary things like reset etc.

    def __get_time_stamp(self):
        now = datetime.now()
        date_time = now.strftime("%d.%m.%Y, %H:%M:%S")
        return date_time

    def on_message(self, client, userdata, msg):
        x = threading.Thread(
            target=self.handle_management_message, args=(msg.payload, msg.topic))
        x.start()

    def run(self):
        self.client.subscribe('management')
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.on_message

        self.client.loop_forever()

    def __publish_datat(self, json_update):
        # Publish called when necessary
        self.client.publish("management", json_update)
