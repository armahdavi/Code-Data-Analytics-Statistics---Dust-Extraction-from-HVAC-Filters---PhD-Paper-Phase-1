# -*- coding: utf-8 -*-
"""
Program to read mode volumes and fractions from each modal analysis of each raw data file, and append the essential modal information (test dust type, filter type, experiment #, and mode volumes and volume fractions)

@author: alima
"""


## Essential modules and functions 

import sys
sys.modules[__name__].__dict__.clear()

exec(open('C:/PhD Research/Generic Codes/labels_all.py').read())
exec(open('C:/PhD Research/Generic Codes/Generic Codes/notion_corrections.py').read())

import pandas as pd
import numpy as np
import glob
import os


## Reading test dust modal information (for ISO A2 and ASHRAE #2)
mode_info_iso = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Raw\artificial_lds\modal') + '/dust_psd_50_iso_00a.xlsx')
mode_info_ash = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Raw\artificial_lds\modal') + '/dust_psd_51_ash_00a.xlsx')

mode_info_iso = mode_info_iso.loc[0:5,['Mode #', 'GSD', 'GM']]
mode_info_ash = mode_info_ash.loc[0:5,['Mode #', 'GSD', 'GM']]

############################################################################################
### Step 1: Collect all modal analysis files and extract their mode volume and fractions ###
############################################################################################

## Collecting all modal analysis raw data files and extract its mode volume values and fractions from each file (see for loop)
path = backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Raw\artificial_lds\modal')
os.chdir(path)

file_list = glob.glob('dust*.xlsx')

psd_modal_ash = pd.DataFrame([])
psd_modal_iso = pd.DataFrame([])

## Reading from each collected file: because ISO and ASHRAE samples have different number of modes, and if statement distinguishes them 
for file in file_list:
    td = file[-12:-9]
    ft = file[-8:-5]
    expn = int(file[9:11])
    if file[-12:-9] == 'ash': # for ashrae samples
        df = pd.read_excel(file).loc[0:5, ['Mode #', 'Total', 'Mode-Fraction']]
        df.rename(columns = {'Mode #': '#', 
                             'Total': 'v',
                             'Mode-Fraction': 'f'}, inplace = True)
        
        ## creating columns
        cols = ['expn', 'td', 'ft']
        for x in ['v', 'f']:
            locals()['list_%s' %x] = []
            for no in list(np.arange(1,7,1)): # a list of 1 - 6 for the # of modes
                cols = cols + ['mode_%s_%s' %(no,x)]
                locals()['list_%s' %x] = locals()['list_%s' %x] + list(df.loc[(df['#'] == no), x])
        
        ## To define all the column names
        list_all = [expn, td, ft] + list_v + list_f 
        
        temp = pd.DataFrame([cols,list_all])
        temp.columns = temp.loc[0]
        temp = temp.loc[1:]
        
        psd_modal_ash = psd_modal_ash.append(temp)
    
    else: # for iso samples
        df = pd.read_excel(file).loc[0:2, ['Mode #', 'Total', 'Mode-Fraction']]
        df.rename(columns = {'Mode #': '#', 
                             'Total': 'v',
                             'Mode-Fraction': 'f'}, inplace = True)
        
        ## creating columns
        cols = ['expn', 'td', 'ft']
        for x in ['v', 'f']:
            locals()['list_%s' %x] = []
            for no in list(np.arange(1,4,1)): # a list of 1 - 6 for the # of modes
                cols = cols + ['mode_%s_%s' %(no,x)]
                locals()['list_%s' %x] = locals()['list_%s' %x] + list(df.loc[(df['#'] == no), x])
        
        list_all = [expn, td, ft] + list_v + list_f 
        
        temp = pd.DataFrame([cols,list_all])
        temp.columns = temp.loc[0]
        temp = temp.loc[1:]
        
        psd_modal_iso = psd_modal_iso.append(temp)
        
    psd_modal_analysis_summary = psd_modal_iso.append(psd_modal_ash).reset_index(drop=True)          
   
psd_modal_analysis_summary.replace({'ft': label_filter_type0,
                                    'td': label_test_dust2},
                                       inplace = True)

## Sorting, exporting, and saving the new processed file
psd_modal_analysis_summary = psd_modal_analysis_summary.astype(float).sort_values(['td','expn'])

savepath = backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Processed\artificial\modal')
psd_modal_analysis_summary.to_excel(savepath +'/psd_modal_analysis_summary.xlsx', index = False)