# -*- coding: utf-8 -*-
import json
import random
import codecs


network = json.load(open('./network_dict_0808_improved_weight.json', encoding='utf-8', errors='ignore'))


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
        # if edge_count[edge]>100:
        #     print(edge_count[edge])
        if edge_count[edge] >= 10:
            fr.write('"' + names[edge.split('->')[0].strip().strip('"')] +
                     '" -> "' + names[edge.split('->')[1].strip().strip('"')] + '"' + '\n')

        # if edge_count[edge] >= 20:
        #     fr.write('"' + edge.split('->')[0].strip().strip('"') +
        #              '" -> "' + edge.split('->')[1].strip().strip('"') + '"' + '\n')

    fr.write('}')
    fr.close()

ICmodel(network, "2153710278", 10000)

draw_trees('./inter_res/ICres_2153710278.txt', './inter_res/IC0808/xionghui_10.dot')
