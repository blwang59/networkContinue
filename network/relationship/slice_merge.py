# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15th 14:33:00 2017

@author: wangbl
Purpose: merge the slices into a whole tree,and save the cooperate time when diffusion

"""
import pickle
import re
import os
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot
G=nx.DiGraph()

pattern = re.compile(r'.*pkl$')
for files in os.listdir('./inter_res/netx/'):

    if os.path.isfile('./inter_res/netx/'+files) and pattern.match('./inter_res/netx/'+files):
        graph = pickle.load(open('./inter_res/netx/'+files, 'rb'))
        G=nx.compose(G,graph)
# pos = nx.spectral_layout(G)
# pos = nx.circular_layout(G)
# pos =nx.random_layout(G)
# pos = nx.shell_layout(G)
# pos = nx.fruchterman_reingold_layout(G,center='Enhong Chen')
# pos = nx.spring_layout(G, scale=2)
from networkx.drawing.nx_agraph import graphviz_layout
pos = graphviz_layout(G,prog= 'dot')
edge_labels = nx.get_edge_attributes(G,'year')



nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)
nx.draw(G,pos,with_labels=True)
# nx.draw_networkx_nodes()
plt.savefig('./results/chenenhong_shift2.png')
plt.show()
# pos = graphviz_layout(G, prog='dot')
# nx.draw(G, pos, with_labels=True, arrows=False)
#
# plt.savefig('./results/chenenhong_shift2.png', bbox_inches='tight')
# plt.show()
