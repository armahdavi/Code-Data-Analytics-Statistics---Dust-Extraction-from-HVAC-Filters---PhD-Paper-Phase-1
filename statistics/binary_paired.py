# -*- coding: utf-8 -*-
"""
Program to creat binary recovery data from cumulative recovery values after 1st and 2nd extraction cycles.
This program prepares the data paired available for a non-oparameteric signed rank test.
The signed rank test is performed elsewhere.

@author: alima
"""

### Importing and reading important modules, functions, and files
import sys
sys.modules[__name__].__dict__.clear()
import pandas as pd
# import math
import numpy as np

exec(open('C:/PhD Research/Generic Codes/notion_corrections.py').read())

#################################################################
### Step 1: Reading artificial recovery database and refining ###
################################################################# 

path = backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Processed\artificial')
df = pd.read_excel(path + '/artl_dataset_summary.xlsx')

## Refining the data to keep 1st and 2nd cycle of a test
df['keepdrop'] = 'drop'
Exp_list = df.loc[df['Cycle_N'] == 2, 'ExpN'].unique()

for item in Exp_list: # keeping all the tests with at least 2 cycles
    df.loc[df['ExpN'] == item,'keepdrop'] = 'keep'

df = df[~(df['keepdrop'] == 'drop')] # dropping higher cycle observations
df = df[~(df['Cycle_N'] >= 3)]

df_sign_rank_all = pd.DataFrame([])
col_list = stata_varlist_split("M_d M_d_cum M_s M_s_cum M_t M_t_cum CE CE_cum sCE sCE_cum tCE tCE_cum E C D M_C_cum")

#############################################################
### Step 2: Coupling the 1st and 2nd cycle and unstacking ###
#############################################################

for item in col_list:
    temp = df[['ExpN', 'Cycle_N', item]]
    temp[['ExpN', 'Cycle_N']] = temp[['ExpN', 'Cycle_N']].astype(str)
    temp.set_index(['ExpN', 'Cycle_N'], inplace = True)
    temp = temp.unstack('Cycle_N')
    
    df_sign_rank_all = pd.concat([df_sign_rank_all, temp], axis = 1)

df_sign_rank_all.columns = ['_'.join(x) for x in list(df_sign_rank_all.columns)]
a = list(df_sign_rank_all.columns)
new_col_list = ['ExpN'] + list(df_sign_rank_all.columns)

df_sign_rank_all['ExpN'] = df_sign_rank_all.index
df_sign_rank_all = df_sign_rank_all[new_col_list]

df_sign_rank_all.index.name = 'index'
df_sign_rank_all['ExpN'] = df_sign_rank_all['ExpN'].astype(int)
df_sign_rank_all.sort_values(['ExpN'], inplace = True)
df_sign_rank_all = df_sign_rank_all.reset_index(drop=True)

df_sign_rank_all_log = pd.DataFrame([])

## making a log value in the case of log-normal distributions
for col in a:
    df_sign_rank_all_log[col] = np.log10(df_sign_rank_all[col])

df_sign_rank_all_log.replace([np.inf, -np.inf], np.nan, inplace = True)

### Saving and exporting
export_path = backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Processed\artificial')
df_sign_rank_all.to_excel(export_path + '/sign_rank_all.xlsx', index=False)
df_sign_rank_all_log.to_excel(export_path + '/sign_rank_all_log.xlsx', index=False)

