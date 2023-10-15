#https://towardsdatascience.com/video-streaming-in-web-browsers-with-opencv-flask-93a38846fe00
#https://github.com/miguelgrinberg/flask-video-streaming/blob/v1/app.py
import cv2
from flask import Flask, Response

app = Flask(__name__)

def gen_frames():
    """Function to capture video footage from the webcam and stream it"""
    cap = cv2.VideoCapture(0) # 0 for the first USB camera
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            # Flip the frame horizontally for selfie mode
            frame = cv2.flip(frame, 1)
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            # Convert the encoded frame into bytes
            frame_bytes = buffer.tobytes()
            # Yield the frame bytes in the response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    """Function to serve the video stream"""
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
