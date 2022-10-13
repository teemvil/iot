# MQTT topic naming conventions

Sensors are named as `sensor/webcam`, `sensor/ir`, `sensor/lux`, `sensor/tof`.

## Management channel
```
management/<device>/<sensor>
```

## Alert channel
```
alert/<device>/<sensor>
```

## Data channels
```
data/<device>/<sensor>/<mesurement>
```
Measurement here means the measured data. This could be array of pixels, temperature, distance etc
