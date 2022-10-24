# Device Manager

This is the manager class which operates the pis. The main operation is starting the sensor processes and then keeping track of them. 

Pseudocode

```
Sensors = []
ip: str

on_change(msg)
  # Publish mqtt messages when needed.
  mqtt.publish(ip, msg)

start_sensor(n)
  sensor[n].measure_stuff()

start_sensors()
  sensor.forEach(measure_stuff())

kill_process(n)
  sensor[n].kill()

restart()
  pi.restart()

```