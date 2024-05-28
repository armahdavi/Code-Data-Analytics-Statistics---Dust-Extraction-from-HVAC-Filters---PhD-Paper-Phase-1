# -*- coding: utf-8 -*-
"""
This program has two functions:
    1) backslash_correct, which conversts "\" characters to "/" (readable in Python and Stata)
    2) stata_varlist_split, which converts stata varlist to a python list which is suitable for pandas dataframe
@author: alima
"""


def backslash_correct(path):
    path = path.replace('\\' , '/')
    path = path.replace('//' , r'/')
    return path

## Ex. 'var1 var2 var3 ...' --> ['var1', 'var2', 'var3', ....]
## does not work for python if stata varlist contains part of variable name. e.g., star for start_time
def stata_varlist_split(varlist):
    varlist = varlist.split(" ")
    return varlist
        
