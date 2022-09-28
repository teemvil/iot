import paho.mqtt.client as mqtt


def publish(payload):
    def on_connect(client, userdata, flags, rc):
        print("connected with result code " + str(rc))
    
        client.publish("image/temperature", payload=payload)


    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("192.168.11.79", 1883, 60)
    client.loop_forever()
