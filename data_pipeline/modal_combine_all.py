# -*- coding: utf-8 -*-
"""
Program to read from all modal analyses processed data and join them all in one master file

@author: alima
"""

## Importing essential modules and functions 
import sys
sys.modules[__name__].__dict__.clear()

import glob
import pandas as pd
import os

exec(open('C:/PhD Research/Generic Codes/notion_corrections.py').read())

### Collecting all individual modal analysis processed data (from each test), reading from each (see for loop), keeping essential information, and merging
path = backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Processed\artificial\modal')
os.chdir(path)
file_list = glob.glob('fit*.xlsx')

modal_all = pd.DataFrame([])
i = 1 

## Reading from each file listed in the file list
for file in file_list:
    df = pd.read_excel(path + '/' + file)
    df = df.iloc[:,0:2]
    
    df.rename(columns = {df.columns[1] : df.columns[1] + '_' + file[-8:-5] + '_' + file[-12:-9]}, inplace = True)
    ## renaming based on the file name
    
    if i == 1:
        modal_all = df
        i += i
    else:
        modal_all = modal_all.merge(df, on ='Size', how = 'outer')

### Exporting and saving
modal_all.to_excel(backslash_correct('C:\PhD Research\Paper 1 - Extraction\Processed\artificial\modal\modal_combine_all.xlsx'), index=False)

