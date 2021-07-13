from MQTTClient import MQTTClient
import time
from VideoFeed import VideoFeed
from threading import Thread
import cv2
import numpy as np
from VideoFeed import VideoFeed
from enum import Enum
import time


class RedDetector:
    '''
    Class that continuously gets frames from a VideoFeed object and detects the red parts in them.
    '''

    class State(Enum):
        COLD = 0,
        HOT = 1,
        UNDETERMINED = 2

    FONT = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE: int = 1
    FONT_COLOR: tuple = (255, 255, 255)
    LINE_TYPE: int = 2
    POSITION: tuple = (50, 450)

    def __init__(self, videoFeed: VideoFeed, mqttClient: MQTTClient, waitTime: float = 0.3, maxLuminancePercentage: float = 0.15):
        self.videoFeed: VideoFeed = videoFeed
        self.mqttClient: MQTTClient = mqttClient
        self.stopped: bool = False
        self.waitTime: float = waitTime
        self.maxLuminancePercentage: float = maxLuminancePercentage
        self.state: RedDetector.State = RedDetector.State.UNDETERMINED

    def start(self):
        thread: Thread = Thread(target=self._detect)
        thread.start()
        return self

    def stop(self):
        self.stopped = True

    def _detect(self):
        threshold: float = self._calculateThreshold(
            self.videoFeed.frame, self.maxLuminancePercentage)
        while not self.stopped:
            time.sleep(self.waitTime)
            self.frame: np.array = self._detectRed(self.videoFeed.frame)
            luminance: float = self._calcLuminance(self.frame)[0]
            newState: RedDetector.State = self._detectState(
                luminance, threshold)
            self._changeStateIfNecessary(newState)
            self._writeOnImage(self.frame, str(luminance))

    def _calculateThreshold(self, image: np.array, percentage: float):
        shape: tuple = image.shape
        height: int = shape[0]
        width: int = shape[1]
        return height * width * 255 * percentage

    def _calcLuminance(self, image):
        return cv2.sumElems(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))

    def _writeOnImage(self, image: np.array, text: str):
        cv2.putText(image,
                    text,
                    RedDetector.POSITION,
                    RedDetector.FONT,
                    RedDetector.FONT_SCALE,
                    RedDetector.FONT_COLOR,
                    RedDetector.LINE_TYPE)

    def _detectRed(self, image: np.array):
        hsv: np.array = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        red_mask1: np.array = cv2.inRange(hsv, np.array(
            [0, 70, 50]), np.array([10, 255, 255]))
        red_mask2: np.array = cv2.inRange(hsv, np.array(
            [170, 70, 50]), np.array([180, 255, 255]))
        mask: np.array = cv2.bitwise_or(red_mask1, red_mask2)
        red_color: np.array = cv2.bitwise_and(image, image, mask=mask)
        kernel = np.ones((5, 5), np.uint8)
        red_color = cv2.dilate(red_color, kernel, iterations=5)
        return red_color

    def _detectState(self, luminance: float, threshold: float):
        if luminance > threshold:
            return RedDetector.State.HOT
        return RedDetector.State.COLD

    def _changeStateIfNecessary(self, newState: State):
        if self.state is not newState:
            self.state = newState
            self.mqttClient.publish(
                "sensors/infraRed", {"sensor": self.mqttClient.user, "state": str(self.state)})
