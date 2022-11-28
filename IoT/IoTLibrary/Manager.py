from IoTElement import IoTElement
from datetime import datetime
import attest as att
import json
import threading


class Manager(IoTElement):
    def __init__(self):
        super().__init__()

    def __on_connect(self, client, userdata, flags, rc):
        print("devmanager connected with result code " + str(rc))
        json_object = self.message
        json_object["message"] = "Manager running"
        json_object["event"] = "manager startup"
        json_object["timestamp"] = self.__get_time_stamp()
        self.client.publish("management", json.dumps(json_object))
        # print(json_object)

    def handle_management_message(self, client, userdata, msg):
        decoded_message = str(msg.payload.decode("utf-8"))
        json_object = json.loads(decoded_message)
        # print(json_object)
        if (json_object["event"] == "device startup"):
            valid_object = att.check_validity(json_object)
            if (valid_object["event"] == "device valdation ok"):
                self.__publish_datat(valid_object)
            else:
                json_object["event"] = "device validation fail"
                json_object["message"] = "Validation unsuccesfull"
                json_object["device"]["validtimestamp"] = self.__get_time_stamp()
                json_object["messagetimestamp"] = self.__get_time_stamp()
                self.__publish_datat(json_object)

        if (json_object["event"] == "sensor startup"):
            # att.check_sensor_validity(json_object)
            print("Sensor validation")

    def __get_time_stamp(self):
        now = datetime.now()
        date_time = now.strftime("%d.%m.%Y, %H:%M:%S")
        return date_time

    def on_message(self, client, userdata, msg):
        x = threading.Thread(
            target=self.handle_management_message(client, userdata, msg))
        x.start()

    def run(self):
        self.client.subscribe('management')
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.on_message
        self.client.loop_forever()

    def __publish_datat(self, json_update):
        # Publish called when necessary
        self.client.publish("management", json_update)
