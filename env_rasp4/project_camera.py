import picamera
import time
from datetime import datetime

import logging

import global_config as config

""" Taking picture under a given interval.
"""


def take_picture():
        camera = None
        timestamp = None
        filename = None

        while True:
            time.sleep(config.CAMERA_INTERVAL_SECONDS)
            
            try:
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
                    filename = "./images/image_%s.jpg" % timestamp

                    # add annotate on picture
                    camera.annotate_text = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
                    camera.annotate_text_size = 15

                    # take the picture
                    camera.capture(filename)
                    print(str(datetime.now()) +
                          "(Camera) Captured %s" % filename)

                    camera.stop_preview()
                except:
                    raise
                finally:
                    # The interval between two shots should be quite long, it would be better to
                    # turn it back on when taking next shot
                    camera.close()
            except KeyboardInterrupt:
                return
            except:
                logging.error(
                    "(Camera) error taking picture... skipping current one...")

if __name__ == "__main__":
    take_picture()
