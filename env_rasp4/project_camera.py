import picamera
import time
from datetime import datetime

import global_config as config

camera = None
timestamp = None
filename = None


while True:
    camera = picamera.PiCamera()
    
    # my camera is installed upside down so i have to flip it over
    camera.rotation = 180
    camera.resolution = (1024, 768)
    camera.framerate = 5
    
    try:
        # give camera some time to warm up
        camera.start_preview()
        time.sleep(2)
        
        # get current time and capture the picture
        timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        filename = './images/image_%s.jpg' % timestamp
        
        # add annotate on picture
        camera.annotate_text = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        camera.annotate_text_size = 15
        
        camera.capture(filename)
        print(str(datetime.now()) + ': Captured %s' %filename)
        
        camera.stop_preview()
    finally:
        # The interval between two shots should be quite long, it would be better to
        # turn it back on when taking next shot 
        camera.close()
        
    time.sleep(config.CAMERA_INTERVAL_SECONDS - 3)
    
    
    
    
    
    # # take one picture each interval
    # for filename in camera.capture_continuous('./images/image_{timestamp:%Y-%m-%d_%H:%M:%S}.jpg'):
    #     print(str(datetime.now()) + ': Captured %s' % filename)
    #     time.sleep(config.CAMERA_INTERVAL_SECONDS)
