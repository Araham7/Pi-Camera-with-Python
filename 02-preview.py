'''
1. You can add configuration options inside the create_preview_configuration method to change the default settings.

In this example, I force the camera to display the preview in 1600×1200 pixels, instead of the default option. I’m using the same configuration for the recording, so the JPG file will be the same size.

2. You can use libcamera to rotate the picture.

Don’t forget to import it at the beginning, and then you can use the “Transform()” method to flip the picture either vertically, horizontally or both.
'''

import time, libcamera
from picamera2 import Picamera2, Preview

picam = Picamera2()

config = picam.create_preview_configuration(main={"size": (1600, 1200)})
config["transform"] = libcamera.Transform(hflip=1, vflip=1)
picam.configure(config)

picam.start_preview(Preview.QTGL)

picam.start()
time.sleep(2)
picam.capture_file("test02-python.jpg")

picam.close()