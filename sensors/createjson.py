import json
import socket
import os
from datetime import datetime
from pathlib import Path

data_folder = Path("/etc/iotDevice/")

json_file = {
    "itemid": "",
    "hostname": "",
    "ip": "",
    "operation": "",
    "timestamp": ""
}

def create_json ():
    json_file["hostname"]=socket.gethostname()
    json_file["ip"]=get_ip_address()

    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time = now.strftime("%H:%M:%S")
    date_time = now.strftime("%d.%m.%Y, %H:%M:%S")

    #print("date and time:",date_time)	

    json_file["timestamp"]= date_time
    save_to_device()

def get_ip_address():
    ip_address = '';
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

def save_to_device ():
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
       
create_json()
print(json_file)