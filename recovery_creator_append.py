# -*- coding: utf-8 -*-
"""
Program to make dataframes from all extraction lab data sheets (LDSs) from the artificially loaded filters

@author: alima

"""

import sys
sys.modules[__name__].__dict__.clear()

import pandas as pd
import numpy as np
import os
os.chdir(r'C:/PhD Research/Generic Codes')
from notion_corrections import backslash_correct, stata_varlist_split


###################################################################
### Step 1: Loop for reading all LDSs and append to a master df ###
###################################################################

## Importing filter_loading_master (for merging later with new files) and reading all required labels
filter_loading_master = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Processed\artificial\filter_loading_master.xlsx'))
exec(open('C:/PhD Research/Generic Codes/labels_all.py').read())

## Putting all excel files of LDSs in one list and operate on each file to extract essential information prior to appending
os.chdir('C:/PhD Research/Paper 1 - Extraction/Raw/artificial_lds/')
import glob

## creating master df
df_append_all = pd.DataFrame([])

## looping over all LDS files and take important data
for item in glob.glob('lds_ex*.xlsx'):
    df = pd.read_excel(item, sheet_name = 'Extraction_data_entry', header=None)
    
    # memorizing all necessary constant values
    dust_mass = round(df.loc[2,3],3)
    ExpN = item[-22:-19]
    filtertype = item[27:30]
    tdn = item[15:19]
    Exdate = item[-11:-5]
    
    # rereading with the rid of first 10 rows to make a structured data frame
    df = pd.read_excel(item, sheet_name = 'Extraction_data_entry', header=10)
    
    # calculating new variables using memorized values
    df['dustmass'] = dust_mass
    df['ExpN'] = int(ExpN)
    df['ft'] = filtertype
    df.replace({'ft':label_filter_type1}, inplace = True)  
    df['td'] = tdn
    df.replace({'td':label_test_dust}, inplace = True) 
    df['Mass_C'] = df['M_ph_full'] - df['M_ph_clean']
    
    # Getting rid of extra columns
    varlist_drop = stata_varlist_split('Duration_min M_ph_clean M_ph_full M_ph_dumped M_vd M_vs Initials')
    df.drop(varlist_drop, axis = 1, inplace = True)
    
    # Convert to percentages
    df['M_C'] = df['M_C']*100
    df['M_C_cum'] = df['M_C_cum']*100
    
    # Append to the data from previous run of the loop
    df_append_all = df_append_all.append(df)
    
####################################################################
### Step 2: Refining, sorting and creating new important columns ###
####################################################################

## Removing test dust samples other than ISO A2 and ASHRAE #2
df_append_all = df_append_all[~(df_append_all['td'] == 'iso1' )]
df_append_all['td'] = df_append_all['td'].astype(int)
df_append_all.sort_values(['ExpN', 'Cycle_N'], inplace = True)
df_append_all.reset_index(inplace = True, drop = True)

new_columns = ['ExpN',  'Cycle_N', 'ft', 'td', 'M_filter_post', 'M_filter_change',
               'M_filter_change_cum', 'M_d', 'M_d_cum', 'M_s', 'M_s_cum', 'E', 'E_cum',
               'C', 'D', 'CE', 'CE_cum', 'M_C', 'M_C_cum', 'dustmass',  'Mass_C']
    
df_append_all = df_append_all[new_columns]

## Defining new variables for:
# 1) Total dust recovery - single cycle and cumulative (M_t and M_t_cum), 
# 2) Sieve recovery efficiency - single cycle and cumulative (sCE and sCE_cum), 
# 3) Total recovery efficiency - single cycle and cumulative (tCE and tCE_cum),
# 4) After-seive recovery ratio, the ratio of dust recovered by after sievel per total recovery - single cycle and cumulative (d_t_rat and d_t_rat_cum)

df_append_all['M_t'] = df_append_all['M_d'] + df_append_all['M_s']
df_append_all['M_t_cum'] = df_append_all['M_d_cum'] + df_append_all['M_s_cum']

df_append_all['sCE'] = (df_append_all['M_s'] / df_append_all['dustmass']) * 100
df_append_all['sCE_cum'] = (df_append_all['M_s_cum'] / df_append_all['dustmass']) * 100

df_append_all['tCE'] = ((df_append_all['M_d'] + df_append_all['M_s'])/df_append_all['dustmass']) * 100
df_append_all['tCE_cum'] = ((df_append_all['M_d_cum'] + df_append_all['M_s_cum'])/df_append_all['dustmass']) * 100

df_append_all['d_t_rat'] = df_append_all['M_d'] / df_append_all['M_t']
df_append_all['d_t_rat_cum'] = df_append_all['M_d_cum'] / df_append_all['M_t_cum']

#################################################################################
### Step 3: Merging LDS master df with filter loading data, QA, and exporting ###
#################################################################################

## Merging with filter_master_loading
lat_join = filter_loading_master[['ExpN','lat']]
df_append_all = pd.merge(df_append_all, lat_join, on = 'ExpN', how = 'left')  # left to not include the EXPN = 8 corresponding to iso1 test dust

## Data QA, Getting rid of bad data (negative collection and dump efficiency (due to super small values and measurement uncertainties))
for col in ['C', 'D']:
    df_append_all.loc[df_append_all[col] < 0, col] = np.nan


## Exporting and Loading Processed Data
export_path = backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Processed\artificial')
df_append_all.to_excel(export_path + '/artl_dataset_summary.xlsx', index=False)

varlist = stata_varlist_split('ExpN Cycle_N M_d_cum M_s_cum M_t_cum CE_cum sCE_cum tCE_cum d_t_rat_cum ft td dustmass M_filter_change_cum')
df_append_all_aggmax = df_append_all.groupby('ExpN', as_index = False).agg('max')
df_append_all_aggmax = df_append_all_aggmax[varlist]

df_append_all_aggmax.to_excel(export_path + '/artl_dataset_summary_collapsed.xlsx', index=False)
