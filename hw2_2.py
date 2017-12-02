# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 12:06:50 2017

@author: letty
"""

import pandas as pd
import geopy
from geopy.distance import great_circle
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


#read, adjust data
file = open('HW2_tsp.txt', 'r')
file = file.readlines()
data=pd.DataFrame(file[10:])
data.columns=['x']
data=data['x'].str.split(' ',expand=True)
data.columns=['city','latitude','longitude']
data["city"] = pd.to_numeric(data["city"])
data["latitude"] = pd.to_numeric(data["latitude"])/1000
data["longitude"] = pd.to_numeric(data["longitude"])/1000
data['position'] = data['latitude'].astype(str) +','+ data['longitude'].astype(str)
#data['position'] = data[data.columns[1:]].apply(lambda x: ','.join(x.dropna()),axis=1)




#calculate great circle distance of each pair of the city
#i did not divide it by 1000 in this calculation tho***
distance=list()
for i in range(38):
    for j in range(38):
        distance.append((great_circle(data.loc[i,'position'],data.loc[j,'position']).km))

chunks = [distance[x:x+38] for x in range(0, len(distance), 38)]

#turn into a distance matrix
city=list()
for i in range(1,39):
    city.append('city '+str(i))
matrix=pd.DataFrame(chunks,columns=city)

#Question a

lons = data['longitude'].tolist()
lats = data['latitude'].tolist()

plt.figure(figsize=(18,18))
plt.scatter(lons,lats)

#Question b/c
