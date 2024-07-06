# -*- coding: utf-8 -*-
"""
Practices over stastistical tests

@author: alima
"""

#### Rank sum test
from scipy.stats import ranksums, wilcoxon
import pandas as pd
import numpy as np

exec(open('C:/PhD Research/Generic Codes/notion_corrections.py').read())

path = backslash_correct(r'C:\PhD Research\Paper 1 - Extraction\Processed\artificial')
artl_dataset_summary = pd.read_excel(path + '/artl_dataset_summary.xlsx')

sample1 = artl_dataset_summary['C'].dropna()
sample2 = artl_dataset_summary['D'].dropna()
# must always drop nan to get accurate results (compared to STATA)
# sample1 = artl_dataset_summary['C']
# sample2 = artl_dataset_summary['D']

result = ranksums(sample1, sample2, alternative='two-sided')

#### Signed rank test
wilcoxon(np.array(df_sign_rank_all['M_d_cum_1']), np.array(df_sign_rank_all['M_d_cum_2']))
# data is exactly the same as those processed by STATA, bu the resylts are different. WHY?

result2 = ranksums(df_sign_rank_all['M_d_1'], df_sign_rank_all['M_d_2'], alternative='two-sided')
