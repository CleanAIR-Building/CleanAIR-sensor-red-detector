import paho.mqtt.client as mqtt
import json
import time


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
        self.client.reconnect_delay_set(min_delay=1, max_delay=5)

    def connect(self):
        while True:
            try:
                self.client.connect(self.host,
                                    port=self.port,
                                    keepalive=self.keepalive)
                return
            except Exception:
                print(".", end='', flush=True)
                time.sleep(1)

    def publish(self, topic: str, payload: dict):
        self.client.publish(topic, json.dumps(payload))

    def start(self):
        self.client.loop_forever()
