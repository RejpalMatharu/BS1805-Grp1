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

# read file
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

# plot the latitude and longitude as a scatter plot (credit to Letty...)
lons = data['longitude'].tolist()
lats = data['latitude'].tolist()
plt.figure(figsize=(18,18))
plt.scatter(lons, lats)


# Question 2b
# https://github.com/google/or-tools/blob/master/examples/python/tsp.py
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

def Distance(i, j):
    return dist_matrix[i][j]

routing = pywrapcp.RoutingModel(38, 1, 0)
search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

routing.SetArcCostEvaluatorOfAllVehicles(Distance)

assignment = routing.Solve()

if assignment:
    # Solution cost.
    print(assignment.ObjectiveValue())
    # Inspect solution.
    # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
    route_number = 0
    rount_list = []
    node = routing.Start(route_number)
    route = ''
    while not routing.IsEnd(node):
        route += 'city ' + str(node + 1) + ' -> '
        rount_list.append(node)
        node = assignment.Value(routing.NextVar(node))
    route += 'city 1'
    print(route)
else:
    print('No solution found.')

# Question 2d for 2b

x1 = []
y1 = []

for i in route_list:
    x1.append(lons[i])
    y1.append(lats[i])

plt.plot(x1, y1, "b--", linewidth=1)
plt.show()

# Question 2c
# http://examples.gurobi.com/traveling-salesman-problem/
from gurobipy import *

# Callback - use lazy constraints to eliminate sub-tours

def subtourelim(model, where):
  if where == GRB.callback.MIPSOL:
    selected = []
    # make a list of edges selected in the solution
    for i in range(n):
      sol = model.cbGetSolution([model._vars[i,j] for j in range(n)])
      selected += [(i,j) for j in range(n) if sol[j] > 0.5]
    # find the shortest cycle in the selected edge list
    tour = subtour(selected)
    if len(tour) < n:
      # add a subtour elimination constraint
      expr = 0
      for i in range(len(tour)):
        for j in range(i+1, len(tour)):
          expr += model._vars[tour[i], tour[j]]
      model.cbLazy(expr <= len(tour)-1)


# Given a list of edges, finds the shortest subtour

def subtour(edges):
  visited = [False]*n
  cycles = []
  lengths = []
  selected = [[] for i in range(n)]
  for x,y in edges:
    selected[x].append(y)
  while True:
    current = visited.index(False)
    thiscycle = [current]
    while True:
      visited[current] = True
      neighbors = [x for x in selected[current] if not visited[x]]
      if len(neighbors) == 0:
        break
      current = neighbors[0]
      thiscycle.append(current)
    cycles.append(thiscycle)
    lengths.append(len(thiscycle))
    if sum(lengths) == n:
      break
  return cycles[lengths.index(min(lengths))]

n = 38

m = Model()

# Create variables

vars = {}
for i in range(n):
   for j in range(i+1):
     vars[i,j] = m.addVar(obj= dist_matrix[i][j], vtype=GRB.BINARY,
                          name='e'+str(i)+'_'+str(j))
     vars[j,i] = vars[i,j]
   m.update()

# Add degree-2 constraint, and forbid loops

for i in range(n):
  m.addConstr(quicksum(vars[i,j] for j in range(n)) == 2)
  vars[i,i].ub = 0

m.update()

# Optimize model

m._vars = vars
m.params.LazyConstraints = 1
m.optimize(subtourelim)

solution = m.getAttr('x', vars)
selected = [(i,j) for i in range(n) for j in range(n) if solution[i,j] > 0.5]
assert len(subtour(selected)) == n

new_route_list = subtour(selected)
new_route_list.append(0)

new_route = ""
for i in new_route_list:
    new_route = new_route + "city" + str(i + 1) + ' -> '
   
print(new_route[:-4])

# Question 2d for 2b
x2 = []
y2 = []

for i in new_route_list:
    x2.append(lons[i])
    y2.append(lats[i])

plt.plot(x2, y2, "b--", linewidth=1)
plt.show()
