import picamera
import time
from datetime import datetime

import global_config as config


with picamera.PiCamera() as camera:
    # give camera some time to warm up
    camera.start_preview()
    time.sleep(2)
    # take one picture each interval
    for filename in camera.capture_continuous('./images/image-{timestamp:%Y-%m-%d_%H:%M:%S}.jpg'):
        print(str(datetime.now()) + ': Captured %s' % filename)
        time.sleep(config.CAMERA_INTERVAL_SECONDS)