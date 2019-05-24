"""
This module spits out demand charge profiles and csv files for the 4 meters.
Inputs are year and a meter among the four (i.e., PQube3PTot', 'PkFltM1AntPTot', 'PkFltM2TelPTot', 'PkFltM3SciPTot')

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

def demand_profile(mter, yr):
    """ Inputs are meter ('PQube3PTot', 'PkFltM1AntPTot', 'PkFltM2TelPTot', 'PkFltM3SciPTot') and years ('2017', '2018', '2019') """

    dirn = "../demand_acep/Data/" + yr + "/"
    dirName = [dirn+i+"/" for i in os.listdir(dirn)]
    dirName.sort()

        # dirName is a list of months in a year
        for i in dirName:
            Name = [i+j for j in os.listdir(i)]
            Name.sort()

        # Name is a list of days in a month
            y = pd.DataFrame()
            vname = []
            yname = []
            justonce = True
            for i in Name:
                fname = os.listdir(i)

                ind = []
                for j in fname:
                    ind.append(re.search(mter, j))
                l=[i for i in range(len(ind)) if ind[i] != None]
                fname = [fname[i] for i in l]
                fname.sort()

                if len(fname) == 1:
                    psiCDF = PsiNetcdf(netCDF4.Dataset(os.path.join(i,fname[0]),'r'))
                    v = list(np.round(list(psiCDF.cdf['value'][2:]),0))
                    t = list(psiCDF.cdf['time'][1:])

                    if mter == 'PQube3PTot':
                        v = list(np.round(np.array(v)/1000, 0))

                    if (t[-1] - t[0]) > 86000:
                        ti = t[1:] - np.min(t)
                        tim = np.round(ti/ 900, 0)
                        dte = re.search("[0-9]{4}-[0-9]{2}-[0-9]{2}", fname[0])[0]
                        da = pd.DataFrame({'x': tim, 'y': v}).groupby('x')['y'].mean()
                        fin = pd.DataFrame(da)
                        fin['y'] = np.round(fin['y'], 1)
                        fin["date"] = dte
                        y = pd.concat([y, fin])

                    if justonce:
                        vname = re.sub("PokerFlatResearchRange-PokerFlat-", "", re.sub("@.*$", "" , fname[0]))
                        yname = psiCDF.cdf.variables['value'].getncattr('Units')
                justonce=False

            dname = re.sub('/', '-', re.search("[0-9]{4}/[0-9]{2}", Name[0])[0]) + '-' + mter

            fig, ax = plt.subplots(figsize=(18,6))
            for name, group in y.groupby(['date']):
                group.plot(y= 'y', ax=ax, label=name)
            plt.ylabel(yname)
            plt.title('{0}'.format(vname))
            fig.savefig(dname+".pdf", bbox_inches='tight')

            y.to_csv(dname)

    return

# demand_profile('PQube3PTot', '2018')
