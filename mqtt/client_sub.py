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
    # while True:
    #     status,pixels = sensor.read_temp(pix_to_read) # read pixels with status
    #     if status: # if error in pixel, re-enter loop and try again
    #         continue
    
    #     #timer how often it checks the temperature
    #     time.sleep(1)

    #     T_thermistor = sensor.read_thermistor() # read thermistor temp
    #     # fig.canvas.restore_region(ax_bgnd) # restore background (speeds up run)
    #     # im1.set_data(np.reshape(pixels,pix_res)) # update plot with new temps
    #     # ax.draw_artist(im1) # draw image again
    #     # fig.canvas.blit(ax.bbox) # blitting - for speeding up run
    #     # fig.canvas.flush_events() # for real-time plot
    #     client.publish("image/temperature", T_thermistor)
    #     # print("Thermistor Temperature: {0:2.2f}".format(T_thermistor)) # print thermistor temp