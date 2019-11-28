from project_serial_reader import SerialReader
from project_mqtt_publisher import MQTTDataPublisher

from project_camera import IntervalPictureTaker

import threading
import logging

logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", \
                    # filename="project.log", 
                    level=logging.DEBUG)

""" Main Entry of the project 
"""
# Thread dealing with serial data from Arduino
serial_reader = SerialReader(MQTTDataPublisher())
t_serial = threading.Thread(target=serial_reader.start_processing, daemon=True)
t_serial.start()

# Thread dealing with camera
t_camera = threading.Thread(
    target=IntervalPictureTaker().start_taking_picture, daemon=True)
t_camera.start()

# block main thread to make sure all other threads will continue running
t_camera.join()
