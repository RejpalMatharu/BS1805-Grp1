# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 14:43:51 2017

@author: mingyang
"""

import pandas as pd
import networkx as nx

sent = pd.read_csv('D:\Work\MSc Business Analytics\\Network Analytics\Homework 2\HW2sent.csv', index_col='Nodes')
rec = pd.read_csv('D:\Work\MSc Business Analytics\\Network Analytics\Homework 2\HW2rec.csv', index_col='Nodes')

for col in rec:
    sent[col] = pd.to_numeric(sent[col], errors = 'coerce')
    rec[col] = pd.to_numeric(rec[col], errors = 'coerce')

sent = sent.fillna(0)
rec = rec.fillna(0)

averagedf = (rec.add(sent, fill_value=0))/2
averagedf.drop(['Unnamed: 82','Unnamed: 83','Unnamed: 84','Unnamed: 85','Unnamed: 86'], axis = 1, inplace=True)
averagedf.columns = averagedf.index

#Converts dataframe to numpy matrix first, because nx.from_pandas_adjacency has a bug:
#the 'create_using = nx.DiGraph()' argument does not work. See link:
#https://stackoverflow.com/questions/47561779/why-do-i-get-a-graph-when-i-specify-create-using-nx-digraph
b = averagedf.as_matrix()
DG = nx.DiGraph(b)

#Define distance from one person to another as the inverse of number of messages? Debatable
#This will be used for closeness centrality
dist = nx.get_edge_attributes(DG, 'weight')
for k,v in dist.items():
    dist[k] = 1/v
nx.set_edge_attributes(DG, dist, 'distance')

centralitydf = pd.DataFrame()
centralitydf['indeg'] = (dict(DG.in_degree(weight='weight'))).values()
centralitydf['outdeg'] = (dict(DG.out_degree(weight = 'weight'))).values()
centralitydf['degdiff'] = centralitydf['indeg'].sub(centralitydf['outdeg'])
centralitydf['indeg_centr']=(nx.in_degree_centrality(DG)).values()
centralitydf['outdeg_centr']=(nx.out_degree_centrality(DG)).values()
centralitydf['eigen_centr']=(nx.eigenvector_centrality(DG, max_iter=500)).values()
centralitydf['closeness_centr'] = (nx.closeness_centrality(DG, distance = 'distance')).values() #represents the closeness FROM this node
centralitydf['closeness_centr_rev'] = (nx.closeness_centrality(DG.reverse(), distance = 'distance')).values() #represents closeness TO this node
centralitydf['between_centr'] = (nx.betweenness_centrality(DG, normalized = False, weight = 'weight')).values()
