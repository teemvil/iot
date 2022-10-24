import paho.mqtt.client as mqtt
import sys

IP=sys.argv[1]
PORT=1883

# This is just a testing function. It listens to changes in the topic given to the
# client.subscirbe() function.
def on_connect(client, userdata, flags, rc):
    print("connected with result code " + str(rc))

    client.subscribe("management")


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(IP, PORT, 60)

client.loop_forever()
