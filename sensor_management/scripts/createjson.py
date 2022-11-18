import json
import socket
import os
from datetime import datetime
from pathlib import Path

data_folder = Path("/etc/iotDevice/")
file_to_open = data_folder / "data_packet.json"

json_file = {
    "itemid": "",
    "hostname": "",
    "ip": "",
    "message": "",
    "event": "",
    "device": {
        "valid": False,
        "timestamp": ""
    },
    "sensor": {
        "name": "",
        "timestamp": ""
    },
    "timestamp": "",
    "client": {
        "host": "192.168.11.79",
        "port": 1883,
        "keepalive": 60
    }

}


def create_json():
    json_file["hostname"] = socket.gethostname()
    json_file["ip"] = get_ip_address()

    now = datetime.now()
    date_time = now.strftime("%d.%m.%Y, %H:%M:%S")

    #print("date and time:",date_time)

    #json_file["timestamp"]= date_time
    save_to_device()


def get_ip_address():
    ip_address = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address


def save_to_device():
    json_object = json.dumps(json_file, indent=4)
    if os.path.isdir(data_folder) == False:
        os.mkdir(data_folder)
        print("Directory created")
        file_to_write = data_folder / "data_packet.json"
        with open(file_to_write, "w") as outfile:
            outfile.write(json_object)
    else:
        print("The directory exist")
        file_to_write = data_folder / "data_packet.json"
        with open(file_to_write, "w") as outfile:
            outfile.write(json_object)


# For testing purposes to check for the file existence
"""
def open_json():
    with open(file_to_open, 'r') as openfile:    
        json_object = json.load(openfile)    
        #print(json_object)
        #print(type(json_object))
    return json_object
"""
create_json()
print(json_file)
print(json_file["device"]["valid"])
print(json_file["client"]["host"])

