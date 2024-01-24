# -*- coding: utf-8 -*-
"""
Program to refine PSDs from all tests that have both pre-sieve and after-sieve PSDs measured (denoted by and hd)(for ASHRAE tests only; ISO tests do not have sieve fractions)
The program also refines more to keep the test that has all pre-sieve, after-sieve, and combined sieve PSDs (denoted by sc) along with ASHRAE#2 test dust PSD

@author: alima
"""

########################################################################
### Step 1: Import important modules, functions, and processed files ###
########################################################################

import sys
sys.modules[__name__].__dict__.clear()
import pandas as pd

# from notion_corrections import backslash_correct
exec(open('C:/PhD Research/Generic Codes/notion_corrections.py').read())
path = backslash_correct('C:\PhD Research\Paper 1 - Extraction\Raw\psd')

artl_v_psd_master = pd.read_excel(path + '/artl_v_psd_master.xlsx')
col_list = list(artl_v_psd_master.columns)


###############################################
### Step 2: Refining to keep important data ###
###############################################

## refining all the samples where both sd and hd are available
sn_list = [sn[4:9] for sn in col_list if 'sd' in sn]
sn_list = list(set(sn_list)) # the command set makes a set of uniqe values in a list. Need to put it in a list to convert from set to list

## Keeping all necessary samples
for sn in sn_list:
    temp_list = [col for col in col_list if sn in col]
    keep_list.extend(temp_list)

## Getting rid of non-min, max, and mean values (not useful for plotting). Also getting rid of extra samples (fg and gf; flow and gravitationl dust during loding)
keep_list = [col for col in keep_list if ('mean' in col) | ('min' in col) | ('max' in col)]
keep_list = [col for col in keep_list if ('_fg_' not in col) & ('_gf_' not in col)]

td_list = [col for col in col_list if ('_td_' in col) & 
                                                       ('ash2' in col) & 
                                                       (('mean' in col) | ('min' in col) | ('max' in col))]
keep_list.extend(td_list)
keep_list = ['Size'] + keep_list # Adding particle size to the list

artl_v_psd_master = artl_v_psd_master[keep_list]


## Exporting the created dataframe
artl_v_psd_master.to_excel(path + '/artl_v_psd_master_sieve.xlsx', index = False)


############################################################################
############ Step 3: Refining more to keep the test that has all ###########
### pre-, after-, and combine- sieve dust along with ASHRAE #2 test dust ###
############################################################################

core_list = [col[17:21] for col in list(artl_v_psd_master.columns)]
core_list = list(set(core_list))
core_list.pop(0)

i = 1
artl_psd_sieve = pd.DataFrame([])
for item in core_list:
    for stat in ['min', 'mean', 'max']:
        text = '%s%s' %(item,stat)
        text = text[1:]
        locals()['list%s%s' %(item,stat)] =  [col for col in keep_list if (item in col) & (stat in col)] 
        locals()['df%s%s' %(item,stat)] = pd.concat([artl_v_psd_master['Size'],
                                                     artl_v_psd_master[locals()['list%s%s' %(item,stat)]].agg(stat, axis=1)],
                                                     axis = 1).rename(columns = {0: text})
        if i == 1:
            artl_psd_sieve = locals()['df%s%s' %(item,stat)]
            i += 1
        else:
            artl_psd_sieve = artl_psd_sieve.merge(locals()['df%s%s' %(item,stat)], on = 'Size', how = 'outer')

## Exporting and saving the created dataframe
artl_psd_sieve.to_excel(backslash_correct('C:\PhD Research\Paper 1 - Extraction\Processed\artl_psd_sieve.xlsx'), index = False)
     
