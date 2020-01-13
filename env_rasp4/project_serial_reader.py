from datetime import datetime, timedelta
from rx import operators as ops
import time
import json
import serial
import serial.tools.list_ports
import rx

import logging

from project_mqtt_helper import MQTTDataHelper
import global_config as config


''' Use Python rx model to read data streaming from Arduino Sensors
    through serial communication, process, assign correct topics
    and finally upload to cloud
'''


class SerialReader:
    def __init__(self):
        self.mqtt_publisher = MQTTDataHelper()

    def start_processing(self):
        rx.create(self.read_from_serial).subscribe(
            on_next=lambda data: self.publish_data_with_mqtt(
                data, self.mqtt_publisher),
            on_error=lambda e: logging.info("(Main) There was an error processing data, message: {}".format(str(e))))

    def read_from_serial(self, observer, args):
        try:
            while True:
                # this one blocks until find correct port -> can block forever
                ser = self.find_ardunio_serial_port()
                
                last_correct_data_timestamp = datetime.utcnow()
                
                while True:
                    line = None
                    
                    try:
                        # read each line of json data from serial
                        line = ser.readline().decode('UTF-8').strip()
                        
                        if len(line) > 0:
                            data = json.loads(line)

                            # mark last timestamp reading correct data
                            last_correct_data_timestamp = datetime.utcnow()
                        
                            # push that one line to rx stream
                            observer.on_next(data)
                    except KeyboardInterrupt:
                        raise
                    except:
                        logging.info("(Main) error parsing data {}".format(line))
                        time_since_last_correct_data = datetime.utcnow() - last_correct_data_timestamp
                        # if haven't been able to get correct data for a long time, abandon the current connection and 
                        # try to initiallize the serial connection again
                        if time_since_last_correct_data > timedelta(seconds=config.SERIAL_ERROR_MAX_TIMEOUT):
                            break
                        # add some time buffer to prevent too frequent retry when error occurs
                        time.sleep(3)
        except KeyboardInterrupt:
            logging.info("(Main) User canceled, exiting...")
        
            
    # Find the right working serial port, blocks until finds correct port (also when no data in serial or wrong data format -> non json sent)
    def find_ardunio_serial_port(self):
        while True:
            logging.info(
                "(Main) ------- Trying to find correct serial port... -------")
            ports = list(serial.tools.list_ports.comports())
            
            # find out which serial port is the one has data
            for p in ports:
                logging.info("(Main) Testing serial port {}".format(p))
                # try to open serial port
                ser = serial.Serial(
                    p.device, config.SERIAL_BAND_RATE, timeout=3)
                
                error_count = 0
                while error_count < config.SERIAL_ERROR_MAX_RETRY:
                    try:
                        # read each line of json data from serial
                        line = ser.readline().decode('UTF-8').strip()
                        
                        if len(line) > 0:
                            logging.debug("read line: {}".format(line))
                            data = json.loads(line)
                            logging.info("(Main) Successfully read data from serial {}".format(str(data)))
                            return ser
                    except KeyboardInterrupt:
                        raise
                    except:
                        error_count += 1
                        logging.info("(Main) Try {} on Port {} failed... retrying...".format(error_count, p))
                        # add some time buffer to prevent too frequent retry when error occurs
                        time.sleep(3)
            
            # Wait for a long time and check again if there's new machine available
            RETRY_INTERVAL = 300
            logging.error(
                "(Main) Can not read data from Serial port, is arduino working correctly? Retrying in {} seconds...".format(RETRY_INTERVAL))
            time.sleep(RETRY_INTERVAL)
            
    
    # Process sensor data, assign correct topics to it and finally use MQTT to publish to the cloud
    def publish_data_with_mqtt(self, data, mqtt):
        topic = config.TOPIC_PREFIX_SENSOR + \
            data["sensor"] + "/" + data["unit"] + "/"
        mqtt.publish_data_to_cloud(topic, data['data'])
        return data


# Main function
if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s",
                        level=logging.DEBUG)

    SerialReader().start_processing()
    
