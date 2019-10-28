from datetime import datetime
from rx import operators as ops
import time
import json
import serial
import rx

from project_mqtt_publisher import MQTTDataPublisher
import global_config as config


''' Use Python rx model to read data streaming from Arduino Sensors
    through serial communication, process, assign correct topics
    and finally upload to cloud
'''

class SerialReader:
    def __init__(self, mqtt_publisher):
        self.mqtt_publisher = mqtt_publisher
        pass
    
    def start_processing(self):
         rx.create(self.__read_from_serial).subscribe(
             on_next=lambda data: self.__publish_data_to_cloud(
                 data, self.mqtt_publisher),
             on_error=lambda e: print(str(datetime.now()), ": (Main) There was an error processing data, message: ", e))
    
    def __read_from_serial(self, observer, args):
        try:
            # open serial port
            ser = serial.Serial(config.SERIAL_PORT_NAME, config.SERIAL_BAND_RATE)

            while True:
                # read each line of json data from serial
                line = ser.readline()
                data = json.loads(line)

                # push that one line to rx stream
                observer.on_next(data)
        except KeyboardInterrupt:
            print(str(datetime.now()) +
                ": (Main) User cancel signal received... Aborting porgram ...")
            pass
        except Exception:
            print(str(datetime.now()) + 
                ": (Serial) Error, unable to get serial communincation... Retrying...")
            # retry accessing serial after a while
            time.sleep(3)
            self.__read_from_serial(observer, args)


    # Process sensor data, assign correct topics to it and finally use MQTT to publish to the cloud
    def __publish_data_to_cloud(self,data, mqtt):
        topic = config.TOPIC_PREFIX_SENSOR + \
            data["sensor"] + "/" + data["unit"] + "/"
        mqtt.publish_data_to_cloud(topic, data['data'])
        return data


# Main function
if __name__ == "__main__":
    mqtt_publisher = MQTTDataPublisher()
    serial = SerialReader(mqtt_publisher)
    serial.start_processing()
