# -*- coding: utf-8 -*-
"""
Code to calculate the cv of the dust recovery and recovery efficiency from repeated experiements (MERV 11 filters from both test dust cases)

@author: alima
"""

#################################################################
### Step 1: Importing important modules, functions, and files ###
#################################################################

import sys
sys.modules[__name__].__dict__.clear()

import pandas as pd
import os
os.chdir(r'C:\PhD Research\Generic Codes')
from notion_corrections import backslash_correct

file = backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Processed\artificial\artl_dataset_summary.xlsx')
df_append_all = pd.read_excel(file)

##################################################################################################
### Step 2: Keeping MERV 11 filters (labelled 3), and data corresponding to 1st and 2nd cycles ###
############### and calculating CVs based on test dust and cycle number ##########################
##################################################################################################

df_append_all = df_append_all[(df_append_all['ft'] == 3) & (df_append_all['Cycle_N'] <= 2)] # replicates happened for filter type 3 only
cv = df_append_all.groupby(['td', 'Cycle_N'], as_index = False)['M_t_cum', 'tCE_cum'].agg(['std','mean'])

## Calculating CV based on std/mean and adding it to the oritional dataframe
df_append_all = pd.read_excel(file)

for td in [1,2]: # for test dust
    for c in [1,2]: # for Cycle #
        for var in ['M_t_cum', 'tCE_cum']:
            df_append_all.loc[(df_append_all['td'] == td) 
                              & (df_append_all['ft'] != 3)
                              & (df_append_all['Cycle_N'] == c),
                              'cv_%s_%s_%s' %(var,td,c)] = round(((cv.loc[(td,c),(var, 'std')] / cv.loc[(td,c),(var, 'mean')]) * 100),2)
        
## Exporting and saving 
export_path = backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Processed\artificial')
df_append_all.to_excel(export_path+ '/artl_dataset_summary_w_cv.xlsx', index=False)
