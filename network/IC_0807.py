# -*- coding: utf-8 -*-
import json
import random
import codecs





def ICmodel(net, seeds, times):
    fr = open('./inter_res/ICres_' + seeds + '.txt', 'w', encoding='utf-8', errors='ignore')
    for i in range(times):
        # target = set()
        active = set()
        target1 = set()

        # target.add(seeds)
        target1.add(seeds)
        active.add(seeds)

        while target1:
            target = set()
            for node in target1:
                if node in net:
                    for follower in net[node]:
                        if follower not in active:
                            if random.random() <= net[node][follower]:
                                target.add(follower)
                                active.add(follower)
                                # active = active | target
                                fr.write(node + '->' + follower + '\n')


            # print(str(active))
            target1 = target


        fr.write('\n')

    fr.close()


def draw_trees(docsource, docdes, network):

    edge_count = {}
    net = network
    with codecs.open(docsource, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            l = line.rstrip().split('->', 1)
            if len(l) > 1:
                if '"' + l[0] + '" -> "' + l[1] + '"' not in edge_count:
                    edge_count['"' + l[0] + '" -> "' + l[1] + '"'] = 1
                else:
                    edge_count['"' + l[0] + '" -> "' + l[1] + '"'] += 1

    fr = open(docdes, 'w', encoding='utf-8')
    fr.write('strict digraph G{\n')
    names = json.load(open('./inter_res/name_per_author.json', encoding='utf-8', errors='ignore'))
    for edge in edge_count:
        # if edge_count[edge]>100:
        #     print(edge_count[edge])
        if edge_count[edge] >= 10:
            fr.write('"' + names[edge.split('->')[0].strip().strip('"')] +
                     '" -> "' + names[edge.split('->')[1].strip().strip('"')] + '"' + '[label = '+str(round((net[edge.split('->')[0].strip().strip('"')][edge.split('->')[1].strip().strip('"')]), 2))+']'+ '\n')

        # if edge_count[edge] >= 20:
        #     fr.write('"' + edge.split('->')[0].strip().strip('"') +
        #              '" -> "' + edge.split('->')[1].strip().strip('"') + '"' + '\n')

    fr.write('}')
    fr.close()

def draw_final(author):
    # network = json.load(open('./network_dict_0809_first_site_first_time_with_cheneh.json', encoding='utf-8', errors='ignore'))
    network = json.load(
        open('./topic_model/network_del_others_avg_' + str(author) + '.json', encoding='utf-8',
             errors='ignore'))
    ICmodel(network, author, 10000)
    names = json.load(open('./inter_res/name_per_author.json', encoding='utf-8', errors='ignore'))
    # draw_trees('./inter_res/ICres_'+str(author)+'.txt', './inter_res/IC0815/'+names[str(author)]+'_0001.dot', network)

    draw_trees('./inter_res/ICres_' + str(author) + '.txt', './inter_res/IC0815/' + names[str(author)] + '_0001_topic_avg_20.dot',
               network)



draw_final('2136372366')#Enhong Chen
draw_final('2153710278')# Hui Xiong
draw_final('2126330539')# Jian Pei
draw_final('2121939561')#Jiawei Han
