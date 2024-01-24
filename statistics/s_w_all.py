# -*- coding: utf-8 -*-
"""
Program to run Shapiro-Wilk normality test on the test and recovered dust sample PSDs and return a normality 
p-value for every single PSD.
It runs a function, "shapiro_wilk_psd" from "mastersizer_all.py" which calculates the normality of a given PSD in the format used for this research. 
@author: alima
"""

## Calling essential modules and functions
import sys
sys.modules[__name__].__dict__.clear()
import pandas as pd

exec(open('C:/Career/Learning/Python Practice/Generic Codes/notion_corrections.py').read())
exec(open('C:/Career/Learning/Python Practice/Generic Codes/mastersizer_all.py').read())

##############################################
### Step 1: Reading PSD files and refining ###
##############################################

df = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Raw\psd\artl_v_psd_master.xlsx'))
psd_list = list(list(df.columns))[1:]

psd_list = [x for x in psd_list if 'mean' in x if ('hd' in x) | ('td' in x) if 'r2' not in x] # keeping the subject ones (not r2, and not except hd and td representing the after-sieve and test dust samples)

##################################################
## Step 2: Running S-W test and return p-value ###
##################################################

s_w_p_values = {}

for item in psd_list:
    if item[18:20] == 'td':
        key = item[5:8] + '_' + item[18:20]
        value = shapiro_wilk_psd(df,item)
        s_w_p_values[key] = value
    else:
        key = item[5:8] + '_' + item[18:20]
        value = shapiro_wilk_psd(df,item)
        s_w_p_values[key] = value
