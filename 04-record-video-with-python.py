'''
Record a video in Python:

The picamera2 library includes a ton of methods and goes beyond what you might be using in the previous version. It may look overwhelming when you check the documentation, but keep trying because it can save you a lot of time for typical applications.

For example, instead of using the previous timelapse method (manual way of creating a video with ffmpeg), you can directly record a video, doing everything in a short Python script:

NOTE: Ye code video capture karega magar monitor par show nahi karega.
'''

import time

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)

encoder = H264Encoder(10000000)

picam2.start_recording(encoder, 'test.h264')
time.sleep(10)
picam2.stop_recording()