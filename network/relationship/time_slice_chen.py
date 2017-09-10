# -*- coding: utf-8 -*-
"""
Created on Thu Sep 7th 10:27:37 2017

@author: wangbl
Purpose: time slice experiment on Enhong Chen, whose paper is from 2006.
slice into three parts:2006-2010,2011-2015,2016-2017


"""

import codecs
import csv
import json
import pickle
import IC

def add_networks(dic1, key_a, key_b, val):
    if key_a in dic1:
        dic1[key_a].update({key_b: val})
    else:
        dic1.update({key_a: {key_b: val}})

def network_construct(author,step,shift):
    '''

    :param author: number of author
    :param step: length of time slices
    :param overlap: how much overlap between slices 
    :return: none, generate final file './results/number_time1_time2.dot'
    '''
    # first_time = json.load(open('../first_time_0809_first_site_first_time_with_cheneh.json'))
    #
    # root= set()
    # root.add(author)
    # diffusion(root,author,first_time[author],first_time[author]+step)
    # network = json.load(open('./results/network_dict_' + author + '_' + str(int(first_time[author]) ) + '_' + str(int(first_time[author]+ step)) + '.json'))
    # IC.draw_final(network, root, author, first_time[author] , first_time[author] + step)
    #
    #
    # for i in range(int((2017-first_time[author])/step)):
    #     roots = pickle.load(open(
    #         './inter_res/result_set_' + author + '_' + str(int(first_time[author] + i * step)) + '_' +
    #         str(int(first_time[author] + (i + 1) * step)) + '.pkl', 'rb'))
    #     diffusion(roots,author,first_time[author]+(i+1)*step,first_time[author]+(i+2)*step)
    #     network = json.load(
    #         open('./results/network_dict_' + author + '_' + str(int(first_time[author] + (i + 1) * step)) + '_' + str(
    #             int(first_time[author] + (i + 2) * step)) + '.json', encoding='utf-8', errors='ignore'))
    #
    #     IC.draw_final(network, roots, author, first_time[author] + (i + 1) * step, first_time[author] + (i + 2) * step)


    first_time = json.load(open('../first_time_0809_first_site_first_time_with_cheneh.json'))
    ftime =first_time[author]

    root = set()
    root.add(author)
    diffusion(root, author, ftime, ftime + step)
    network = json.load(open('./inter_res/network_dict/network_dict_' + author + '_' + str(int(ftime))  + '_' + str(int(ftime + step)) + '.json'))
    IC.draw_final(network, root, author, ftime, ftime + step,shift)

    for i in range(int((2017-ftime-step)/shift)):
        roots = pickle.load(open(
            './inter_res/result_set_' + author + '_' + str(int(ftime + i*shift)) + '_' +str(int(ftime + i*shift + step)) + '.pkl', 'rb'))
        diffusion(roots, author, ftime + (i+1) * shift, ftime + (i+1)*shift + step)
        network = json.load(open(
            './inter_res/network_dict/network_dict_' + author + '_' + str(int( ftime + (i+1) * shift)) + '_' + str(int(ftime + (i+1)*shift + step)) + '.json', encoding='utf-8', errors='ignore'))

        IC.draw_final(network, roots, author,  ftime + (i+1) * shift, ftime + (i+1)*shift + step,shift)





def diffusion(roots,author,time1,time2):
    ppa = {}
    union_ab = {}
    network = {}
    first_time = json.load(open('../first_time_0809_first_site_first_time_with_cheneh.json'))
    with codecs.open('../data/data.csv', 'r', encoding='utf-8', errors='ignore') as f:
        f_csv = csv.reader(f)

        for row in f_csv:
            for root in roots:

                if root in row[2] and int(row[4].split('-')[0]) < time2 and int(row[4].split('-')[0]) >= time1:
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
                                            weight = float(2017.0 - time + 1) / (2017.0 - first_time[author2] + 1)
                                        else:
                                            weight = float(2017.0 - time + 1) / (2017.0 - first_time[author1] + 1)
                                        if author1 not in union_ab or author2 not in union_ab[author1]:
                                            add_networks(union_ab, author1, author2, [weight])
                                        else:
                                            union_ab[author1][author2].append(weight)

                                if author1 in first_time and author2 in first_time and first_time[author1] <= first_time[
                                    author2]:
                                    if author1 not in network or author2 not in network[author1]:
                                        add_networks(network, author1, author2,
                                                     [float(2017.0 - time + 1) / (2017.0 - first_time[author2] + 1)])
                                    else:
                                        weight = float(2017.0 - time + 1) / (2017.0 - first_time[author2] + 1)
                                        network[author1][author2].append(weight)


    for author1 in network:
        for author2 in network[author1]:
            network[author1][author2] = sum(network[author1][author2]) / sum(union_ab[author1][author2])

    fr = open('./inter_res/network_dict/network_dict_'+author+'_'+str(int(time1))+'_'+str(int(time2))+'.json', 'w', encoding='utf-8',
              errors='ignore')
    json.dump(network, fr, ensure_ascii='false')

network_construct('2121939561', 5, 2)