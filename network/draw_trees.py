import json
import codecs


def draw_trees(docsource, docdes):
    names = json.load(open('./inter_res/name_per_author.json'))
    edge_count = {}
    net = json.load(open(docsource))
    fr = open(docdes, 'w', encoding='utf-8')
    fr.write('strict digraph G{\n')
    for a1 in net:
        for a2 in net[a1]:
            if a2 == '2110384818' or a1 == '2110384818':
                fr.write('"' + names[a1] +'" -> "' + names[a2] + '"' + '[label = '+str(round((net[a1][a2]), 2))+']'+'\n')

    fr.write('}')
    fr.close()
    # with codecs.open(docsource, 'r', encoding='utf-8', errors='ignore') as f:
    #     for line in f:
    #         l = line.rstrip().split('->', 1)
    #         if len(l) > 1:
    #             if '"' + l[0] + '" -> "' + l[1] + '"' not in edge_count:
    #                 edge_count['"' + l[0] + '" -> "' + l[1] + '"'] = 1
    #             else:
    #                 edge_count['"' + l[0] + '" -> "' + l[1] + '"'] += 1
    #
    #
    # names = json.load(open('./inter_res/name_per_author.json', encoding='utf-8', errors='ignore'))
    # for edge in edge_count:
    #     if edge_count[edge] >= 2:
    #         fr.write('"' + names[edge.split('->')[0].strip().strip('"')] +
    #                  '" -> "' + names[edge.split('->')[1].strip().strip('"')] + '"' + '\n')
draw_trees('./network_dict_0807_right_weight.json', './test_0807.dot')