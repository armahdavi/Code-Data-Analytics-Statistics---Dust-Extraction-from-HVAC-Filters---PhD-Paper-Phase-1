# -*- coding: utf-8 -*-
"""

The purpose of this file is to define functions that reads in raw sensor data and convert them to dataframes applicable for further processings.
Sensor data often comes with time series data (e.g., Mini-WRAS, DT, DC, HOBO etc.,).
This is the simple version meaning there is no procesing of the raw time-series data.
The next version of this file should process the time series to adjust summer time / winter time adjustment as well as putting a universal time of GMT

@author: alima

"""


###############################
#### READ IN DUSTTRAK DRX #####
###############################

def dt_drx_read_in(importpath, exportpath, file_in, file_out):
    exec(open(r'C:\Career\Learning\Python Practice\Generic Codes\notion_corrections.py').read())
    import pandas as pd
    if file_in[-3:] == 'txt':
        file_get = backslash_correct(importpath) + file_in
    else:
        file_get = backslash_correct(importpath) + file_in + '.txt'
    
    df = pd.read_csv(file_get, skiprows = 28)
    df['Date'] = df['dd/MM/yyyy'] + ' ' +  df['hh:mm:ss']
    df.drop(['dd/MM/yyyy','hh:mm:ss', 'mg/m^3.2'], axis = 1, inplace = True)
    df.columns = ['PM1', 'PM2.5', 'PM10', 'TSP', 'Date']
    df = df[['Date','PM1', 'PM2.5', 'PM10', 'TSP']]
    
    if file_out[-4] != 'xlsx':
        file_give = backslash_correct(exportpath) + file_out + '.xlsx'
    else:
        file_give = backslash_correct(exportpath) + file_out
        
    df.to_excel(file_give, index = False)
    
    return df



##############################
#### READ IN DUSTTRAK II #####
##############################

# one more argument for cap type: 'PM2.5', 'PM10', relative to drx

def dt_ii_read_in(importpath, exportpath, file_in, file_out, captype):
    exec(open(r'C:\Career\Learning\Python Practice\Generic Codes\notion_corrections.py').read())
    import pandas as pd
    if file_in[-3:] == 'txt':
        file_get = backslash_correct(importpath) + file_in
    else:
        file_get = backslash_correct(importpath) + file_in + '.txt'
    
    df = pd.read_csv(file_get, skiprows = 28)
    df['Date'] = df['dd/MM/yyyy'] + ' ' +  df['hh:mm:ss']
    df.drop(['dd/MM/yyyy','hh:mm:ss'], axis = 1, inplace = True)
    df = df[['Date', 'mg/m^3']]    
    df.rename(columns = {'mg/m^3': cap_type}, inplace = True)
    
    if file_out[-4] != 'xlsx':
        file_give = backslash_correct(exportpath) + file_out + '.xlsx'
    else:
        file_give = backslash_correct(exportpath) + file_out
        
    df.to_excel(file_give, index = False)
    
    return df


########################################
#### READ IN DYLOS COUNTER. DC1700 #####
########################################

# Also automatically fixes the date issue but it does not convert it to timestamp

def dc_1700_read_in(importpath, exportpath, file_in, file_out):
    exec(open(r'C:\Career\Learning\Python Practice\Generic Codes\notion_corrections.py').read())
    import pandas as pd
    if file_in[-3:] == 'txt':
        file_get = backslash_correct(importpath) + file_in
    else:
        file_get = backslash_correct(importpath) + file_in + '.txt'
    
    df = pd.read_csv(file, skiprows = 7)
    df['Date/Time'] = '20' + df['Date/Time'].str[6:8] + '-' + df['Date/Time'].str[0:2] + '-' + df['Date/Time'].str[3:5] + ' ' + df['Date/Time'].str[-5:]

    if file_out[-4] != 'xlsx':
        file_give = backslash_correct(exportpath) + file_out + '.xlsx'
    else:
        file_give = backslash_correct(exportpath) + file_out
        
    df.to_excel(file_give, index = False)
    
    return df
    
    
    
######################################
####### HOBO Sensors U Series ########
######################################

def hobo_u_read_in(importpath, exportpath, file_in, file_out):
    exec(open(r'C:\Career\Learning\Python Practice\Generic Codes\notion_corrections.py').read())
    import pandas as pd
    if file_in[-3:] == 'csv':
        file_get = backslash_correct(importpath) + file_in
    else:
        file_get = backslash_correct(importpath) + file_in + '.csv'
    
    df = pd.read_csv(file_get, skiprows = 1).iloc[:,1:4]
    df.columns = ['Time', 'Temp', 'RH']
    # 07/19/18 09:50:00  AM
    df['Time'] = '20' + df['Time'].str[6:8] + '-' + df['Time'].str[0:2] + '-' + df['Time'].str[3:5] + ' ' + df['Time'].str[-12:-3]

    if file_out[-4] != 'xlsx':
        if file_out[-4] == '.csv':
            file_give = backslash_correct(exportpath) + file_out[:-4] + '.xlsx'
        else:
            file_give = backslash_correct(exportpath) + file_out + '.xlsx'
    else:
        file_give = backslash_correct(exportpath) + file_out
        
    df.to_excel(file_give, index = False)
    
    return df

    
    
    
    
    