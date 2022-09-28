import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("connected with result code " + str(rc))

    client.subscribe("image/temperature")


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.11.79", 1883, 60)

client.loop_forever()
