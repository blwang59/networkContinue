# -*- coding: utf-8 -*-
import json
import random
import codecs


network = json.load(open('./network_dict_0804_one_hop_right_weight.json', encoding='utf-8', errors='ignore'))


def ICmodel(net, seeds, times):
    fr = open('./inter_res/ICres_' + seeds + '.txt', 'w', encoding='utf-8', errors='ignore')
    for i in range(times):
        target = []
        active = []

        target.append(seeds)
        active.append(seeds)

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


def draw_trees(docsource, docdes):

    edge_count = {}

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
        if edge_count[edge] >= 10:
            fr.write('"' + names[edge.split('->')[0].strip().strip('"')] +
                     '" -> "' + names[edge.split('->')[1].strip().strip('"')] + '"' + '\n')

    fr.write('}')
    fr.close()

ICmodel(network, "2136372366", 100)

draw_trees('./inter_res/ICres_2136372366.txt', './inter_res/chenenhong_10_one_hop_right_weight.dot')
