
#!/usr/bin/env python
"""
Draw a graph with matplotlib.
You must have matplotlib for this to work.
"""
# try:
#     import matplotlib.pyplot as plt
#     import matplotlib.colors as colors
#     import matplotlib.cm as cmx
#     import numpy as np
# except:
#     raise
#
# import networkx as nx
#
# G=nx.path_graph(8)
# #Number of edges is 7
# values = range(7)
# # These values could be seen as dummy edge weights
#
# jet = cm = plt.get_cmap('jet')
# cNorm  = colors.Normalize(vmin=0, vmax=values[-1])
# scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
# colorList = []
#
# for i in range(7):
#   colorVal = scalarMap.to_rgba(values[i])
#   colorList.append(colorVal)
#
#
# nx.draw(G,edge_color=colorList)
# plt.savefig("simple_path.png") # save as png
# plt.show() # display


import matplotlib.pyplot as plt
import networkx as nx
import random

G = nx.gnp_random_graph(10,0.3)
for u,v,d in G.edges(data=True):
    d['weight'] = random.random()

edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())

pos = nx.spring_layout(G)
nx.draw(G, pos, node_color='b', edgelist=edges, edge_color=weights, width=10.0, edge_cmap=plt.cm.Blues)
# plt.savefig('edges.png')
plt.show()