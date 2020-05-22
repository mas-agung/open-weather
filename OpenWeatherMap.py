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
from pandas.io.json import json_normalize
from datetime import datetime
from module.WriteToCsv import *

config = configparser.ConfigParser()
config.read(sys.argv[1])

URL = config['Parameter']['URL']
location = config['Parameter']['location']
units = config['Parameter']['units']
lang = config['Parameter']['lang']
appid = config['Parameter']['appid']
output = config['Output']['output']
PARAMS = {'q': location, 'units': units, 'lang': lang, 'appid': appid}

response = requests.get(url = URL, params = PARAMS)
data_resp = response.json()
print('Response Code : '+ str(response.status_code) +'\n')
print(response.text +'\n')

if response.status_code == 200:
    #Extract 'weather' list object, then add as a new column in main dataframe ---------
    df = pd.DataFrame(json_normalize(data_resp))
    weather = pd.DataFrame.from_dict(json_normalize(data_resp['weather']), orient='columns')
    df['Condition'] = weather['description']
    #---------
    
    # if some parameters doesn't exists on data_resp, add as NULL column ---------
    new_column = ['visibility', 'wind.deg', 'rain.1h', 'snow.1h']
    add_new_column = {}
    def addColumn(col):
        if col.lower() not in df:
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
    #Change version value every 'data_prep' header (columns) index / name has changed
    data_prep_version = 'H1'
    
    data_prep.loc[[0],['Local.update.time']] = datetime.utcfromtimestamp(data_prep['Local.update.time'] + 
                                               data_prep['Timezone'])
    data_prep.loc[[0],['Sunrise']] = datetime.utcfromtimestamp(data_prep['Sunrise'] + data_prep['Timezone'])
    data_prep.loc[[0],['Sunset']] = datetime.utcfromtimestamp(data_prep['Sunset'] + data_prep['Timezone'])
    data_prep.loc[[0],['Timezone']] = data_prep['Timezone'] / 3600

#    print(data_prep['Local.update.time'])
#    print(data_prep['Sunrise'])
#    print(data_prep['Sunset'])
#    print(data_prep.columns)
    
    if output.lower() == 'csv':
        header = list(data_prep.columns)
        writeCsv(data_prep_version, data_prep, header)
    elif output.lower() == 'sql':
        print('next feature')
    else:
        print ('Invalid \'Output\' Parameter Value')
    