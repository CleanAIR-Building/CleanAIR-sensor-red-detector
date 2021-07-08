#! /bin/python3

from HeartBeat import HeartBeat
from VideoFeed import VideoFeed
from RedDetector import RedDetector
from WebServer import WebServer
from Config import Config
from MQTTClient import MQTTClient

config: Config = Config()
mqttClient: MQTTClient = MQTTClient(
    config.mqttClientName,
    config.mqttClientUser,
    config.mqttClientPassword,
    config.mqttHost,
    config.mqttPort,
    config.mqttKeepAlive)

heartBeat: HeartBeat = HeartBeat(
    config.mqttClientName,
    config.deviceType,
    mqttClient)

videoFeed: VideoFeed = VideoFeed(
    config.videoSource,
    config.waitTime)

redDetector: RedDetector = RedDetector(
    videoFeed,
    mqttClient,
    config.waitTime,
    config.maxLuminancePercentage)

webServer: WebServer = WebServer(
    config.webServerName,
    config.webServerHost,
    config.webServerPort,
    videoFeed,
    redDetector,
    config.waitTime)


def main():
    config.printConfig()
    videoFeed.start()
    redDetector.start()
    webServer.start()
    mqttClient.connect()
    heartBeat.start()
    mqttClient.start()


if __name__ == '__main__':
    main()
