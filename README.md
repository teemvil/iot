# MQTT topic naming conventions

Sensors are named as `sensor/webcam`, `sensor/ir`, `sensor/lux`, `sensor/tof`.

## Management channel
```
management/<sensor>
```

## Alert channel
```
alert/<sensor>
```

## Data channels
```
data/<sensor>/<unit>
```
Unit here means whe unit of measurement. This could be temperature or distance etc.