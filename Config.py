import json
import os


class Config:
    def __init__(self):
        self.waitTime: float = 0.3
        self.maxLuminancePercentage: float = os.environ.get(
            "MAX_LUMINANCE_PERCENTAGE", 0.15)
        self.videoSource = os.environ.get("VIDEO_SOURCE", 0)
        self.webServerName: str = os.environ.get(
            "WEB_SERVER_NAME", "Video Feed")
        self.webServerHost: str = os.environ.get("WEB_SERVER_HOST", "0.0.0.0")
        self.webServerPort: str = os.environ.get("WEB_SERVER_PORT", "5000")
        self.mqttClientName: str = os.environ.get(
            "MQTT_CLIENT_NAME", "red-detection")
        self.mqttHost: str = os.environ.get("MQTT_HOST", "localhost")
        self.mqttPort: int = os.environ.get("MQTT_PORT", 1883)
        self.mqttKeepAlive: int = os.environ.get("MQTT_KEEP_ALIVE", 60)
        self.mqttClientUser: str = os.environ.get("MQTT_USER", "user1")
        self.mqttClientPassword: str = os.environ.get("MQTT_PASSWORD", "user1")
        self.deviceType: str = os.environ.get("DEVICE_TYPE", "RED_DETECTION")

    def printConfig(self):
        print("Config:")
        print(json.dumps(self.__dict__, indent=2, sort_keys=True), "\n")
