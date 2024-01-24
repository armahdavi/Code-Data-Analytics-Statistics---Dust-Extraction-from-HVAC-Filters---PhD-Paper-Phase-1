# -*- coding: utf-8 -*-
"""
This program is to append three series corresponding to three extraction processes along with their process names (E, C, and D 
corresponding to "Extraction", "Collection", and "Dump"). The outcome will be later used for a non-parametric rank-sum test

@author: alima
"""

import sys
sys.modules[__name__].__dict__.clear()
import pandas as pd

exec(open('C:/PhD Research/Generic Codes/notion_corrections.py').read())

path = backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Processed\artificial')
artl_dataset_summary = pd.read_excel(path + '/artl_dataset_summary.xlsx')

Eff_proc = pd.DataFrame([])

for item in ['E', 'C', 'D']:
    artl_dataset_summary['Eff'] = item
    temp_df = artl_dataset_summary[[item, 'Eff']]
    temp_df.rename(columns = {item: 'Eff Value'}, inplace = True)
    
    Eff_proc = Eff_proc.append(temp_df)
    Eff_proc.reset_index(drop = True, inplace = True)
    


    
    