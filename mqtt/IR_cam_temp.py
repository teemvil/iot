import time
import busio
import board
import adafruit_amg88xx
import paho.mqtt.client as mqtt

i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)

client = mqtt.Client()
client.connect("192.168.11.79", 1883, 60)

while True:
    for row in amg.pixels:
        print(['{0:.1f}'.format(temp) for temp in row])
        print("")
    print("temp: ", amg.temperature)
    client.publish("image/temperature", payload=amg.temperature)
    print("\n")
    time.sleep(2)
