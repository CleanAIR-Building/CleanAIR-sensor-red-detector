from MQTTClient import MQTTClient
from threading import Thread
import time


class HeartBeat:
    """
    Class that continuously sends heartbeats over the mqtt.
    """
    TOPIC: str = "heartbeat"

    def __init__(self, mqttClientName: str, deviceType: str, mqttClient: MQTTClient, interval: float = 5):
        self.mqttClient = mqttClient
        self.mqttClientName = mqttClientName
        self.deviceType = deviceType
        self.interval = interval
        self.stopped: bool = False

    def start(self):
        thread = Thread(target=self._get)
        thread.start()
        return self

    def stop(self):
        self.stopped = True

    def _get(self):
        while not self.stopped:
            time.sleep(self.interval)
            self.mqttClient.publish(
                HeartBeat.TOPIC, {"name": self.mqttClientName, "type": self.deviceType})
