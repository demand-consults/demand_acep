"""
This module detects abnormal date folders from the raw data.


"""

# %% Imports

import numpy as np
import pandas as pd
%matplotlib inline
import matplotlib.pyplot as plt
import os
import re
import netCDF4
from PSINetcdf import * #assumes you are running from the same directory
import csv
from itertools import zip_longest

# %%

def abnormal_date(dirn):
    '''This function takes a list of year path and retunrs a list of csv and plots indicating abnormal dates'''
    for h in dirn:
        dirName = [h+i+"/" for i in os.listdir(h)]
        dirName.sort()

        # dirName is a list of months in a year
        y = []
        x = []
        for i in dirName:
            Name = [i+j for j in os.listdir(i)]
            Name.sort()

        # Name is a list of days in a month 
            ea = []
            nam = []
            for j in Name:
                fname = os.listdir(j)

                ind = []
                for k in fname:
                    ind.append(re.search('.nc', k))
                l=[i for i in range(len(ind)) if ind[i] != None]
                fname = [fname[i] for i in l] 
                fname.sort()

                fname.sort()
                nam.append(re.search("[0-9]{4}/[0-9]{2}/[0-9]{2}", j)[0])
                ea.append(len(fname))

            y.extend(nam)
            x.extend(ea)
        
        da = pd.DataFrame({'Date': y, '# of files': x})
        dname = re.search("[0-9]{4}", h)[0]
        da.to_csv(dname)
        ax = da.plot(['Date'], ['# of files'])
        fig = ax.get_figure()
        fig.savefig(dname+".pdf", bbox_inches='tight')

    return 
 
# dirn = ["../demand_acep/Data/2017/", "../demand_acep/Data/2018/", "../demand_acep/Data/2019/"]
# abnormal_date(dirn) 
