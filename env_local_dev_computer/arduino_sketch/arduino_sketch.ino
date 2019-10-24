
#include <dht_nonblocking.h>
#include <ArduinoJson.h>

/* pin arrangement */
static const int DHT_SENSOR_DIGITAL_PIN = 2;  
static const int WATER_LEVEVL_SENSOR_ANALOG_PIN= A0;


/* general delay between two readings of sensor data */
#define READING_INTERVAL_SECONDS 5


/* use int value to stand for sensor types in order to prevent meomory leak
 * when converting to json */
#define TEMPERATURE_SENSOR 1
#define HUMIDITY_SENSOR 2

#define DHT_SENSOR_TYPE DHT_TYPE_11

DHT_nonblocking dht_sensor( DHT_SENSOR_DIGITAL_PIN, DHT_SENSOR_TYPE );




//create json objects for storing data
const size_t capacity = JSON_OBJECT_SIZE(4);
DynamicJsonDocument temp_json(capacity);
DynamicJsonDocument humid_json(capacity);
DynamicJsonDocument water_level_json(capacity);

/*
 * Initialize the serial port.
 */
void setup( )
{
  // Set default values to json objects which hold sensor data, it is important that the String and Object values 
  // e.g. the text "temperature" and "°C" should not be changed in the loop() function later, otherweise there may be risk of memory leaking 
  // (See arduinojson document: https://arduinojson.org/v6/doc/)
  temp_json["timestamp"] = 1ul;
  temp_json["sensor"] = "Temperature";
  temp_json["data"] = -1.0f;
  temp_json["unit"] = "°C";

  humid_json["timestamp"] = 1ul;
  humid_json["sensor"] = "Humidity";
  humid_json["data"] = -1.0f;
  humid_json["unit"] = "%";

  water_level_json["timestamp"] = 1ul;
  water_level_json["sensor"] = "Water-level";
  water_level_json["data"] = -1.0f;
  water_level_json["unit"] = "%";
  
  Serial.begin(9600);
}



/* Temperature and humidity measurement
 * 
 * Poll for a measurement, keeping the state machine alive.  Returns
 * true if a measurement is available.
 */
static bool measure_environment( float *temperature, float *humidity )
{
  static unsigned long measurement_timestamp = millis( );

  /* Measure once per interval */
  if( millis( ) - measurement_timestamp > (READING_INTERVAL_SECONDS * 1000ul) ||  millis( ) < measurement_timestamp )
  {
    if( dht_sensor.measure( temperature, humidity ) == true )
    {
      measurement_timestamp = millis( );
      return( true );
    }
  }

  return( false );
}



/* Water level measurement
 *  
 * Poll for a measurement, keeping the state machine alive.  Returns
 * true if a measurement is available.
 */
static bool measure_water_level(float *water_level){
  static unsigned long measurement_timestamp = millis( );
  
  /* Measure once every inverval */
  if( millis( ) - measurement_timestamp > (READING_INTERVAL_SECONDS * 1000ul) || millis( ) < measurement_timestamp )
  {   
      //convert water level to percent (sensor max output voltage 4.2V, last value is for collaboration) 
      *water_level = ((analogRead(WATER_LEVEVL_SENSOR_ANALOG_PIN) * 5.0 / 4.2) / 1023.0 * 100.0) / 0.85;
      measurement_timestamp = millis( );
      return( true );
  }
  
  return ( false );
}


/*
 * Main program loop.
 */
void loop( )
{
  float temperature;
  float humidity;

  float water_level;   

  /* Measure temperature and humidity.  If the functions returns
     true, then a measurement is available. */
  if( measure_environment( &temperature, &humidity ) == true )
  {
    temp_json["timestamp"] = millis();
    temp_json["data"] = temperature;

    humid_json["timestamp"] = millis();
    humid_json["data"] = humidity;
    
    serializeJson(temp_json, Serial);
    Serial.println();
    serializeJson(humid_json, Serial);
    Serial.println();
  }


 /* Measure water level.  If the functions returns
   true, then a measurement is available. */
  if(measure_water_level(&water_level))
  {
    water_level_json["timestamp"] = millis();
    water_level_json["data"] = water_level;
    
    serializeJson(water_level_json, Serial);
    Serial.println();
  }
  
}
