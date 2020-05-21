

# open-weather
Weather data collector from Open Weather API using python script. Stored it into some of media. Weather data obtained from the 'current weather data' API. You can create free account to get your 'appid' (API Key).

*For more explanation about OpenWeatherMap API :*
[https://openweathermap.org/current#other](https://openweathermap.org/current#other)


## How to Run
	'OpenWeatherMap.py config.ini'

## Output Format
At this time, the output format is only available in CSV format. File is stored in the 'output' folder.

**Parameter output :**

>***Location :***  City identification  
***Longitude :***  City geo location, longitude
***Latitude :*** City geo location, longitude
***Country :*** Country code
***Local.update.time :***  Local location time when data available
***Timezone :***  Time zone differencess with GMT
***Temperature :*** Current temperature*
***Temp.feels :*** Current temperature feels like*
***Temp.min :***  Minimum temperature at the moment. This is deviation from current temp that is possible for large cities and megalopolises geographically expanded*
***Temp.max :*** Maximum temperature at the moment. This is deviation from current temp that is possible for large cities and megalopolises geographically expanded*
***Pressure :*** Atmospheric pressure (hPa)
***Humidity :*** Humidity (%)
***Wind.speed :*** Wind speed (meter/sec)*
***Wind.direction :*** Wind degrees (meteorological)
***Cloudiness :*** Cloudiness (%)
***Visibility :*** Visibility (meter)
***Condition :*** Weather condition**
***Rain.1h :*** Precipitation volume for last hour (mm)
***Snow.1h :*** Snow volume for last hour (mm)
***Sunrise :*** Sunrise time
***Sunset :*** Sunrise time


### * Units format
##### Description:
Standard, metric, and imperial units are available.
##### Parameters:

**units**  metric, imperial. When you do not use units parameter, format is Standard by default.
Temperature is available in Fahrenheit, Celsius and Kelvin units.

-   For temperature in Fahrenheit use units=imperial
-   For temperature in Celsius use units=metric
-   Temperature in Kelvin is used by default, no need to use units parameter in API call

### ** Multilingual support

You can use  `lang`  parameter to get the output in your language.  
Translation is applied for the  `Location`  and  `Condition`  fields.

> Please visit to [https://openweathermap.org/current#other](https://openweathermap.org/current#other)
> for more detail.
