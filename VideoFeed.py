from threading import Thread
import cv2
import numpy as np
import time


class VideoFeed:
    """
    Class that continuously gets frames from a VideoCapture object with a dedicated thread.
    """

    def __init__(self, src=0, waitTime: float = 0.3):
        self.stream = cv2.VideoCapture(src)
        result_grabbed, result_frame = self.stream.read()
        self.grabbed: bool = result_grabbed
        self.frame: np.array = result_frame
        self.waitTime: float = waitTime
        self.stopped: bool = False

    def start(self):
        thread = Thread(target=self._get)
        thread.start()
        return self

    def stop(self):
        self.stopped = True

    def _get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                time.sleep(self.waitTime)
                result_grabbed, result_frame = self.stream.read()
                self.grabbed = result_grabbed
                self.frame = cv2.flip(result_frame, 1)
