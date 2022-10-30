#!/bin/env python3
import paho.mqtt.client as mqtt
import socket
import json
import requests
import threading
import os

def setup():
    mgr = device_manager
    thread = threading.Thread(target=mgr.run)
    thread.start()

def start():
    client = mqtt.Client()
    client.connect('192.168.11.79')

    payload = {
        'hostname': socket.gethostname(),
        'operation': 'process-startup',
        'type': '',
        'ip': '123.123.123.123',
        'metadata': {

        }
    }

    client.publish('management', payload=json.dumps(payload))

    payload.update({'type': 'attest'})
    client.publish('management', payload=json.dumps(payload))


if __name__ == '__main__':
    setup()
    start()