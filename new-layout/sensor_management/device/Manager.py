from device.InitObject import InitObject
import paho.mqtt.client as mqtt
import threading
from datetime import datetime
import os
import json
import socket


class Manager(InitObject):
    def __init__(self):
        super().__init__()

    def start_devmngr(self, json_update, client):
        json_object = json_update
        json_object["message"] = "Device manager started"
        json_object["event"] = "dvmngr_start"
        json_object["timestamp"] = self.get_time_stamp()
        # print(json_object)
        client.publish(f"management", json.dumps(json_object))
        self.attest_validate(json_object)

    def attest_validate(self, json_update):
        json_object = json_update
        json_object["event"] = "validating device"
        json_object["message"] = "Device validation in process"
        self.client.publish(f"management/verify", json.dumps(json_object))

    # def on_connect(self, client, userdata, flags, rc):
    #     print("connected with result code " + str(rc))
    #     client.subscribe("management")

    def sensor_start(self, json_update):
        json_object = json_update
        json_object["message"] = "Device manager starting device"
        json_object["event"] = "sensorstart"
        json_object["timestamp"] = self.get_time_stamp()
        print("Sensor start")
        # os.system("python3 /home/metropolia/rangetest/sensors/*.py")

        self.client.publish(f"management", json.dumps(json_object))

    def process_message(self, payload, topic):
        print(topic+" "+str(payload))
        # Funcitonality for restart and reboot comes here


    def on_message(self, client, userdata, msg):
        decoded_message = str(msg.payload.decode("utf-8"))
        json_object = json.loads(decoded_message)

        print(json_object)

        # startup.sh antaa event tietona startup
        if (msg.topic == "management" and json_object["hostname"] == socket.gethostname()):

            if (msg.topic == "management" and json_object["event"] == "startup"):
                self.start_devmngr(json_object, client)

            if (msg.topic == "management" and json_object["event"] == "validation ok" and json_object["device"]["valid"] == True):
                # x = threading.Thread(target=self.process_message,
                #                      args=(msg.payload, msg.topic))
                # x.start()

                client.publish("management/iotpi014", json.dumps({"start": "sensor"}))
                # self.sensor_start(json_object)
            else:
                json_object["message"] = "Device validation error"
                json_object["event"] = "dev_val_error"
                json_object["timestamp"] = self.get_time_stamp()
                #client.publish(f"management", json.dumps(json_object))
        """        
        if (msg.topic == "management" and json_object["hostname"]!=socket.gethostname())
            json_object["message"]="Device host names does not match"
            json_object["event"]="dev_name_error"
            json_object["timestamp"]=get_time_stamp()
            client.publish(f"alert", "Device host names does not match")
            client.publish(f"management", json.dumps(json_object))
        """

    def get_time_stamp(self):
        now = datetime.now()
        date_time = now.strftime("%d.%m.%Y, %H:%M:%S")
        return date_time

    def run(self):
        self.connect()

        self.client.subscribe('management')
        # self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.loop_forever()