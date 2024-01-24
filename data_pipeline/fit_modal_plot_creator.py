# -*- coding: utf-8 -*-
"""
Program to read and keep the fitted and measured PSDs for all the dust recovered from the artificially loaded filters.
It compares the PSDs of measured and fitted based on modal analysis calculations.

@author: alima
"""

#############################################################
### Step 1: Importing essential modules and generic codes ###
#############################################################

import sys
sys.modules[__name__].__dict__.clear()

exec(open('C:/PhD Research/Generic Codes/labels_all.py').read())
exec(open('C:/PhD Research/Generic Codes/Generic Codes/notion_corrections.py').read())

import pandas as pd
import glob
# from notion_corrections import backslash_correct
import os

####################################################################
### Step 2: Collecting all modal analysis raw files and refining ###
####################################################################

path = backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Raw\artificial_lds\modal')
os.chdir(path)

## putting all modal analysis files in a list
file_list = glob.glob('dust*.xlsx')

## looing over all files
for file in file_list:
    exp = '0' + file[9:11]
    t = file[12:15]
    f = file[16:19]
    
    df = pd.read_excel(path + '/' + file, header = 9)
    df = df[['Size', 'Made', 'Real']]
    df.rename(columns = {'Made':'fit_%s' %exp,
                         'Real': 'Measure_%s' %exp}, inplace = True)
    
    ## Saving the file corresponding to the imported raw file
    savepath = backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Processed\artificial\modal')
    savefile = 'fit_mode_%s_%s_%s' %(exp,t,f)
    df.to_excel(savepath + '/' + savefile + '.xlsx', index = False)
    