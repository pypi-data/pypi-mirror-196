# iot-core

## Subscribe to MQTT Topic
```
import iotcore


def callback(payload):
    print(f"Received payload in python: {payload}")


core = iotcore.IotCore("mqtt.eclipseprojects.io", 1883, callback)
core.publish("pub/iotcore", "hello")
core.subscribe("sub/iotcore")
core.run()

```