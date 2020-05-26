# -*- coding: utf-8 -*-
"""
Created on Sat May 16 14:47:53 2020

@author: Agung Purnomo
"""

import requests
import pandas as pd
import numpy as np
import configparser
import sys
import time
from pandas.io.json import json_normalize
from datetime import datetime
from module.WriteToCsv import *
pd.options.mode.chained_assignment = None

config = configparser.ConfigParser()
config.read(sys.argv[1])

URL = config['Parameter']['URL']
locations = config.get('Parameter', 'locations').split(',')
units = config['Parameter']['units']
lang = config['Parameter']['lang']
appid = config['Parameter']['appid']
output = config['Output']['output']

print('Locations : '+ str(locations) +'\n')

data_resp = []
for location in locations:
    response = requests.get(URL +'?q='+ location +'&units='+ units +'&lang='+ lang +'&appid='+ appid)
    data_resp.append(response.json())
    print('Location :'+ location)
    print('Response Code : '+ str(response.status_code) +'\n')
    print(response.text +'\n')
    time.sleep(1)
    
resp_code = [resp["cod"] for resp in data_resp]

if all(code == 200 for code in resp_code) == False:
    sys.exit('>>> Someting wrong with one or more data (Not all \'Response Code\' is 200) <<<'+'\n')
    
#Extract 'weather' list object, then add as a new column in main dataframe ---------
df = pd.DataFrame(json_normalize(data_resp))
weather = [d.get('weather') for d in data_resp]

for index in range(len(weather)):
    df.at[index, 'Condition'] = weather[index][0]['description']
#---------

# if some parameters doesn't exists on data_resp, add as NULL column ---------
new_column = ['visibility', 'wind.deg', 'rain.1h', 'snow.1h']
add_new_column = {}
def addColumn(col):
    if col not in df:
            df[col] = np.NaN
    return col

for col in new_column:
    add_new_column[col] = addColumn(col)
#---------

df.rename(
        columns={'name': 'Location',
                'coord.lon': 'Longitude',
                'coord.lat': 'Latitude',
                'sys.country': 'Country',
                'dt': 'Local.update.time',
                'main.temp': 'Temperature',
                'main.feels_like': 'Temp.feels',
                'main.temp_min': 'Temp.min',
                'main.temp_max': 'Temp.max',
                'main.pressure': 'Pressure',
                'main.humidity': 'Humidity',
                'wind.speed': 'Wind.speed',
                'wind.deg': 'Wind.direction',
                'clouds.all': 'Cloudiness',
                'sys.sunrise': 'Sunrise',
                'sys.sunset': 'Sunset'
                }, inplace = True)
    
df.columns = map(str.capitalize, df.columns)

data_prep = df[['Location', 'Longitude', 'Latitude', 'Country',
                'Local.update.time', 'Timezone', 'Temperature', 
                'Temp.feels', 'Temp.min', 'Temp.max', 'Pressure', 
                'Humidity', 'Wind.speed', 'Wind.direction', 
                'Cloudiness', 'Visibility', 'Condition', 'Rain.1h',
                'Snow.1h', 'Sunrise', 'Sunset']]
#Change version value every 'data_prep' header (columns) index has changed
data_prep_version = 'H1'

for index in range(len(data_prep)):
    data_prep.loc[[index][0],['Local.update.time']] = datetime.utcfromtimestamp(data_prep.loc[[index][0],['Local.update.time']] + 
                                               int (data_prep.loc[[index][0],['Timezone']]))
    data_prep.loc[[index][0],['Sunrise']] = datetime.utcfromtimestamp(data_prep.loc[[index][0],['Sunrise']] + int (data_prep.loc[[index][0],['Timezone']]))
    data_prep.loc[[index][0],['Sunset']] = datetime.utcfromtimestamp(data_prep.loc[[index][0],['Sunset']] + int (data_prep.loc[[index][0],['Timezone']]))
    data_prep.loc[[index][0],['Timezone']] = int (data_prep.loc[[index][0],['Timezone']] / 3600)

if output.lower() == 'csv':
    header = list(data_prep.columns)
    writeCsv(data_prep_version, data_prep, header)
elif output.lower() == 'sql':
    print('next feature')
else:
    print ('Invalid \'Output\' Parameter Value')
