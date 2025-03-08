import cv2
import numpy as np
from picamera2 import Picamera2
import socket
import time

# Initialize the Raspberry Pi camera
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

# UDP settings
UDP_IP = "127.0.0.1"  # Replace with your server IP
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def capture_and_send_frames():
    while True:
        try:
            # Capture a frame from the camera
            frame = picam2.capture_array()
            print("Frame captured:", frame.shape)  # Debug print

            # Convert the frame to JPEG format
            _, jpeg_frame = cv2.imencode('.jpg', frame)
            print("JPEG frame size:", len(jpeg_frame))  # Debug print

            # Send the frame to the server
            sock.sendto(jpeg_frame.tobytes(), (UDP_IP, UDP_PORT))
            print("Frame sent to server")  # Debug print

        except Exception as e:
            print(f"Error capturing or sending frame: {e}")

        # Wait for a small delay to control the frame rate
        time.sleep(1 / 20)  # Adjust frame rate as needed

# Start capturing and sending frames
capture_and_send_frames()