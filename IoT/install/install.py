import json
import socket
import os
from pathlib import Path

def create_device_config():
    # Structure of the device_config.json
    device_config = {
        "itemid": "",
        "hostname": socket.gethostname(),
        "address": get_ip_address(),
    }
    data_folder = Path("/etc/iotDevice/") 
    file_name = "device_config.json"
    save_to_device(data_folder, file_name, device_config)

def create_client_config():
    # Structure of the client_config.json
    client_config = {
        "host": "192.168.0.24",
        "port": 1883,
        "keepalive": 60
    }
    data_folder = Path("/etc/iotDevice/") 
    file_name = "client_config.json"
    save_to_device(data_folder, file_name, client_config)

def move_service_files():
    # Service files moved under systemd
    Path("/opt/iot/install/service_files/iot.devices.service").rename("/etc/systemd/system/iot.devices.service")
    print("devices.service creted in systemd")
    Path("/opt/iot/install/service_files/iot.sensors.service").rename("/etc/systemd/system/iot.sensors.service")
    print("sensors.service creted in systemd")

def get_ip_address():
    ip_address = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

def save_to_device(data_path, write_to_file, file_to_be_written):
    json_object = json.dumps(file_to_be_written, indent=4)
    if os.path.isdir(data_path) == False:
        os.mkdir(data_path)
        print("Directory created")
        file_to_write = data_path / write_to_file
        with open(file_to_write, "w") as outfile:
            outfile.write(json_object)
        print("Config created")
    else:
        print("Directory already exists")
        file_to_write = data_path / write_to_file
        with open(file_to_write, "w") as outfile:
            outfile.write(json_object)
        print("Config created")

if __name__ == "__main__":
    move_service_files()
    create_device_config()
    create_client_config()