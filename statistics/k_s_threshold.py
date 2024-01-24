# -*- coding: utf-8 -*-
"""
The purpose of this program is to see, between the two samples: 'Eval_010_iso2_11e_hd_180326_am_mean', 'Eval_010_iso2_11e_hd_180326_am_r2_mean', which size is the threshold below which the K-S tests confirms the two samples come from the same distribution.

@author: alima
"""

## Essential modules and files
import sys
sys.modules[__name__].__dict__.clear()
import pandas as pd

exec(open('C:/PhD Research/Generic Codes/notion_corrections.py').read())
exec(open('C:/PhD Research/Generic Codes/mastersizer_all.py').read())

#################################
### Step 1: Readigng PSD data ###
#################################

df_collapsed = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Processed\artificial\artl_dataset_summary_collapsed.xlsx'))
# exp_list = df['ExpN'].unique()

df = pd.read_excel(backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Raw\psd\artl_v_psd_master.xlsx'))
psd_list = list(list(df.columns))[1:]
df = df[["Size", 'Eval_010_iso2_11e_hd_180326_am_mean', 'Eval_010_iso2_11e_hd_180326_am_r2_mean']]

##########################################
### Step 2: Finding the threshold size ###
##########################################

def k_s_threshold(threshold):
    new_df = df[(df['Size'] <= threshold)]
    p_value = two_sample_k_s_test_psd(new_df, 'Eval_010_iso2_11e_hd_180326_am_mean', 'Eval_010_iso2_11e_hd_180326_am_r2_mean')
    return p_value
    
threshold_p_value = k_s_threshold(61)

'''
instead of 61, any other number (representing size in terms of micron) can be placed.
Re-running with larger values than 61 (e.g., 100 micron) shows p<0.05 meaning distributions are different.
Re-running with smaller values than 61 (e.g., 40 micorn) shows p>0.05 meaning distributions are the same.

'''
