from flask import Flask, render_template, Response
from VideoFeed import VideoFeed
from RedDetector import RedDetector
from threading import Thread
import cv2
import time
import numpy as np


class WebServer:
    '''
    Class that controls the webserver that is used to monitor the camera.
    '''

    def __init__(self, name: str, host: str, port: int, videoFeed: VideoFeed, redDetector: RedDetector, waitTime: float = 0.3):
        self.videoFeed: VideoFeed = videoFeed
        self.redDetector: RedDetector = redDetector
        self.host: str = host
        self.port: int = port
        self.waitTime: float = waitTime
        self.server: Flask = Flask(name)

    def start(self):
        self.thread: Thread = Thread(target=self._start)
        self.thread.start()
        return self

    def stop(self):
        self.thread.stop()

    def _genFrames(self):
        while True:
            time.sleep(self.waitTime)
            ret, buffer = cv2.imencode('.jpg', np.concatenate(
                (self.videoFeed.frame, self. redDetector.frame), axis=1))
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')  # concat frame one by one and show result

    def _start(self):
        @self.server.route('/video')
        def video():
            # Video streaming route. Put this in the src attribute of an img tag
            return Response(self._genFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')

        @self.server.route('/')
        def index():
            """Video streaming home page."""
            return render_template('index.html')
        self.server.run(threaded=True, host=self.host, port=self.port)
