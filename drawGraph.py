# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 15:47:59 2020

@author: nlama
"""

# -*- coding: utf-8 -*-
"""
Created on Monday Oct 08 14:18:00 2019

@author: nlama
"""
##Import Dependencies
#import igraph as ig
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random, os


####################
##Classes
####################



class DrawGraph:
    
    def __init__(self, G, nodeColor='#A0CBE2'):
                 
        self.graph = G
        self.nodeColor = nodeColor
        self.plot()
        self.GraphStats = GraphStatistics
    
    def plot(self):       
        pos=nx.spring_layout(self.graph)     
        f = plt.figure(random.randint(0,40),[30,40])
        ax = f.add_subplot(1,1,1)
        
            
        nx.draw_networkx(self.graph, pos, node_color=self.nodeColor, node_size=100, 
                width=2, edge_color="k", with_labels=True, cmap=plt.cm.Reds,
                font_size=20, font_family='sans-serif', ax=ax)

    def draw(G, pos, m, rnaName):
        measures = m[0]
        measure_name = m[1]
        
        f = plt.figure(random.randint(0,2000),[50,70])
        backgroundColor = 'white'
        plt.rcParams['figure.facecolor'] = backgroundColor
        plt.rcParams['savefig.facecolor']= backgroundColor
        plt.rcParams['ytick.color'] = 'black'
        plt.rcParams['ytick.labelsize'] = 50
        
        nodes = nx.draw_networkx_nodes(G, pos, node_size=1000, cmap=plt.cm.magma, 
                                       linewidths=5, alpha = 0.55,
                                       node_color=list(measures.values()),
                                       nodelist=list(measures.keys()))
        
        nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1))
        edges = G.edges()
        weights = [G[u][v]['weight'] for u,v in edges]
        
        nx.draw_networkx_labels(G,pos,font_size=20,font_color="k",font_weight="bold")
        nx.draw_networkx_edges(G, pos, width = weights,alpha = 0.55, edge_color="lightgray")
    
        plt.title('{0} : {1}'.format(rnaName, measure_name),color="k",fontsize=50)
        plt.colorbar(nodes)
        plt.axis('off')
        plt.show()
        return f
        
class GraphStatistics:
    
    def __init__(self, G):
        self.graph = G
        
    def bC(self):
        ''' 
        Measure nodes where they intercept most shortest paths
        This one seems to correspond most to end of helix
        '''
        return (nx.betweenness_centrality(self.graph), 'Betweenness Centrality')
    
    def eC(self):
        return (nx.eigenvector_centrality(self.graph), 'Eigenvector Centrality')
    
    def cC(self):
        return (nx.closeness_centrality(self.graph), 'Closeness Centrality')
    
    def hC(self):
        return (nx.harmonic_centrality(self.graph), 'Harmonic Centrality')
    
    def dC(self):
        '''
        Measure of degrees. Unpaired nucleotides will have a higher Deg. Cent.
        '''
        return ( nx.degree_centrality(self.graph), 'Degree Centrality' )

def getPercentileCutoffs(metricDict, low=15, high=80):
    
    normCent = {}
    l = list(metricDict.values())
    c = dict(metricDict)
    
    l_cutoff = np.percentile(l,low)
    h_cutoff = np.percentile(l,high)
    
    for item in c.items():
#        if item[1] < l_cutoff: #percentile cutoff
#            normCent[item[0]]=0
        if item[1] > h_cutoff:
            normCent[item[0]]=0.5
        else:
            normCent[item[0]]=item[1]
    
    return (normCent, 'Normalized Centrality')
            
            
def initialize(G, draw = False, getNorm=False):
    rnaName = "Subreddit User Network"
    GraphMet = GraphStatistics(G)
    metric = GraphMet.cC()
    norm_metric = getPercentileCutoffs(metric[0])
    if draw:
        DrawGraph.draw(G, nx.spectral_layout(G, scale= 2) , metric, rnaName) 
        DrawGraph.draw(G, nx.kamada_kawai_layout(G, scale= 2) , norm_metric, rnaName)       
    if getNorm == True:
        return norm_metric
    else:
        return metric
    
    
##############################################################################  
if __name__ == "__main__":
    m = initialize(G, True, True)
#    print(h)
#    f.savefig('D:/Weeks/PocketFinding/dataSetA/MachineLearning/NetworkGraphs/{0}.png'.format(rnaName),
#                facecolor=f.get_facecolor(), edgecolor='none')

