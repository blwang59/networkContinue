# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15th 14:33:00 2017

@author: wangbl
Purpose: save the cooperate time when diffusion

"""
import json
import random
import codecs
import pickle
import os
import networkx as nx
network = pickle.load(open('./inter_res/nx.pkl', 'rb'))

def ICmodel(net, seeds, times, year1,year2):
    fr = open('./inter_res/ICres.txt', 'w', encoding='utf-8', errors='ignore')
    for i in range(times):
        target = []
        active = []
        for seed in seeds:
            target.append(seed)
            active.append(seed)

        while (target):

            node = target.pop()
            if node in net:
                for follower in net[node]:
                    if follower not in active:
                        if random.random() <= net[node][follower]['weight'] and net[node][follower]['year'] < year2 and\
                            net[node][follower]['year'] >=  year1:
                            target.append(follower)
                            active.append(node)
                            fr.write(node + '->' + follower + '\n')

        fr.write('\n')

    fr.close()


def draw_trees(author,time1,time2):
    '''

    :param docdes: where to store the doc
    :param author:
    :return:
    '''
    G = nx.DiGraph()
    edge_count = {}
    result_set = set()
    with codecs.open('./inter_res/ICres.txt', 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            l = line.rstrip().split('->', 1)
            if len(l) > 1:
                if '"' + l[0] + '" -> "' + l[1] + '"' not in edge_count:
                    edge_count['"' + l[0] + '" -> "' + l[1] + '"'] = 1

                else:
                    edge_count['"' + l[0] + '" -> "' + l[1] + '"'] += 1

    # fr = open(docdes, 'w', encoding='utf-8')
    # fr.write('strict digraph G{\n')
    names = json.load(open('../inter_res/name_per_author.json', encoding='utf-8', errors='ignore'))
    for edge in edge_count:
        if edge_count[edge] >= 10:

            G.add_edge(names[edge.split('->')[0].strip().strip('"')],
                       names[edge.split('->')[1].strip().strip('"')],

                       year = network[edge.split('->')[0].strip().strip('"')][edge.split('->')[1].strip().strip('"')]['year'])


            result_set.add(edge.split('->')[1].strip().strip('"'))


    fn = './inter_res/netx/net_' + author + '_' + str(int(time1)) + '_' + str(int(time2)) + '.pkl'
    pickle.dump(G, open(fn, 'wb'))
    # fr.write('}')
    # fr.close()
    return result_set



def draw_final(net, author, step, shift):
    '''

    :param net: the network which the influence model based on
    :param roots: source nodes(in set)
    :param author: author number of the seed node
    :param time1: from year time1
    :param time2: to year time2
    :return: none
    '''
    first_time = json.load(open('../first_time_0809_first_site_first_time_with_cheneh.json'))
    time1 =first_time[author]
    roots = set()
    roots.add(author)
    ICmodel(net,roots,10000,time1,time1+step)
    for i in range(int((2017-time1-step)/shift)+1):
        roots = draw_trees(author,time1+ (i) * shift, time1 + (i)*shift + step)
        ICmodel(net,roots,10000,time1+ (i+1) * shift, time1 + (i+1)*shift + step)

draw_final(network,'2136372366',5,2)





