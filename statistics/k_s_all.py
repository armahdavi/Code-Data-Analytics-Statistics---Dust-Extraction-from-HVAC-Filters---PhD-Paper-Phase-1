# -*- coding: utf-8 -*-
"""
Program to run Kolmogorov Smirnov (K-S) test on the PSDs of the test dust and recovered dust samples for each experiment
It calls a function, "two_sample_k_s_test_psd", from "mastersizer_all.py" file that unstack PSD graphs from a distribution curve.

@author: alima
"""

## Importing and reading essential modules and functions
import sys
sys.modules[__name__].__dict__.clear()
import pandas as pd

exec(open('C:/PhD Research/Generic Codes/notion_corrections.py').read())
exec(open('C:/PhD Research/Generic Codes/mastersizer_all.py').read())

####################################################
### Step 1: Reading PSD data: test and recovered ###
#################################################### 

## Reading PSDs of the test and recovered dust samples prior to K-S test
df = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Raw\psd\artl_v_psd_master.xlsx'))
psd_list = list(list(df.columns))[1:]
psd_list = [x for x in psd_list if 'mean' in x if 'hd' in x if 'r2' not in x] # keeping the good samples and getting rid of bad ones

#############################################################
### Step 2: Running k-S test over test and recovered dust ###
#############################################################

## Running K-S tests over test and recovered samples and collecting the results in a dictionary
k_s_p_values = {}

for psd in psd_list:
    if psd[9:13] == 'ash2':
        p_value = two_sample_k_s_test_psd(df, psd, 'Eval_001_ash2_11e_td_171128_am_mean')
        k_s_p_values[psd[5:8]] = p_value
    
    if psd[9:13] == 'iso2':
        p_value = two_sample_k_s_test_psd(df, psd, 'Eval_010_iso2_11e_td_180326_am_mean')
        k_s_p_values[psd[5:8]] = p_value

## Saving and exporting results
k_s_all = pd.DataFrame(k_s_p_values.items(), columns = ['ExpN','P Value']).sort_values('ExpN')
k_s_all.to_excel(backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Processed\artificial') + '/k_s_all.xlsx', index = False)
