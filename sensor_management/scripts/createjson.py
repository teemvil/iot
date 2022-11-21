import json
import socket
import os
from datetime import datetime
from pathlib import Path

data_folder = Path("/etc/iotDevice/")  # Location needs to be declared


def create_device_json():
    # Structure of the device.json
    json_file = {
        "itemid": "",
        "hostname": socket.gethostname(),
        "event": "",
        "message": "",
        "timestamp": "",
        "address": get_ip_address(),
        "device": {
            "valid": False,
            "timestamp": ""
        },
        "sensor": {
            "name": "",
            "timestamp": "",
            "valid": False,
            "validtimestamp": ""
        }
    }

    file_name = "device.json"
    save_to_device(file_name, json_file)


def create_client_json():
    # Structure of the config.json
    client_file = {
        "host": "192.168.0.24",
        "port": 1883,
        "keepalive": 60
    }
    file_name = "config.json"
    save_to_device(file_name, client_file)


def get_ip_address():
    ip_address = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address


def save_to_device(write_to_file, file_to_be_written):
    json_object = json.dumps(file_to_be_written, indent=4)
    if os.path.isdir(data_folder) == False:
        os.mkdir(data_folder)
        print("Directory created")
        file_to_write = data_folder / write_to_file
        with open(file_to_write, "w") as outfile:
            outfile.write(json_object)
    else:
        print("The directory exist")
        file_to_write = data_folder / write_to_file
        with open(file_to_write, "w") as outfile:
            outfile.write(json_object)

# For testing purposes to check for the file existence


def open_json(file_to_open):
    with open(data_folder / file_to_open, 'r') as openfile:
        json_object = json.load(openfile)
        print(json_object)
    return json_object


create_device_json()
create_client_json()
open_json("device.json")
open_json("config.json")
