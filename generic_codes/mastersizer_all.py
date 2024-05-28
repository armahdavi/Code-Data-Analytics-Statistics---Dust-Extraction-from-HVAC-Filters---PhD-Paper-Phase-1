# -*- coding: utf-8 -*-
"""
This program processes the raw data of Malvern Mastersizer PSD measurement equipment. 
Raw files include rows that correspond to following:
    1) Record number
    2) Bin measurements (92 bins overall) as set in Mastersizer options
    3) Dx values (D10, D50, and D90)
    4) Other measurement properties: sample name, measurement date/time, laser properties (RI, AI, particle densiti), 
    ultrasound properties, original record number, file path etc.,

@author: alima
"""

import pandas as pd
import numpy as np
import os
from notion_corrections import backslash_correct # required for all path corrections
exec(open(backslash_correct('C:\PhD Research\Generic Codes\notion_corrections.py')).read())



### Function 1: mastersizer_input
### A generic function that reads raw mastersizer file and returns a processed one
### must not have .xlsx at the end of importfile
### works only for csv files

def mastersizer_input(path,importfile,exportfile):
    getpath = backslash_correct(path) # corrects path if \ is used instead of /
    importfilepath = getpath + '/' + importfile 
    exportfilepath = getpath + '/' + exportfile
    # exportfilepath = path + '/' + exportfile
    if importfilepath[-4:] == '.csv': # flexible if import file with or without .csv at end
        importfilepath = importfilepath[:-4]
    
    df = pd.read_csv(importfilepath + '.csv', header = None)
        
    ## too see if the psd is distributed or cumulative
    cumulative = 0 
    if df.iloc[1, 92] > 0.99: # if the last bin of psd is close to 100% meaning it is cumulative
        cumulative = 1
        
    ## making all sizes in a separate series to join later with psd (index are kept the same)
    size_series = df.iloc[0, :].loc[1:92].rename('Size').astype(float)

    df.rename(columns = {96: 'Sample Name'}, inplace = True)
    
    ## creating a dataframe to append the processed statistical results of the runs for each bin
    df_collapse_all = pd.DataFrame([])
    for agg_type in ['count', 'mean', 'median', 'min', 'max', 'std']:
        df_collapse = pd.merge(df.iloc[1:,1:93], 
                               df.loc[1:,'Sample Name'], 
                               left_index=True, right_index=True).groupby('Sample Name', 
                                                                          as_index = False).agg(agg_type)
        
        df_collapse['stat'] = agg_type
        df_collapse['Sample Name'] = df_collapse['Sample Name'] + '_' + df_collapse['stat']
        df_collapse.set_index('Sample Name', inplace = True)
        del df_collapse['stat']
        df_collapse_all = df_collapse_all.append(df_collapse)

        
    ## Transposing the dataframe so bins (size) become one column and everything is reported as a function of particle size   
    df_collapse_all = df_collapse_all.T
    old_cols = list(df_collapse_all.columns)

    ## merging the transposed df to particle size    
    df_collapse_all = df_collapse_all.merge(size_series, left_index=True, right_index=True)
    
    ## re-ordering with size    
    cols = ['Size']
    cols.extend(old_cols)
    df_collapse_all = df_collapse_all[cols]
    
    ## creating the processed file xlsx based on whether or not cumulative or distributed
    if cumulative == 0:
        if exportfilepath[-4:] == '.csv':
            exportfilepath = exportfilepath[:-4]
            df_collapse_all.to_excel(exportfilepath + '.xlsx', index=False)
        else:
            df_collapse_all.to_excel(exportfilepath + '.xlsx', index=False)
    else:
        if exportfilepath[-4:] == '.csv':
            exportfilepath = exportfilepath[:-4]
            df_collapse_all.to_excel(exportfilepath + '_cumulative.xlsx', index=False)
        else:
            df_collapse_all.to_excel(exportfilepath + '_cumulative.xlsx', index=False)
    
    return df_collapse_all


### Function 2: mastersizer_input_v2
### The difference between mastersizer_input and mastersizer_input_v2 is that v2 has the import and export paths separate



def mastersizer_input_v2(importpath,exportpath,importfile,exportfile):
    getpathimport = backslash_correct(importpath) # corrects path if \ is used instead of /
    getpathexport = backslash_correct(exportpath)
    importfilepath = getpathimport + '/' + importfile 
    exportfilepath = getpathexport + '/' + exportfile
    # exportfilepath = path + '/' + exportfile
    if importfilepath[-4:] == '.csv': # flexible if import file with or without .csv at end
        importfilepath = importfilepath[:-4]
    
    df = pd.read_csv(importfilepath + '.csv', header = None)
    
    ## too see if the psd is distributed or cumulative       
    cumulative = 0 
    if df.iloc[1, 92] > 0.99: # if the last bin of psd is close to 100% meaning it is cumulative
        cumulative = 1
        
    ## maiking all sizes in a separate series to join later with psd (index are kept the same)
    size_series = df.iloc[0, :].loc[1:92].rename('Size').astype(float)

    ## locating the index of sample name    
    sample_col = [col for col in list(df.columns) if df.iloc[0,col] == 'Sample Name'][0]
    df.rename(columns = {sample_col: 'Sample Name'}, inplace = True)

    ## Making count, median, mean, min, and max of runs per sample name   
    for agg_type in ['count', 'median', 'mean', 'min', 'max']: # need to find a way better than globals
        globals()['df_collapse_%s' %agg_type] = pd.merge(df.iloc[1:,1:93], 
                                                        df.loc[1:,'Sample Name'], 
                                                        left_index=True, right_index=True).groupby('Sample Name', 
                                                                                                   as_index = False).agg(agg_type)
        
        globals()['df_collapse_%s' %agg_type]['stat'] = agg_type
        # globals()['df_collapse_%s' %agg_type].set_index('Sample Name', inplace = True)
    df_collapse_min.iloc[:,1:93] = (df_collapse_mean.iloc[:,1:93] - df_collapse_min.iloc[:,1:93]).round(3)
    df_collapse_max.iloc[:,1:93] = (df_collapse_max.iloc[:,1:93] - df_collapse_mean.iloc[:,1:93]).round(3)

    ## Appending all count, median, mean, min, and max calculated from runs per sample
    df_collapse_all = pd.concat([df_collapse_count, df_collapse_median, df_collapse_mean, df_collapse_min, df_collapse_max])
    
    df_collapse_all['Sample Name'] = df_collapse_all['Sample Name'] + '_' + df_collapse_all['stat']
    del df_collapse_all['stat']
    df_collapse_all.set_index('Sample Name', inplace = True)
    
    ## Transposing the dataframe so bins (size) become one column and everything is reported as a function of particle size   
    df_collapse_all = df_collapse_all.T
    
    old_cols = list(df_collapse_all.columns)
    
    ## merging the transposed df to particle size    
    df_collapse_all = df_collapse_all.merge(size_series, left_index=True, right_index=True)
    
    ## re-ordering with size    
    cols = ['Size']
    cols.extend(old_cols)
    df_collapse_all = df_collapse_all[cols]
    
    ## creating the processed file xlsx based on whether or not cumulative or distributed
    if cumulative == 0:
        if exportfilepath[-4:] == '.csv':
            exportfilepath = exportfilepath[:-4]
            df_collapse_all.to_excel(exportfilepath + '.xlsx', index=False)
        else:
            df_collapse_all.to_excel(exportfilepath + '.xlsx', index=False)
    else:
        if exportfilepath[-4:] == '.csv':
            exportfilepath = exportfilepath[:-4]
            df_collapse_all.to_excel(exportfilepath + '_cumulative.xlsx', index=False)
        else:
            df_collapse_all.to_excel(exportfilepath + '_cumulative.xlsx', index=False)
    
    return df_collapse_all



### Function 3: mastersizer_d_input 
### The function extracts dx information from a raw mastersizer file. 
### It is compatible to any no. of dxs
### Compatible with csv files only for now
### Same algorithm as bins in the above functions but for d-values only, escept no transpose

 
def mastersizer_d_input(importpath,exportpath,importfile,exportfile):
    getpathimport = backslash_correct(importpath) # corrects path if \ is used instead of /
    getpathexport = backslash_correct(exportpath)
    importfilepath = getpathimport + '/' + importfile 
    exportfilepath = getpathexport + '/' + exportfile
    # exportfilepath = path + '/' + exportfile
    if importfilepath[-4:] == '.csv': # flexible if import file with or without .csv at end
        importfilepath = importfilepath[:-4]
    
    df = pd.read_csv(importfilepath + '.csv')
    d_col = [col for col in df.columns if 'Dx' in col] # compatible even with less no of Dxs
    df = df[['Sample Name'] + d_col]
    
    i = 1
    for agg_type in ['count', 'median', 'gmean', 'gstd', 'min', 'max']:
        if agg_type == 'gmean':
            df.groupby('Sample Name', as_index = False)[d_col].apply((lambda x: np.exp(np.mean(np.log(x)))))
        elif agg_type == 'gstd':
            df.groupby('Sample Name', as_index = False)[d_col].apply((lambda x: np.exp(np.std(np.log(x))))) # remember gstd = exp(std(log(x)))
        else:
            df_collapse = df.groupby('Sample Name', as_index = False)[d_col].agg(agg_type) # unlike psd, min and max in d is absolute values and not errors
        
        df_collapse['stat'] = agg_type
        
        if i == 1: 
            df_collapse_all = df_collapse 
            i += 1
        else:
            df_collapse_all = df_collapse_all.append(df_collapse)

    if exportfilepath[-4:] == '.csv':
        exportfilepath = exportfilepath[:-4]
        df_collapse_all.to_excel(exportfilepath + '.xlsx', index=False)
    else:
        df_collapse_all.to_excel(exportfilepath + '.xlsx', index=False)
    
    return df_collapse_all
    



### Function 4: two_sample_k_s_test_psd
### A specific Kolmogorov smirnov test for comparing two compact size distributions.
### Might need to add more inputs for more sophistications required in the future.
### Both samnples must be from a same dataset (or otehrwise repeated input is needed which is unnecessary in most cases)
### Size scales must be the same

def two_sample_k_s_test_psd(df_name, sample1_name, sample2_name):
    import pandas as pd
    import numpy as np
    from scipy.stats import ks_2samp
          
    temp = df_name.set_index('Size')
    temp.index.name = 'index'
    
    sample1 = round(temp[sample1_name]*1000,0)
    sample2 = round(temp[sample2_name]*1000,0)
    
    sample1 = pd.Series(np.repeat(sample1.index, sample1))
    sample2 = pd.Series(np.repeat(sample2.index, sample2))
    
    return round(ks_2samp(sample1, sample2)[1],3)


### Function 5: shapiro_wilk_psd
### Shapiro Wilk test for checking the normality of a given mastersizer PSD
### Must have the size as the index of the series (first input)
### The second input is the name of the series you want to decompact for sw test

def shapiro_wilk_psd(df_name, sample_name):
    import pandas as pd
    import numpy as np
    from scipy.stats import shapiro
    
    temp = df_name.set_index('Size')
    temp.index.name = 'index'
    sample = round(temp[sample_name]*10,0)
    sample = pd.Series(np.repeat(sample.index, sample))
    sample = np.log10(sample)
    return round(shapiro(sample)[1],3)
    
