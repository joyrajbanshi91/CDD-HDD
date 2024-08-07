# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:16:49 2022

@author: Joy
"""

import numpy as np
import rasterio
import os, glob
import matplotlib.pyplot as plt
import pandas as pd

### Reading HDD from netcdf files 

HDD_dir = r'E:\Cordex_Data\India_Final_Cordex\India_States_CDD_HDD\West_Bengal_CDD_HDD\West_Bengal_HDD'
extensions = ('.nc')

HDD_file_list = []
for subdir, dirs, files in os.walk(HDD_dir):
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext in extensions:
            HDD_file_list.append(os.path.join(subdir, file))



HDD=[]
for ras in HDD_file_list:
    raster = rasterio.open(ras) 
    array = raster.read()
#    print(array.shape)
    array = np.asarray(array.reshape(array.shape[1], array.shape[2]))
    array[array<0]=np.nan
    HDD.append((array))
    
Final_HDD = np.array(HDD)


Popdir = r'E:\Cordex_Data\India_Final_Cordex\India_States_CDD_HDD\West_Bengal_CDD_HDD\West_Bengal_Population\Population'
extensions = ('.tif')

file_list = []
for subdir, dirs, files in os.walk(Popdir):
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext in extensions:
            file_list.append(os.path.join(subdir, file))

file_1 =file_list[16:19]
file_2 = file_list[0:16]   
final_files = file_1 + file_2            
            
Population=[]
for ras in file_list:
    raster = rasterio.open(ras) 
    array = raster.read()
    array = np.asarray(array.reshape(array.shape[1], array.shape[2]))
    array[array<0]=np.nan
    array[array==255]=np.nan
    Population.append((array))

Final_Population = np.array(Population)


df = pd.read_csv(r"E:\Cordex_Data\India_Final_Cordex\India_States_CDD_HDD\West_Bengal_CDD_HDD\West_Bengal_Population\West_Bengal_Population_2010_2100.csv")

Tot_Population=df['West_Bengal_Population_Numbers'][:]


Pop_HDD_final= []
without_pop_HDD =[]
for i,j,k in zip(Final_HDD,Final_Population,Tot_Population):
    Uk_HDD = np.nanmean(i)
    HDD_Pop = np.nansum((i*j))
    Pop_W_HDD = HDD_Pop/k
    without_pop_HDD.append(Uk_HDD)
    Pop_HDD_final.append(Pop_W_HDD)

Pop_HDD_final=np.array(Pop_HDD_final)

dates= np.arange(2010, 2101, 5)

# Saving data into dataframe

df1 = pd.DataFrame(dates, columns=['Year'])
df1["West_Bengal_Population_Numbers"]=Tot_Population
df1["HDD"]=without_pop_HDD
df1["POP_W_HDD"]=Pop_HDD_final

df1.to_csv("West_Bengal_HDD_2010-2100.csv", index=False)


print("Processing Over")
