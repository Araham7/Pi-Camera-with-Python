import cv2
import numpy as np
from picamera2 import Picamera2
import socketio
import time

# Initialize the Raspberry Pi camera
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

# Connect to Express.js server
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to Express.js server")
    # Start sending frames after connection is established
    capture_and_send_frames()

@sio.event
def disconnect():
    print("Disconnected from Express.js server")

def capture_and_send_frames():
    while True:
        try:
            # Capture a frame from the camera
            frame = picam2.capture_array()
            print("Frame captured:", frame.shape)  # Debug print

            # Convert the frame to JPEG format
            _, jpeg_frame = cv2.imencode('.jpg', frame)
            print("JPEG frame size:", len(jpeg_frame))  # Debug print

            # Send the frame to Express.js server
            sio.emit('video_frame', jpeg_frame.tobytes())
            print("Frame sent to Express.js server")  # Debug print

        except Exception as e:
            print(f"Error capturing or sending frame: {e}")

        # Wait for a small delay to control the frame rate
        time.sleep(1 / 20) # Adjust frame rate as needed

# Connect to Express.js server
sio.connect("https://pi-video-streaming-server.onrender.com")
sio.wait()
