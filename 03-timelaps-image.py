'''
create a timelapse (meaning recording a picture every X seconds or minutes over a long period)
'''

import time
from picamera2 import Picamera2, Preview

picam = Picamera2()

config = picam.create_preview_configuration()
picam.configure(config)
picam.start()

for i in range(1,10):
    picam.capture_file(f"ts{i}.jpg")
    print(f"Captured image {i}")
    time.sleep(3)
    
picam.stop()