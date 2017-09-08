# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 17:09:28 2018

@author: wangbl
Purpose:
draw the net with networkX

"""

import networkx as nx
import operator
import matplotlib.pyplot as plt
import json
# create a graph, filling it with one of the edgelists


def add_networks(dic1, key_a, key_b, val):
    if key_a in dic1:
        dic1[key_a].update({key_b: val})
    else:
        dic1.update({key_a: {key_b: val}})

names = json.load(open('./inter_res/name_per_author.json'))
d = json.load(open('./relationship/results/network_dict_chenenehong_2006_2010.json'))
d1 = {}


for author1 in d:
    for author2 in d[author1]:
        add_networks(d1,author1,author2,{'weight':d[author1][author2]})#{'weight': d[author1][author2]}
        # d1[i][j] = {}
        # d1[i][j]['weight'] = d[i][j]

g2=nx.DiGraph(d1)


# # try to make the graph more understandable
# # (1) remove nodes that only have one connection, to shrink size of drawing
# # g2 = g.copy()
# d2 = nx.degree(g2)
# for n in g2.nodes():
#     if d2[n] <= 1:
#         g2.remove_node(n)
#
# # print out the smaller size (it's about half as big now in terms of nodes)
# g2numNodes = nx.number_of_nodes(g2)
# g2numEdges = nx.number_of_edges(g2)
# print('g2numNodes:', g2numNodes)
# print('g2numEdges:', g2numEdges)

# get degrees for the new g2 (with the pendants removed)
d3 = nx.degree(g2)

# (2) add some parameters to the draw() function
# --scale the size of the node to its degree (high-degree nodes will be bigger)
nx.draw(g2, with_labels=True,nodelist=d3.keys(), node_size=[v * 10 for v in d3.values()])
plt.show()
plt.savefig('./relationship/results/network_dict_chenenhong_2006_2010.png')