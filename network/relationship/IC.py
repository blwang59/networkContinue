# -*- coding: utf-8 -*-
import json
import random
import codecs
import pickle
import os
import networkx as nx

def ICmodel(net, seeds, times):
    fr = open('./inter_res/ICres.txt', 'w', encoding='utf-8', errors='ignore')
    for i in range(times):
        target = []
        active = []
        for seed in seeds:

            target.append(seed)
            active.append(seed)

        while(target):

            node = target.pop()
            if node in net:
                for follower in net[node]:
                    if follower not in active:
                        if random.random() <= net[node][follower]:
                            target.append(follower)
                            active.append(node)
                            fr.write(node + '->' + follower + '\n')

        fr.write('\n')

    fr.close()


def draw_trees(docdes,author,time1,time2):
    G=nx.DiGraph()
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

    fr = open(docdes, 'w', encoding='utf-8')
    fr.write('strict digraph G{\n')
    names = json.load(open('../inter_res/name_per_author.json', encoding='utf-8', errors='ignore'))
    for edge in edge_count:
        if edge_count[edge] >= 10:
            fr.write('"' + names[edge.split('->')[0].strip().strip('"')] +
                     '" -> "' + names[edge.split('->')[1].strip().strip('"')] + '"' + '\n')


            result_set.add(edge.split('->')[1].strip().strip('"'))

    fr.write('}')
    fr.close()
    fn = './inter_res/result_set_'+author+'_'+str(int(time1))+'_'+str(int(time2))+'.pkl'
    pickle.dump(result_set, open(fn, 'wb'))

    # with open(fn, 'w') as f:  # open file with write-mode

        # f.write(picklestring)# serialize and save object
    # pickle.dump(result_set,'/inter_res/result_set06.pkl')

#
# def draw_final(author, load_time, result_time):
#
#
#     roots = pickle.load(open('/inter_res/result_set'+author+'_'+load_time+'.pkl','rb'))
#
#
#     ICmodel(network, roots, 10000)
#     # root = set()
#     # root.add('2136372366')
#     # ICmodel(network,root, 10000)
#     draw_trees('/inter_res/ICres_'+author+'.txt', '/inter_res/'+author+'_'+result_time+'.dot')

def draw_final(net, roots, author, time1,time2 , shift):
    '''

    :param net: the network which the influence model based on
    :param roots: source nodes(in set)
    :param author: author number of the seed node
    :param time1: from year time1
    :param time2: to year time2
    :return: none
    '''

    ICmodel(net, roots, 10000)

    names = json.load(open('../inter_res/name_per_author.json', encoding='utf-8', errors='ignore'))
    if(os.path.exists(('./results/include_seeds/shift'+str(shift)))):
        pass
    else:
        os.mkdir('./results/include_seeds/shift'+str(shift))
    draw_trees('./results/include_seeds/shift'+str(shift)+'/'+names[author]+'_'+str(int(time1))+'_'+str(int(time2))+'.dot',author,time1,time2)