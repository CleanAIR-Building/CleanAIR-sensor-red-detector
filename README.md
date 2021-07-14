# Red Detector

This sensor detects if especially red objects are in front of it. It sends messages of the form:

``` json
{
  "sensor": <sensor name>,
  "state": ("HOT"|"COLD")
}
```
To the topic `sensors/infraRed`. The state `HOT` is sent when a red object appears and `COLD` is sent when a red object disappears from the camera image. This means a message is only sent when the state changes and not continuously. 

## Deployment

### Prerequisites
- Docker
- Docker compose
- Webcam

To deploy it on a x86_64 architecture run

``` bash
VIDEO_INPUT=<Path to Webcam> MQTT_HOST=<MQTT host> docker-compose up
```

To deploy it on ARM run

``` bash
VIDEO_INPUT=<Path to Webcam> MQTT_HOST=<MQTT host> docker-compose -f docker-compose-arm.yml up
```

If you want to deploy it on a Raspberry Pi and don't have Docker installed run

``` bash
./install-docker-rpi.sh
```

to install it.

You can also watch the evaluated video stream and the red parts of it under `localhost:5000`.
