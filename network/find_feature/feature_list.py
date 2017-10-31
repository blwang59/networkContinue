# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25th 2017  14:38:00

@author: wangbl
Purpose: find some useful features in networks

"""
import pickle
import networkx as nx
network = pickle.load(open('../relationship/inter_res/netx/xionghui_onlyNum.pkl', 'rb'))

degree_centralities = nx.degree_centrality(network)
in_degree_centralities = nx.in_degree_centrality(network)
out_degree_centralities = nx.out_degree_centrality(network)

page_ranks = nx.pagerank(network,)


eigens = nx.eigenvector_centrality(network,)
katz = nx.katz_centrality(network,)

for node in network.nodes():
    network.indegree(node)