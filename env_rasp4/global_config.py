
# Time between two pictures are taken in seconds, Raspberry Pi needs ca. 3 seconds to take one 
# picture with the current setting, so this value should be at least 3
CAMERA_INTERVAL_SECONDS = 1800


# Settings used for Serial communication with Arduino
SERIAL_BAND_RATE = 9600
SERIAL_PORT_NAME = "/dev/ttyACM0"


# MQTT base topics used for communication between Raspberry Pi and Cloud, subtopics will 
# be added after this depending on sensor or device type (these variables should end with '/')
TOPIC_PREFIX_SENSOR = "/iot_cloud_solutions/project/db/regensburg/rpi_1/sensor/"
TOPIC_PREFIX_CONTROL = "/iot_cloud_solutions/project/control/regensburg/rpi_1/device/"