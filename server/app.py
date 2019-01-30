#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
import time
from senbay import SenbayFrame

app = Flask(__name__)
vc = cv2.VideoCapture(0)
# vc.set(cv2.CAP_PROP_FPS, 10)
# vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen():
    """Video streaming generator function."""
    sframe = SenbayFrame(qr_box_size = 5)
    while True:
        # content:
        # YOUR CODE IS HERE
        now = "V:3,TIME:"+str(time.time())

        # frame
        rval, frame = vc.read()
        frame = cv2.resize(frame, (640, 360))
        frame = cv2.flip(frame, 1)

        imencoded = cv2.imencode(".jpg", sframe.gen(frame=frame,data=now))[1]
        yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + imencoded.tostring() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
