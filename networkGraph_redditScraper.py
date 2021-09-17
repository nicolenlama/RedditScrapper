# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:17:14 2020

@author: nlama
"""

import networkx as nx
import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl
from string import ascii_lowercase
import drawGraph


#os.chdir("")

with open("reddit_users_subreddits_edgelist.pickle",'rb') as file:
    edgeList = pickle.load(file)
    
G = nx.Graph()
G.add_weighted_edges_from(edgeList)
pos = nx.spring_layout(G, k=5, iterations=200)


path = "Reddit_NSFW_Quarantined.graphml"
nx.write_graphml(G, path)

#edges = G.edges()
#weights = [G[u][v]['weight'] for u,v in edges]
#
#
#    
#plt.subplot(121)
#colors = range(100)
#nx.draw(G, pos, node_color=range(121), node_size=800, alpha=0.75, 
#        width=weights, with_labels=True)
#
#
#
#
#nx.draw_networkx_labels(G, pos, font_size=20)

drawGraph.initialize(G,True,True)

