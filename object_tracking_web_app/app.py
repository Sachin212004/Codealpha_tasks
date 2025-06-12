from flask import Flask, render_template, Response, request
from camera import VideoCamera
import cv2

app = Flask(__name__)

camera = None
tracking = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global tracking
    tracking = True
    return ('', 204)

@app.route('/stop', methods=['POST'])
def stop():
    global tracking
    tracking = False
    return ('', 204)

def generate_frames():
    global camera, tracking
    if camera is None:
        camera = VideoCamera()

    while True:
        if tracking:
            frame = camera.get_frame()
            if frame is None:
                continue
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            import time
            time.sleep(0.1)  # Prevent high CPU usage


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        if camera:
            camera.release()
