# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:16:49 2022

@author: Joy
"""

import numpy as np
import rasterio
import os
import matplotlib.pyplot as plt
import pandas as pd


rootdir = r'E:\Cordex_Data\India_Final_Cordex\India_States_CDD_HDD\West_Bengal_CDD_HDD\West_Bengal_Population\Population'
extensions = ('.tif')

file_list = []
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext in extensions:
            file_list.append(os.path.join(subdir, file))
#final_files = file_list[:]


file_1 =file_list[16:19]
file_2 = file_list[0:16]   
final_files = file_1 + file_2



Population=[]
for ras in final_files:
    raster = rasterio.open(ras) 
    array = raster.read()
    array = np.asarray(array.reshape(array.shape[1], array.shape[2]))
    array[array<0]=np.nan
    array[array==255]=np.nan
    Population.append(np.nansum(array))


Pop_actual = np.array(Population)
Pop_Million = np.array(Population)/1000000

#dates = pd.date_range(start='1/1/2020',end="31/12/2099", freq='Y')
dates= np.arange(2010, 2101, 5)

# Saving data into dataframe

df = pd.DataFrame(dates, columns=['Year'])
df["West_Bengal_Population_Numbers"]=Pop_actual
df["West_Bengal_Population_Millions"]=Pop_Million
df.to_csv("West_Bengal_Population_2010_2100.csv", index=False)


plt.style.use("fivethirtyeight")
 
# setting figure size to 12, 10
plt.figure(figsize=(12, 10))

plt.plot(dates[3: -1],Pop_Million[3:-1],'b')
plt.xlabel("Years")
plt.ylabel("Population (Millions)")
plt.title("West_Bengal Population [SSP2]")


