# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 18:32:04 2017

@author: Anna
"""

from pandas import Series, DataFrame
import pandas as pd
import networkx as nx
import numpy as np
import scipy as sp
import sys
import matplotlib.pyplot as plt

# Assigns spreadsheet filename and Loads spreadsheet
interactions = r'C:\Users\Anka\Documents\Network Analytics\HW2_who_talks_to_whom.xlsx'
dfInteractions = pd.ExcelFile(interactions)

# Loads both sheets from excel file into DataFrames, replaces NA's nd '-' with 0, drops the first column
dfSent = dfInteractions.parse(dfInteractions.sheet_names[0]).fillna(0).replace(['-'], [0]).drop('Nodes', 1)
dfReceived = dfInteractions.parse(dfInteractions.sheet_names[1]).fillna(0).replace(['-'], [0]).drop('Nodes', 1)

#-------------------------------PART 1 FOR dfSent only-------------------------
#creates edge list for dfSent(node1, node2, weight)
dfLinks = dfSent.stack().reset_index()
dfLinks.iloc[:, 0] = dfLinks.iloc[:, 0] + 1
dfLinks.columns = ['source', 'target','weight']

# keeps only links with nonzero values
# person 16 didn't fill up the spredsheets, maybe it's the Norwegian guy? 
#Some people claim to speak with him though, but with 16, the graph is a mess
dfLinksNonzero = dfLinks.loc[ (dfLinks['weight'] != 0) & (dfLinks['source'] != 16) & (dfLinks['target'] != 16)]

# builds a graph
G0 = nx.DiGraph()
G0 = nx.from_pandas_dataframe(dfLinksNonzero, source = 'source', target = 'target', edge_attr=True, create_using=nx.DiGraph())

nodesDegree = dict(nx.degree(G0))
maximum = max(nodesDegree, key=nodesDegree.get)
minimum = min(nodesDegree, key=nodesDegree.get)
#print(maximum, nodesDegree[maximum])
nodelist = nodesDegree.keys()
nodeSize = [v * 50 for v in nodesDegree.values()]

plt.figure(figsize=(15,15))
nx.draw(G0, nodelist = nodelist, node_size = nodeSize, with_labels=True, node_color='orange', edge_color='green')
plt.show(1)

nodesInDegree = dict(G0.in_degree())
nodesOutDegree = dict(G0.out_degree())
#absurd: person number 6 claims to interact only with 5 people whereas 31 people claim to interact with this person


#----------------------------PART 2 FOR dfReceive only-------------------------
#creates edge list (node1, node2, weight)
dfLinksR = dfReceived.stack().reset_index()
dfLinksR.iloc[:, 0] = dfLinksR.iloc[:, 0] + 1
dfLinksR.columns = ['source', 'target','weight']

# keeps only links with nonzero values
# person 48 removed because it forgot to fill its row in 'Receive' sheet ...
dfLinksNonzeroR = dfLinksR.loc[ (dfLinksR['weight'] != 0) & (dfLinksR['source'] != 16) & (dfLinksR['target'] != 16) & (dfLinksR['source'] != 48) & (dfLinksR['target'] != 48)]

# builds a graph
G1 = nx.DiGraph()
G1 = nx.from_pandas_dataframe(dfLinksNonzeroR, source = 'source', target = 'target', edge_attr=True, create_using=nx.DiGraph())

nodesDegreeR = dict(nx.degree(G1))
maximum = max(nodesDegreeR, key=nodesDegreeR.get)
minimum = min(nodesDegreeR, key=nodesDegreeR.get)
#print(maximum, nodesDegree[maximum])
nodelistR = nodesDegreeR.keys()
nodeSizeR = [v * 50 for v in nodesDegreeR.values()]

plt.figure(figsize=(15,15))
nx.draw(G1, nodelist = nodelistR, node_size = nodeSizeR, with_labels=True, node_color='orange', edge_color='green')
plt.show(2)


#----------------------PART 3 measures of centrality for both Sent and Receive-------------------------
#not finished, needs interpretation and more insight
nodesInDegreeR = dict(G1.in_degree())
nodesOutDegreeR = dict(G1.out_degree())
#nodesInDegreeR should be the same as nodesOutDegree (sent). they are not


inDegreeCent = nx.in_degree_centrality(G0)
outDegreeCent = nx.out_degree_centrality(G0)
inDegreeCentR = nx.in_degree_centrality(G1)
outDegreeCentR = nx.out_degree_centrality(G1)

bc = nx.betweenness_centrality(G0, k=None, normalized=True, weight='weight', endpoints=False, seed=None)
eig = nx.eigenvector_centrality(G0, max_iter=100, tol=1e-06, nstart=None, weight='weight')
#print(['%s %0.4f'%(node,eig[node]) for node in eig])

#below does not converage
#kc = nx.katz_centrality(G0, alpha=0.1, beta=1.0, max_iter=10000, tol=1e-05, nstart=None, normalized=True, weight='weight')


