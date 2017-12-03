# -*- coding: utf-8 -*-
"""
Last version created on Sun Dec  3 14:39:35 2017

@author: Group I
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# assigns spreadsheet filename and Loads spreadsheet
# loads both sheets from excel file into DataFrames, replaces NA's nd '-' with 0
# drops the first column
interactions = r'C:\Users\Anka\Documents\Network Analytics\HW2_who_talks_to_whom.xlsx'
dfInteractions = pd.ExcelFile(interactions)
dfSent = dfInteractions.parse(dfInteractions.sheet_names[0]).fillna(0).replace(['-'], [0]).drop('Nodes', 1)
dfReceived = dfInteractions.parse(dfInteractions.sheet_names[1]).fillna(0).replace(['-'], [0]).drop('Nodes', 1)
dfSent.index = dfSent.columns
dfReceived.index = dfReceived.columns

dfReceived = dfReceived.transpose()
dfReceived.columns = dfReceived.index
dfSent.columns = dfReceived.index
dfSent.index = dfReceived.index

dfAverage = (dfReceived.add(dfSent, fill_value=0))/2
            
a = dfAverage.as_matrix()
G = nx.DiGraph(a)
            
dist = nx.get_edge_attributes(G, 'weight')
for k,v in dist.items():
    dist[k] = 1/v
nx.set_edge_attributes(G, dist, 'distance')

centralitydfAvg = pd.DataFrame()
centralitydfAvg['indeg'] = (dict(G.in_degree(weight=None))).values()
centralitydfAvg['outdeg'] = (dict(G.out_degree(weight = None))).values()
centralitydfAvg['degdiff'] = centralitydfAvg['indeg'].sub(centralitydfAvg['outdeg'])
centralitydfAvg['indeg_centr']=(nx.in_degree_centrality(G)).values()
centralitydfAvg['outdeg_centr']=(nx.out_degree_centrality(G)).values()
centralitydfAvg['eigen_centr']=(nx.eigenvector_centrality(G, max_iter=500)).values()
centralitydfAvg['closeness_centr'] = (nx.closeness_centrality(G, distance = 'distance')).values() #represents the closeness FROM this node
centralitydfAvg['closeness_centr_rev'] = (nx.closeness_centrality(G.reverse(), distance = 'distance')).values() #represents closeness TO this node
centralitydfAvg['between_centr'] = (nx.betweenness_centrality(G, normalized = False, weight = 'distance')).values()

plt.figure(figsize=(15,15))
nodesDegree = dict(nx.degree(G))
nodelist = nodesDegree.keys()
nodeSize = [v * 15 for v in nodesDegree.values()]
G = nx.convert_node_labels_to_integers(G, first_label=1) # changes labeling of nodes from 1-81 instead 0-80
nx.draw(G, with_labels=True, node_size = nodeSize, node_color='red', edge_color='green')
