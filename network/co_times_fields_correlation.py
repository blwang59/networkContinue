# -*- coding: utf-8 -*-
import json
import codecs
import csv
import matplotlib.pyplot as plt
import numpy as np

network = json.load(open('./inter_res/network_dict_cotimes.json', encoding='utf-8', errors='ignore'))
author_study_field = {}
with codecs.open('D:/WBL/networkContinue/scrap/tests/bigger_all.csv', 'r', encoding='utf-8', errors='ignore') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        authors = row[2].split(',')

        for author in authors:
            if author not in author_study_field:
                author_study_field[author] = set(row[6].rstrip(';').split(';'))
            else:
                author_study_field[author] = (author_study_field[author]) | (set(row[6].rstrip(';').split(';')))

for author in author_study_field:
    if '-' in author_study_field[author]:
        author_study_field[author].remove('-')
        # for i in author_study_field[author]:
        #     print(i)




#
# fr = open('./inter_res/network_dict_cotimes.json', 'w', encoding='utf-8', errors='ignore')
# json.dump(network, fr, ensure_ascii='false')

# network = json.load(open('./inter_res/network_dict_cotimes.json', encoding='utf-8', errors='ignore'))
for author1 in network:
    for author2 in network[author1]:
        t = network[author1][author2]
        network[author1][author2] = [t, len((author_study_field[author1]) & (author_study_field[author2]))]

fr = open('./inter_res/codatas.json', 'w', encoding='utf-8', errors='ignore')
json.dump(network, fr, ensure_ascii='false')


# network = json.load(open('./inter_res/codatas.json'))
#
# d = []
# for author1 in network:
#     for author2 in network[author1]:
#         d.append(network[author1][author2])
#
#
# plt.xlabel('cooperate times')
# plt.ylabel('number of same field of study')
# plt.scatter(*zip(*d), marker='.')
# plt.show()
