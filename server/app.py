#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
import time
from senbay import SenbayFrame

app = Flask(__name__)
vc = cv2.VideoCapture(0)
# vc.set(cv2.CAP_PROP_FPS, 10)           # カメラFPSを60FPSに設定
# vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640) # カメラ画像の横幅を1280に設定
# vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 360) # カメラ画像の縦幅を720に設定

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen():
    """Video streaming generator function."""
    while True:
        # content
        now = time.time()
        # frame
        rval, frame = vc.read()
        frame = cv2.resize(frame, (640, 360))
        frame = cv2.flip(frame,1)
        height, width = frame.shape[:2]
        sframe = SenbayFrame(width, height, frame, str(now), qr_box_size = 5)
        imencoded = cv2.imencode(".jpg", sframe.gen())[1]
        yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + imencoded.tostring() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
