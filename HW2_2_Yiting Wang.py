# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 00:36:12 2017

@author: Yiting
"""
# Question 2a
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

#read file
fhand = open('C:/MSBA17-18/4. Network Analytics/HW2/HW2_tsp.txt', 'r')

file = list()
loc = list()

for line in fhand:
    line = line.rstrip()
    file.append(line)

for i in file[10:]:
    loc.append(i.split(' '))

# transfer to dataframe
data = pd.DataFrame(loc)
data.columns = ["city", "latitude","longitude"]
data["latitude"] = pd.to_numeric(data["latitude"])/1000
data["longitude"] = pd.to_numeric(data["longitude"])/1000

# define a function to calculate the distance between two cities
def distance_on_unit_sphere(lat1, long1, lat2, long2):
    degrees_to_radians = math.pi/180.0
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians  
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
    arc = math.acos(cos)
    return arc*6373 # km between two cities

# calculate distance matrix
dist_matrix = np.zeros((38,38))

for a, b in combinations(range(38),2):
    dist = distance_on_unit_sphere(data.iloc[a, 1], data.iloc[a, 2], data.iloc[b, 1], data.iloc[b,2])
    dist_matrix[a][b] = dist
    dist_matrix[b][a] = dist

print(dist_matrix) 

# plot the latitude and longitude as a scatter plot
lons = data['longitude'].tolist()
lats = data['latitude'].tolist()
plt.figure(figsize=(18,18))
plt.scatter(lons,lats)