from project_serial_reader import SerialReader
import project_camera

import threading
import logging

logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.ERROR, filename="error.log")

""" Main Entry of the project 
"""
# Thread dealing with serial data from Arduino
serial_reader = SerialReader()
t_serial = threading.Thread(target=serial_reader.start_processing, daemon=True)
t_serial.start()

# Thread dealing with camera
t_camera = threading.Thread(
    target=project_camera.take_picture, daemon=True)
t_camera.start()

# block main thread to make sure all other threads will continue running
t_camera.join()
