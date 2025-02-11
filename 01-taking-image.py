'''
Take a picture with Python
'''


import time
from picamera2 import Picamera2, Preview

picam = Picamera2()

config = picam.create_preview_configuration()
picam.configure(config)

picam.start_preview(Preview.QTGL)

picam.start()
time.sleep(2)
picam.capture_file("test01-python.jpg")

picam.close()
