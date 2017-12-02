import pandas as pd
import gurobipy as grb
import networkx as nx
from geopy.distance import vincenty

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

#calculate great circle distance of each pair of the city
distance=list()
for i in range(38):
    for j in range(38):
        distance.append((vincenty(data.loc[i,'position'],data.loc[j,'position']).km))

chunks = [distance[x:x+38] for x in range(0, len(distance), 38)]

#turn into a distance matrix
cities = []
for i in range(1, len(data)+1):
    cities.append('city ' + str(i))
distances = pd.DataFrame(chunks, columns=cities, index=cities)

#Question a

#Create X,Y coordinates of each node
xypos = {}
for i in range(len(data)):
    xypos['city ' + str(data['city'][i])] = ( data['longitude'][i] , data['latitude'][i])

G = nx.from_pandas_adjacency(distances)
nx.draw_networkx_nodes(G, pos = xypos)
nx.draw_networkx_labels(G, pos = xypos)


#Question c
#Definining several functions to use later in a while loop
def saveresult(draw=True):
    """
    To be used after optimizing a Gurobi model.
    Saves the result of a Gurobi Optimizer solution as a Graph, returning NetworkX Graph Object.
    Use draw=True argument to draw the graph.
    """

    vals = m.getAttr('x', vars)
    res=[]
    for i,j in vals.items():
        if j>0:
            res.append(i)
    FG = nx.Graph()
    FG.add_nodes_from(G)
    FG.add_edges_from(res)
    if draw == True:
        nx.draw_networkx(FG, pos=xypos)
    return (FG)

def findsubtour(currentGraph, startnode):
    """
    From a NetworkX Graph, uses BFS to find all nodes linked to a starting node.
    Returns a set that has all nodes which are in the same subtour as the starting node. 
    """
    mainsubtour = set()
    for k,v in dict(nx.bfs_successors(currentGraph, startnode)).items():
        if k not in mainsubtour:
            mainsubtour.add(k)
        for i in v:
            if i not in mainsubtour:
                mainsubtour.add(i)
    return (mainsubtour)

def addcuttomodel(fullgraph, subtourset, Model):
    """
    Identifies the cut (list of edges) that creates the subtour in subtourset.
    Adds a constraint to a Gurobi model specifying that the sum of this subtour >= 2. 
    """
    #Define the cut separating this subtour
    cut = []
    for i,j in fullgraph.edges():
        if i in subtourset and j not in subtourset:
            cut.append((i,j))
        elif j in subtourset and i not in subtourset:
            cut.append((j,i))
    
    #Add cut constraint
    varsx = Model.addVars(cut)
    for i,j in varsx.keys():
        varsx[i,j] = vars[i,j]
    Model.addConstr(varsx.sum() >= 2)
    

#Generate Gurobi model
m = grb.Model()

#Create variables - edges
edgedict = dict(nx.get_edge_attributes(G, 'weight'))
vars = m.addVars(edgedict.keys(), obj=edgedict, vtype=grb.GRB.BINARY, name='edge')
for i,j in vars.keys():
    vars[j,i] = vars[i,j] # edge in opposite direction is equal and referred to edge

#Add initial constraints: Degree of each node = 2
m.addConstrs(vars.sum(i,'*') == 2 for i in G.nodes())

#First Iteration:
m.optimize()
FG = saveresult(draw=True)
tour = findsubtour(FG, 'city 1')

n=1

#Can run each iteration separately to see how the graph changes with each added cut constraint
while len(tour) != len(G.nodes()):
    addcuttomodel(G, tour, m)
    m.optimize()
    n+=1
    FG = saveresult(draw=False)
    tour = findsubtour(FG, 'city 1')
FG=saveresult(draw=True)
