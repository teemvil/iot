from SensorManagementSystem.IoTElement import IoTElement
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
        json_object["messagetimestamp"] = self.get_time_stamp()
        self.client.publish("management", json.dumps(json_object))
        # print(json_object)

    def handle_management_message(self, client, userdata, msg):
        decoded_message = str(msg.payload.decode("utf-8"))
        json_object = json.loads(decoded_message)
        # print(json_object)
        if (json_object["event"] == "device startup"):
            valid_object = att.check_validity(json_object)
            if (valid_object["event"] == "device validation ok"):
                valid_object["device"]["validtimestamp"] = self.get_time_stamp()
                valid_object["messagetimestamp"] = self.get_time_stamp()
                self.publish_data(json.dumps(valid_object))
            else:
                json_object["event"] = "device validation fail"
                json_object["message"] = "Validation unsuccesfull"
                json_object["messagetimestamp"] = self.get_time_stamp()
                self.publish_data(json.dumps(json_object))

        if (json_object["event"] == "sensor startup"):
            # att.check_sensor_validity(json_object)
            print("Sensor validation")

    def on_message(self, client, userdata, msg):
        x = threading.Thread(
            target=self.handle_management_message(client, userdata, msg))
        x.start()

    def run(self):
        self.client.subscribe('management')
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.on_message
        self.client.loop_forever()

    def publish_data(self, json_update):
        # Publish called when necessary
        self.client.publish("management", json_update)


if __name__ == "__main__":
    m = Manager()
    m.run()
