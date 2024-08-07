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

### Reading CDD from netcdf files 

CDD_dir = r'E:\Cordex_Data\India_Final_Cordex\India_States_CDD_HDD\West_Bengal_CDD_HDD\West_Bengal_CDD'
extensions = ('.nc')

cdd_file_list = []
for subdir, dirs, files in os.walk(CDD_dir):
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext in extensions:
            cdd_file_list.append(os.path.join(subdir, file))
        

#cdd_file_1 =[cdd_file_list[18]]
#cdd_file_2 = cdd_file_list[0:3]  
#cdd_file_3 = cdd_file_list[3:18]    
#cdd_file_list = cdd_file_2 + cdd_file_1 + cdd_file_3




CDD=[]
for ras in cdd_file_list:
    raster = rasterio.open(ras) 
    array = raster.read()
#    print(array.shape)
    array = np.asarray(array.reshape(array.shape[1], array.shape[2]))
    array[array<0]=np.nan
    CDD.append((array))
    
Final_CDD = np.array(CDD)
#Final_CDD = Final_CDD[:, :713, :321]

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
for ras in final_files:
    raster = rasterio.open(ras) 
    array = raster.read()
#    print(array.shape)
    array = np.asarray(array.reshape(array.shape[1], array.shape[2]))
    array[array<0]=np.nan
    array[array==255]=np.nan
    Population.append((array))

Final_Population = np.array(Population)
#Final_Population = Final_Population[:, :191, :142]

df = pd.read_csv(r"E:\Cordex_Data\India_Final_Cordex\India_States_CDD_HDD\West_Bengal_CDD_HDD\West_Bengal_Population\West_Bengal_Population_2010_2100.csv")

Tot_Population=df['West_Bengal_Population_Numbers'][:]
#Gujarat_Future_Population = Gujarat_Future_Population.reset_index(drop=True)

Pop_CDD_final= []
without_pop_CDD =[]
for i,j,k in zip(Final_CDD,Final_Population,Tot_Population):
    Uk_CDD = np.nanmean(i)
    CDD_Pop = np.nansum((i*j))
    Pop_W_CDD = CDD_Pop/k
    without_pop_CDD.append(Uk_CDD)
    Pop_CDD_final.append(Pop_W_CDD)

Pop_CDD_final=np.array(Pop_CDD_final)

dates= np.arange(2010, 2101, 5)

# Saving data into dataframe

df1 = pd.DataFrame(dates, columns=['Year'])
df1["West_Bengal_Population_Numbers"]=Tot_Population
df1["CDD"]=without_pop_CDD
df1["POP_W_CDD"]=Pop_CDD_final

df1.to_csv("West_Bengal_CDD_2010-2100.csv", index=False)

print("Processing Over")

