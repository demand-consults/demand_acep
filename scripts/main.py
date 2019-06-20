# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 09:26:41 2019

@author: tcmorgan2
"""

import netCDF4
import matplotlib as ply
import os
import PSINetcdf #assumes you are running from the same directory

#The directory where your file(s) are located
dirName = "C:\\Users\\tmorga22\\Documents\\PokerFlats\\PokerFlats_2017\\Data\\RawData\\03\\01"

#the file you want to read
#naming convention is: studySite-MeterNameVariableName@datetime@duration@Frequency.nc
fname = "PokerFlatResearchRange-PokerFlat-PkFltM2TelVbc@2019-03-01T092003Z@PT23H@PT140F.nc"
#make it a netcdf object
cdf = netCDF4.Dataset(os.path.join(dirName,fname),'r')

#pass it to the PSI netcdf tool handler
psiCDF = PsiNetcdf(cdf)

#list attributes contained in the file (all PSI netcdf are time vs value)
#the parameter name is in the file name
psiCDF.previewNetcdf()

#plot the values in the file and save the plot as a pdf
#You can provide any variable name you want to appear on the plot
psiCDF.plotNetCDF('Voltage B-C',True)