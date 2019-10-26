from picamera import PiCamera
from time import sleep
import global_config as config


camera.start_preview()
for i in range(5):
    sleep(config.CAMERA_INTERVAL_SECONDS)
    camera.capture('./images/image%s.jpg' % i)
camera.stop_preview()
