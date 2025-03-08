import cv2
import numpy as np
from picamera2 import Picamera2
from libcamera import controls
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Flask and Socket.IO setup
app = Flask(__name__)

# Allow connections from http://localhost:5173
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")

# Initialize the Raspberry Pi camera
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

def capture_and_send_frames():
    while True:
        # Capture a frame from the camera
        frame = picam2.capture_array()

        # Convert the frame to JPEG format
        _, jpeg_frame = cv2.imencode('.jpg', frame)

        # Send the frame as a binary message with the event name
        socketio.emit('/video-send', jpeg_frame.tobytes())

        # Wait for a small delay to control the frame rate
        socketio.sleep(1 / 24)  # Adjust frame rate as needed

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    socketio.start_background_task(capture_and_send_frames)

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8765)