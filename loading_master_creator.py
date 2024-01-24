# -*- coding: utf-8 -*-
"""
Program to make a filter artificial loading master spreadsheet from the laoding lab data sheet

@author: alima

"""

import sys
sys.modules[__name__].__dict__.clear()


import pandas as pd
import os
os.chdir(r'C:\PhD Research\Generic Codes\Generic Codes')
from notion_corrections import backslash_correct, stata_varlist_split

###############################################
### Step 1: Importing raw file and refining ###
###############################################

# Import
file  = backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\PhD - Extraction\Raw\artificial_lds\LDS_Filter_Loading_Master_MAIN_test.xlsx')
filter_loading_master = pd.read_excel(file)

# Refine 
varlist = 'Filter_ID Date Start_time Loading_area_loc td_sample_old gf_sample_old ex_sample_old si_sample_old Test_purpose td_sample gf_sample ex_sample si_sample '
# copied from Stata, otherwise had to do it manually
new_drop_varlist = stata_varlist_split(varlist)
filter_loading_master.drop(new_drop_varlist, axis = 1, inplace=True)
filter_loading_master['Loading_area_type'] = filter_loading_master['Loading_area_type'].str.lower()

############################################################
### Step 2: Defining new columns for below key variables ###
############################################################

# 1- dust sprinkled over the filter,
filter_loading_master['Dust_sprinkled_m'] = filter_loading_master['Petridish_w_dust_m'] - filter_loading_master['Petridish_wo_dust_m']

# 2- dust loaded in the filter (indicated by filter mass change)
filter_loading_master['Filter_m_change'] = filter_loading_master['M_filter_pre'] - filter_loading_master['M_filter_blank']

# 3- dust flown into after-filter back vacuum sampler,
filter_loading_master['Flow_dust_m'] = filter_loading_master['Post_hepa_sampler_m'] - filter_loading_master['Pre_hepa_sampler_m']

# 4- Dust lost through the loading system:  (1) - sum(2,3) 
filter_loading_master['Lost_dust_m'] = filter_loading_master['Dust_sprinkled_m'] - (filter_loading_master['Filter_m_change'] + filter_loading_master['Flow_dust_m'])

# 5- Mass closure during loading process - defined as the measurable mass per totatl dust sprinkled mass: sum(2,3)/(1)
filter_loading_master['Mass_closure'] = ((filter_loading_master['Filter_m_change'] + filter_loading_master['Flow_dust_m'])/ filter_loading_master['Dust_sprinkled_m']) * 100

# 6- Loading efficiency - defined as the mass of dust loaded in filter per total mass sprinkled: (2)/(1)
filter_loading_master['Loading_eff'] = (filter_loading_master['Filter_m_change']/filter_loading_master['Dust_sprinkled_m']) * 100


#############################################################################
### Step 3: Labelling all categorical columns for later convenient coding ###
#############################################################################

exec(open('C:/PhD Research/Generic Codes/labels_all.py').read())
filter_loading_master = filter_loading_master.replace({'Filter_type': label_filter_type1})
filter_loading_master = filter_loading_master.replace({'Test_dust': label_test_dust}) 
filter_loading_master = filter_loading_master.replace({'Loading_area_type': label_loading_area_type})

# Renaming and sorting
new_col_name = {'Filter_type': 'ft',
                'Test_dust': 'td',
                'Loading_area_type': 'lat',
                'Experiment_N': 'ExpN'}

filter_loading_master.rename(columns = new_col_name, inplace = True)
filter_loading_master.sort_values(['ft', 'td', 'lat'], inplace = True)
filter_loading_master.reset_index(inplace=True, drop = True)

# Save and export
export_path = backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Processed\artificial')
filter_loading_master.to_excel(export_path + '/filter_loading_master.xlsx', index=False)


