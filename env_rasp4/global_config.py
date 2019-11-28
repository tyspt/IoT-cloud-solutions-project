
# Time between two pictures are taken in seconds, Raspberry Pi needs ca. 3 seconds to take one 
# picture with the current setting, so this value should be at least 3
CAMERA_INTERVAL_SECONDS = 1800


# Settings used for Serial communication with Arduino
SERIAL_BAND_RATE = 9600
# times of retry when searing for the correct Serial port
SERIAL_ERROR_MAX_RETRY = 10              
# when using a serial port which continously having false data but was proven working before before, max waiting 
# time before abandoning the current connection and go through the port selection process again
SERIAL_ERROR_MAX_TIMEOUT = 300          


# MQTT base topics used for communication between Raspberry Pi and Cloud, subtopics will 
# be added after this depending on sensor or device type (these variables should end with '/')
TOPIC_PREFIX_SENSOR = "/iot_cloud_solutions/project/db/regensburg/rpi_1/sensor/"
TOPIC_PREFIX_CONTROL = "/iot_cloud_solutions/project/control/regensburg/rpi_1/device/"
