# -*- coding: utf-8 -*-
import json
import random
import codecs
import pickle

# network = json.load(open('./network_dict_0804_one_hop_right_weight.json', encoding='utf-8', errors='ignore'))

network = json.load(open('./relationship/results/network_dict_chenenehong_2016_2017.json', encoding='utf-8', errors='ignore'))


def ICmodel(net, seeds, times):
    fr = open('./relationship/inter_res/ICres_3.txt', 'w', encoding='utf-8', errors='ignore')
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


def draw_trees(docsource, docdes):

    edge_count = {}

    result_set = set()
    # result_set.add('2136372366')

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
            result_set.add(edge.split('->')[1].strip().strip('"'))

    fr.write('}')
    fr.close()
    fn = './relationship/inter_res/result_set16_17.pkl'
    pickle.dump(result_set, open(fn, 'wb'))

    # with open(fn, 'w') as f:  # open file with write-mode

        # f.write(picklestring)# serialize and save object
    # pickle.dump(result_set,'./relationship/inter_res/result_set06.pkl')

roots = pickle.load(open('./relationship/inter_res/result_set11_15.pkl','rb'))


ICmodel(network, roots, 10000)
# root = set()
# root.add('2136372366')
# ICmodel(network,root, 10000)
draw_trees('./relationship/inter_res/ICres_3.txt', './relationship/inter_res/chenenhong_2016_2017.dot')
