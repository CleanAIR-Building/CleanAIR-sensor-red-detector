import paho.mqtt.client as mqtt
import json


class MQTTClient:
    def __init__(self, name: str, user: str, password: str, host: str,  port: int = 1883, keepalive: int = 60):
        self.name: str = name
        self.host: str = host
        self.port: int = port
        self.user = user
        self.password = password
        self.keepalive: int = keepalive
        self.client: mqtt.Client = mqtt.Client(self.name)
        self.client.username_pw_set(self.user, self.password)

    def connect(self):
        self.client.connect(self.host, port=self.port,
                            keepalive=self.keepalive)

    def publish(self, topic: str, payload: dict):
        self.client.publish(topic, json.dumps(payload))
