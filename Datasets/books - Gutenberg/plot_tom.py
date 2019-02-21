# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 08:32:23 2019

@author: user
"""

# https://www.zanaducloud.com/CC6612B2-B42A-4765-A0C8-4FDB3CEF50E2
import seaborn as sns
from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
sns.set_palette("deep", desat=.6)
sns.set_context(rc={"figure.figsize": (12, 9)})

# heatmap

mdf = pd.read_csv('C:/Users/user/Documents/Python Scripts/thesis/books/heatmap1.csv',header=None,index_col=False,skiprows=1) 
#sns.heatmap(mdf, xticklabels=5 ,fmt="f" )
#result=mdf.pivot_table(mdf,index = ['chapter2'], values = 'KLD',columns = 'result', aggfunc = 'sum')
mdf_transposed = mdf.transpose()
mdf.set_index('chapter2',inplace=True)
mdf.transpose() 

sns.heatmap(mdf_transposed, annot=True, fmt="g")

plt.show()

#sns.heatmap(mdf, xticklabels=5 ,fmt="f" , linewidths=.05)
#sns.heatmap(mdf, fmt="f", linewidths=.1 ,   cbar=False) # annot=True,

#sns.heatmap(mdf, cbar=False) #Remove color bar
#sns.plt.show()

#sns.heatmap(mdf, xticklabels=1 ,  fmt="f") #Hide a few axis labels to avoid overlapping
sns.plt.show()