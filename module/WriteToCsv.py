# -*- coding: utf-8 -*-
"""
Created on Tue May 19 22:03:56 2020

@author: DS - AINO
"""

import csv
import os
from datetime import datetime, timedelta

dirc = 'output/CSV/'
if os.path.exists(dirc) == False:
    os.makedirs(dirc)
      
def writeCsv(data_prep_version, data_prep, header):
    curdate = (datetime.now()+timedelta(days=0)).strftime("%B") + '_' + datetime.now().strftime("%Y")
    
    #create csv 'header_columns' first  
    if os.path.exists(dirc + data_prep_version +'_'+ curdate +'.csv') == False:
        with open(dirc + data_prep_version +'_' + curdate +'.csv', mode='w') as csv_file:
            fieldnames = header
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
     
    #then add row value to existing 'header_columns'
    data_prep.to_csv(dirc + data_prep_version +'_'+ curdate +'.csv', mode='a', index=False, header=False, sep=';')

    print('Success Write to CSV : '+ dirc + data_prep_version + '_'+ curdate +'.csv\n')