import json
import random
import codecs

network = json.load(open('./network_dict_0728_weight_time.json'))


def ICmodel(net, seeds, times):
    fr = open('./inter_res/ICres_' + seeds + '.txt', 'w', encoding='utf-8')
    for i in range(times):
        target = []
        active = []
    # for i in net:
    #   for j in net[i]:
    #neighbor_dict = net[seeds]
    #neighbor_q = neighbor_dict.keys()
    #fr = open('./ICres.txt', 'w', encoding='utf-8')
        target.append(seeds)
        active.append(seeds)
        # ltimes = 0
        while(target):
            # ltimes+=1
            node = target.pop()

            # active.append(node)
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
    # count = {}
    edge_count = {}
    # count the times which the nodes are activated
    # with codecs.open(docsource, 'r', encoding='utf-8', errors='ignore') as f:
    #     for line in f:
    #       l = line.rstrip().split('->',1)
    #       if(len(l)>1):
    #           if l[1] not in count:
    #               count[l[1]] = 1
    #           else:
    #               count[l[1]] += 1

    # count the times which the edges are activated
    with codecs.open(docsource, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            l = line.rstrip().split('->', 1)
            if(len(l) > 1):
                if '"' + l[0] + '" -> "' + l[1] + '"' not in edge_count:
                    edge_count['"' + l[0] + '" -> "' + l[1] + '"'] = 1
                else:
                    edge_count['"' + l[0] + '" -> "' + l[1] + '"'] += 1

    fr = open(docdes, 'w')
    fr.write('strict digraph G{\n')
    names = json.load(open('./inter_res/name_per_author.json'))
    for edge in edge_count:
        if edge_count[edge] >= 50:
            fr.write('"' + names[edge.split('->')[0].strip().strip('"')] +
                     '" -> "' + names[edge.split('->')[1].strip().strip('"')] +'"' + '\n')
            # fr.write(edge+'\n')

    # for i in count:
    #     if count[i]>=50:
    #         fr.write('"'+i+'"'+' [color = red]')
    fr.write('}')
    fr.close()

ICmodel(network, "2136372366", 100)
draw_trees('./inter_res/ICres_2136372366.txt',
           './inter_res/chenenhong_time_50.dot')
