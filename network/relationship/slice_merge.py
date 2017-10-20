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
import matplotlib
from networkx.drawing.nx_pydot import write_dot
G=nx.DiGraph()

pattern = re.compile(r'^net_2153710278.*onlyNum\.pkl$')

for files in os.listdir('./inter_res/netx/'):

    if os.path.isfile('./inter_res/netx/'+files) and pattern.match(files):

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


# G.edge['year']=[int(x['year']) for x in G.edge['year']]
#
edge_labels = nx.get_edge_attributes(G,'year')
# print(edge_labels)

fn = './inter_res/netx/xionghui_onlyNum.pkl'
pickle.dump(G, open(fn, 'wb'))


nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels,font_size=10)
nx.draw(G,pos,with_labels=True,font_size = 10)
# nx.draw_networkx_nodes()
plt.savefig('./results/xionghui_onlyNum_shift2.png')
plt.show()


# pos = graphviz_layout(G, prog='dot')
# nx.draw(G, pos, with_labels=True, arrows=False)
#
# plt.savefig('./results/chenenhong_shift2.png', bbox_inches='tight')
# plt.show()
