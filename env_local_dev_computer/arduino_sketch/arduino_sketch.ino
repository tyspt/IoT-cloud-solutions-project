#include <SR04.h>
#include <dht_nonblocking.h>
#include <ArduinoJson.h>

/* general delay between two readings of sensor data */
#define READING_INTERVAL_SECONDS 20
#define DHT_SENSOR_TYPE DHT_TYPE_11


/* pin arrangement */
static const int DHT_SENSOR_DIGITAL_PIN = 2;
static const int DISTANCE_SENSOR_DIGITAL_PIN_ECHO = 11;
static const int DISTANCE_SENSOR_DIGITAL_PIN_TRIG = 12;

static const int WATER_LEVEVL_SENSOR_ANALOG_PIN = A0;
static const int LIGHT_SENSOR_ANALOG_PIN = A2;
static const int PH_SENSOR_ANALOG_PIN = A3;
static const int TURBIDITY_SENSOR_ANALOG_PIN = A4;

//create json objects for storing data
const size_t capacity = JSON_OBJECT_SIZE(4);
DynamicJsonDocument temp_json(capacity);
DynamicJsonDocument humid_json(capacity);
DynamicJsonDocument water_level_json(capacity);
DynamicJsonDocument brightness_json(capacity);
DynamicJsonDocument distance_json(capacity);
DynamicJsonDocument ph_json(capacity);
DynamicJsonDocument turbidity_json(capacity);

DHT_nonblocking dht_sensor( DHT_SENSOR_DIGITAL_PIN, DHT_SENSOR_TYPE );
SR04 sr04_ultrasonic = SR04(DISTANCE_SENSOR_DIGITAL_PIN_ECHO,DISTANCE_SENSOR_DIGITAL_PIN_TRIG); //object library for ultrasonic sensor

/*
 * Initialize the serial port.
 */
void setup( )
{
  // Set default values to json objects which hold sensor data, it is important that the String and Object values 
  // e.g. the text "temperature" and "celsius" should not be changed in the loop() function later, otherweise there may be risk of memory leak
  // (See arduinojson document: https://arduinojson.org/v6/doc/)
  temp_json["timestamp"] = 1ul;
  temp_json["sensor"] = "temperature";
  temp_json["data"] = -1.0f;
  temp_json["unit"] = "celsius";

  humid_json["timestamp"] = 1ul;
  humid_json["sensor"] = "humidity";
  humid_json["data"] = -1.0f;
  humid_json["unit"] = "percent";

  water_level_json["timestamp"] = 1ul;
  water_level_json["sensor"] = "water_level";
  water_level_json["data"] = -1.0f;
  water_level_json["unit"] = "percent";

  brightness_json["timestamp"] = 1ul;
  brightness_json["sensor"] = "brightness";
  brightness_json["data"] = -1.0f;
  brightness_json["unit"] = "percent";

  distance_json["timestamp"] = 1ul;
  distance_json["sensor"] = "ultrasonic_distance";
  distance_json["data"] = -1.0f;
  distance_json["unit"] = "centimeter";

  ph_json["timestamp"] = 1ul;
  ph_json["sensor"] = "ph";
  ph_json["data"] = -1.0f;
  ph_json["unit"] = "ph";

  turbidity_json["timestamp"] = 1ul;
  turbidity_json["sensor"] = "turbidity";
  turbidity_json["data"] = -1.0f;
  turbidity_json["unit"] = "percent";
  
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
      //convert water level to percent (sensor max output voltage 4.2V so mapping does't go up to 1023) 
      *water_level = map(analogRead(WATER_LEVEVL_SENSOR_ANALOG_PIN), 0, 720, 0, 100);
      measurement_timestamp = millis( );
      return( true );
  }
  
  return ( false );
}


/* Light brightness measurement
 *  
 * Poll for a measurement, keeping the state machine alive.  Returns
 * true if a measurement is available.
 */
static bool measure_brightness(int *brightness){
  static unsigned long measurement_timestamp = millis( );
  
  /* Measure once every inverval */
  if( millis( ) - measurement_timestamp > (READING_INTERVAL_SECONDS * 1000ul) || millis( ) < measurement_timestamp )
  {   
      //convert brightness to percent
      *brightness = map(analogRead(LIGHT_SENSOR_ANALOG_PIN), 0, 1023, 0, 100);
      measurement_timestamp = millis( );
      return( true );
  }
  
  return ( false );
}


/* Ultrasonic Distance measurement
 *  
 * Poll for a measurement, keeping the state machine alive.  Returns
 * true if a measurement is available.
 */
static bool measure_distance(int *distance){
  static unsigned long measurement_timestamp = millis( );
  
  /* Measure once every inverval */
  if( millis( ) - measurement_timestamp > (READING_INTERVAL_SECONDS * 1000ul) || millis( ) < measurement_timestamp )
  {   
      // simply use library
      *distance = sr04_ultrasonic.Distance();
      measurement_timestamp = millis( );
      return( true );
  }
  
  return ( false );
}


/* Water PH measurement
 *  
 * Poll for a measurement, keeping the state machine alive.  Returns
 * true if a measurement is available.
 */
static bool measure_water_ph(float *ph){
  static unsigned long measurement_timestamp = millis( );
  
  /* Measure once every inverval */
  if( millis( ) - measurement_timestamp > (READING_INTERVAL_SECONDS * 1000ul) || millis( ) < measurement_timestamp )
  {   
      //convert analog value to ph --> still needs colabration
      int measure = analogRead(PH_SENSOR_ANALOG_PIN);
      double voltage = 5 / 1024.0 * measure; //classic digital to voltage conversion
            
      // PH_step = (voltage@PH7 - voltage@PH4) / (PH7 - PH4)
      // PH_probe = PH7 - ((voltage@PH7 - voltage@probe) / PH_step)
      *ph = 7 + ((2.5 - voltage) / 0.18);

      measurement_timestamp = millis( );
      return( true );
  }
  
  return ( false );
}


/* Water turbidity measurement
 *  
 * Poll for a measurement, keeping the state machine alive.  Returns
 * true if a measurement is available.
 */
static bool measure_water_turbidity(float *turbidity){
  static unsigned long measurement_timestamp = millis( );
  
  /* Measure once every inverval */
  if( millis( ) - measurement_timestamp > (READING_INTERVAL_SECONDS * 1000ul) || millis( ) < measurement_timestamp )
  {   
      //convert analog value to turbidity
      int measure = analogRead(TURBIDITY_SENSOR_ANALOG_PIN);
      double voltage = 5 / 1024.0 * measure; //classic digital to voltage conversion
      *turbidity = (1.0 - voltage / 5.0) * 100.0;;
      
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
  float ph;
  float turbidity;
  
  int brightness; 
  int distance;
  
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
  if(measure_water_level(&water_level) == true )
  {
    water_level_json["timestamp"] = millis();
    water_level_json["data"] = water_level;
    
    serializeJson(water_level_json, Serial);
    Serial.println();
  }


   /* Measure brightness.  If the functions returns
   true, then a measurement is available. */
  if(measure_brightness(&brightness) == true )
  {
    brightness_json["timestamp"] = millis();
    brightness_json["data"] = brightness;
    
    serializeJson(brightness_json, Serial);
    Serial.println();
  }

   /* Measure distance.  If the functions returns
   true, then a measurement is available. */
  if(measure_distance(&distance) == true )
  {
    distance_json["timestamp"] = millis();
    distance_json["data"] = distance;
    
    serializeJson(distance_json, Serial);
    Serial.println();
  }

  /* Measure ph.  If the functions returns
   true, then a measurement is available. */
  if(measure_water_ph(&ph) == true)
  {
    ph_json["timestamp"] = millis();
    ph_json["data"] = ph;
    
    serializeJson(ph_json, Serial);
    Serial.println();
  }

  /* Measure turbidity.  If the functions returns
   true, then a measurement is available. */
  if(measure_water_turbidity(&turbidity) == true)
  {
    turbidity_json["timestamp"] = millis();
    turbidity_json["data"] = turbidity;
    
    serializeJson(turbidity_json, Serial);
    Serial.println();
  }
}
