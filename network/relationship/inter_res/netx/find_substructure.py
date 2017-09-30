# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25th 18:29:00 2017

@author: wangbl
Purpose: find the different substructure in the graph

"""

import pickle
import networkx as nx

def printres(author_name):

    graph = pickle.load(open(author_name+'.pkl','rb'))

    # print(graph)
    print(author_name+'\n')

    print(nx.triadic_census(graph))
printres('hanjiawei')

#    tg = {name: abc_graph() for name in TRIAD_NAMES}
#     tg['012'].add_edges_from([('a', 'b')])
#     tg['102'].add_edges_from([('a', 'b'), ('b', 'a')])
#     tg['102'].add_edges_from([('a', 'b'), ('b', 'a')])
#     tg['021D'].add_edges_from([('b', 'a'), ('b', 'c')])
#     tg['021U'].add_edges_from([('a', 'b'), ('c', 'b')])
#     tg['021C'].add_edges_from([('a', 'b'), ('b', 'c')])
#     tg['111D'].add_edges_from([('a', 'c'), ('c', 'a'), ('b', 'c')])
#     tg['111U'].add_edges_from([('a', 'c'), ('c', 'a'), ('c', 'b')])
#     tg['030T'].add_edges_from([('a', 'b'), ('c', 'b'), ('a', 'c')])
#     tg['030C'].add_edges_from([('b', 'a'), ('c', 'b'), ('a', 'c')])
#     tg['201'].add_edges_from([('a', 'b'), ('b', 'a'), ('a', 'c'), ('c', 'a')])
#     tg['120D'].add_edges_from([('b', 'c'), ('b', 'a'), ('a', 'c'), ('c', 'a')])
#     tg['120C'].add_edges_from([('a', 'b'), ('b', 'c'), ('a', 'c'), ('c', 'a')])
#     tg['120U'].add_edges_from([('a', 'b'), ('c', 'b'), ('a', 'c'), ('c', 'a')])
#     tg['210'].add_edges_from([('a', 'b'), ('b', 'c'), ('c', 'b'), ('a', 'c'),
#                               ('c', 'a')])
#     tg['300'].add_edges_from([('a', 'b'), ('b', 'a'), ('b', 'c'), ('c', 'b'),
#                               ('a', 'c'), ('c', 'a')])


# census['003'] = ((n * (n - 1) * (n - 2)) // 6) - sum(census.values())


