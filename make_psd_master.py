# -*- coding: utf-8 -*-
"""
Program to read raw particle size distribution (PSD) files from each file and append it to a master psd data file
It requires reading a generic function, mastersizer_input, which has been defined in a generic code, mastersizer_all.py
What mastersizer_all.py does is 1) to read the raw csv PSD file
                                2) to aggregate all repeats of the same sample (aggregation by sample name) for count, min, mean, median, 
                                and max per size bin
                                3) transpose data: this allows to have a separate column for particle size and several columns for count, 
                                min, mean, median, and max of the sample(s)

@author: alima
"""

import sys
sys.modules[__name__].__dict__.clear()
import pandas as pd
import glob
import os

#############################################
### Step 1: Reading necessary labels and  ###
#############################################
exec(open('C:/PhD Research/Generic Codes/notion_corrections.py').read())
exec(open('C:/PhD Research/Generic Codes/mastersizer_all.py').read())
# from notion_corrections import backslash_correct
# from mastersizer_all import mastersizer_input

##############################################################################
################ Step 2: Reading all mastersizer raw files and ###############
### appending all in one file: for "volume" (v) and "count" (c) separately.###
##############################################################################

## Change path to raw file path
path = backslash_correct('C:\PhD Research\Paper 1 - Extraction\Raw\psd')
os.chdir(path)

## Loo over volume and count
for psdtype in ['v', 'c']:
    locals()['artl_%s_psd_master' %psdtype] = pd.DataFrame([]) # variables in locals to change their names based on 'v' or 'c'
    i = 1
    
    ## Loop over all raw file data
    for file in  glob.glob('%s*.csv' %psdtype):
        exportfile = file[:-4] + '_ordered' # because the list has .csv at end
        df_collapse_all = mastersizer_input(path,file,exportfile)
        
        ## merging each processed data to previous psd dataframe
        if i == 1:
            locals()['artl_%s_psd_master' %psdtype] = df_collapse_all
            i = i + 1
        else:
            locals()['artl_%s_psd_master' %psdtype] = pd.merge(df_collapse_all, locals()['artl_%s_psd_master' %psdtype], on='Size', how = 'outer')
        
        ## exporting and saving the master psd processed files
        locals()['artl_%s_psd_master' %psdtype].to_excel(path + '/' + 'artl_%s_psd_master' %psdtype +'.xlsx', index=False)
            

