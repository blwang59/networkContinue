# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15th 14:33:00 2017

@author: wangbl
Purpose: construct the network with an attribute named year.

"""
import codecs
import csv
import json
import networkx as nx
import pickle



def add_networks(dic1, key_a, key_b, val):
    if key_a in dic1:
        dic1[key_a].update({key_b: val})
    else:
        dic1.update({key_a: {key_b: val}})


network = {}
ppa = {}
first_time = json.load(open('../first_time_0809_first_site_first_time_with_cheneh.json'))
union_ab = {}

G=nx.DiGraph()



with codecs.open('../data/data.csv', 'r', encoding='utf-8', errors='ignore') as f:
   f_csv = csv.reader(f)
   for row in f_csv:
       authors = row[2].split(',')
       time = float(row[4].split('-')[0])


       for a in authors:
           if a not in ppa:
               ppa[a] = set(row[0].split())
           else:
               ppa[a].add(row[0])


       if len(authors) > 1:
           for author1 in authors[1:]:
               author2 = authors[0]
               if author1 in ppa and author2 in ppa and author1 in first_time and author2 in first_time:
                   for paper in (ppa[author1] | ppa[author2]):
                       if paper in ppa[author2]:
                           weight = float(2017.0-time+1)/(2017.0-first_time[author2]+1)
                       else:
                           weight = float(2017.0 - time + 1) / (2017.0 - first_time[author1] + 1)
                       if author1 not in union_ab or author2 not in union_ab[author1]:
                           add_networks(union_ab, author1, author2, [weight])

                       else:
                           union_ab[author1][author2].append(weight)




               if author1 in first_time and author2 in first_time and first_time[author1] <= first_time[author2]:
                   if author1 not in network or author2 not in network[author1]:
                       add_networks(network, author1, author2, [float(2017.0-time+1)/(2017.0-first_time[author2]+1)])
                       G.add_edge(author1, author2, year=time)
                   else:
                       weight = float(2017.0-time+1)/(2017.0-first_time[author2]+1)
                       network[author1][author2].append(weight)
                       if time < G[author1][author2]['year']:
                           G[author1][author2]['year'] = time


for author1 in network:
   for author2 in network[author1]:
       network[author1][author2] = sum(network[author1][author2])/sum(union_ab[author1][author2])
       G[author1][author2]['weight'] = network[author1][author2]



fn = './inter_res/nx.pkl'
pickle.dump(G, open(fn, 'wb'))
# fr = open('./network_dict_0809_first_site_first_time_with_cheneh.json', 'w', encoding='utf-8', errors='ignore')
# json.dump(network, fr, ensure_ascii='false')



