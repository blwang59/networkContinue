# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17th  11:06:00 2017

@author: wangbl
Purpose: find some useful features in networks

"""
import json
import random
import codecs
import pickle
import os
import networkx as nx
from pycallgraph import PyCallGraph
from pycallgraph import Config
from pycallgraph.output import GraphvizOutput
network = pickle.load(open('chenenhong.pkl', 'rb'))

# degree_centralities = nx.degree_centrality(network)
# in_degree_centralities = nx.in_degree_centrality(network)
# out_degree_centralities = nx.out_degree_centrality(network)
#
# page_ranks = nx.pagerank(network)


for author in nx.nodes(network):
    

