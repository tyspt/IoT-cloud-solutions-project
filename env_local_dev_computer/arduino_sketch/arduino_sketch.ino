
#include <dht_nonblocking.h>
#include <ArduinoJson.h>

#define DHT_SENSOR_TYPE DHT_TYPE_11

/* use int value to stand for sensor types in order to prevent meomory leak
 * when converting to json
 */
#define TEMPERATURE_SENSOR 1
#define HUMIDITY_SENSOR 2
 
static const int DHT_SENSOR_PIN = 2;
DHT_nonblocking dht_sensor( DHT_SENSOR_PIN, DHT_SENSOR_TYPE );


//create json objects for storing data
const size_t capacity = JSON_OBJECT_SIZE(4);
DynamicJsonDocument temp_json(capacity);
DynamicJsonDocument humid_json(capacity);


/*
 * Initialize the serial port.
 */
void setup( )
{
  // setting values for the fields that don't change in json objects
  temp_json["sensor"] = "temperature";
  temp_json["unit"] = "°C";

  humid_json["sensor"] = "humidity";
  humid_json["unit"] = "%";
  
  Serial.begin( 9600);
}



/*
 * Poll for a measurement, keeping the state machine alive.  Returns
 * true if a measurement is available.
 */
static bool measure_environment( float *temperature, float *humidity )
{
  static unsigned long measurement_timestamp = millis( );

  /* Measure once every four seconds. */
  if( millis( ) - measurement_timestamp > 3000ul )
  {
    if( dht_sensor.measure( temperature, humidity ) == true )
    {
      measurement_timestamp = millis( );
      return( true );
    }
  }

  return( false );
}



/*
 * Main program loop.
 */
void loop( )
{
  float temperature;
  float humidity;

  /* Measure temperature and humidity.  If the functions returns
     true, then a measurement is available. */
  if( measure_environment( &temperature, &humidity ) == true )
  {
    //Serial.print( "T = " );
    //Serial.print( temperature, 1 );
    //Serial.print( " deg. C, H = " );
    //Serial.print( humidity, 1 );
    //Serial.println( "%" );

    temp_json["timestamp"] = millis();
    temp_json["data"] = temperature;

    humid_json["timestamp"] = millis();
    humid_json["data"] = humidity;
    
    serializeJson(temp_json, Serial);
    Serial.println();
    serializeJson(humid_json, Serial);
    Serial.println();
  }

  
}
