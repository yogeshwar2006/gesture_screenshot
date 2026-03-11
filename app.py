from flask import Flask, Response
import cv2
from gesture import process_frame

app = Flask(__name__)

camera=None
running=False

def gen_frames():

    global camera,running

    camera=cv2.VideoCapture(0)

    while running:

        success,frame=camera.read()

        if not success:
            break

        frame=cv2.flip(frame,1)

        frame=process_frame(frame)

        ret,buffer=cv2.imencode('.jpg',frame)
        frame=buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')

    camera.release()

@app.route('/')
def index():
    return open("index.html").read()

@app.route('/video_feed')
def video_feed():

    global running
    running=True

    return Response(gen_frames(),
    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop')
def stop():

    global running,camera

    running=False

    if camera:
        camera.release()

    return "Camera Stopped"

if __name__=="__main__":
    app.run(debug=True)