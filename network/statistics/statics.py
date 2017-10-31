# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30th 2017  11:35:00

@author: wangbl
Purpose: statistics of datasets

"""

import csv
import codecs
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import networkx as nx
import pickle

# person_per_paper={}
# i=0


graph = pickle.load(open('../data/nx.pkl', 'rb'))

               #导入科学绘图的matplotlib包
degree =  nx.degree_histogram(graph)
# print(degree)
# plt.loglog()
plt.scatter(degree)#返回图中所有节点的度分布序列


# x = range(len(degree))                             #生成x轴序列，从1到最大度
# y = [z / float(sum(degree)) for z in degree]
# #将频次转换为频率，这用到Python的一个小技巧：列表内涵，Python的确很方便：）
# plt.loglog(x,y,color="blue",linewidth=2)           #在双对数坐标轴上绘制度分布曲线
plt.show()                                                          #显示图表



# def add_networks(dic1, key_a, key_b, val):
#     if key_a in dic1:
#         dic1[key_a].update({key_b: val})
#     else:
#         dic1.update({key_a: {key_b: val}})

# network = {}
# with codecs.open('../data/data.csv', 'r', encoding='utf-8', errors='ignore') as f:
#     f_csv = csv.reader(f)
#
#     for row in f_csv:
#         authors = row[2].split(',')
#
#         for author1 in authors:
#             for author2 in authors:
#                 if author1 not in network or author2 not in network[author1]:
#                     add_networks(network, author1, author2, 1)
#                 else:
#                     network[author1][author2]+=1
#
# json.dump(network,open('../data/raw_network.json','w'))


# network = json.load(open('../data/raw_network.json','r'))




#
#         i+=1
#
# json.dump(person_per_paper,open('../data/person_per_paper.json','w'))
# person_per_paper = json.load(open('../data/person_per_paper.json','r'))
# plt.loglog()
# plt.hist(list(person_per_paper.values()),bins=35)
#
# plt.ylabel('papers')
# plt.xlabel('people')
# plt.title('person per paper distribusion')
# plt.savefig('./person_d.png')
# plt.show()
# plt.clf()



    # print('total number of papers:'+str(i)+'\n')

# paper_per_person = json.load(open('../data/paper_per_author.json','r'))
# # print('total authors:'+str(len(paper_per_person.keys()))+'\n')
#
#
# print('average paper per person'+str(sum(paper_per_person.values())/len(paper_per_person.keys()))+'\n')
# print('average person per paper'+str(len(paper_per_person.keys())/i)+'\n')
# df = pd.DataFrame(paper_per_person)

# x = np.arange(len(paper_per_person))
# plt.bar(x,paper_per_person.values())
# plt.xticks(x,paper_per_person.keys())
# plt.ylim(1,max(paper_per_person.values())+1)
# plt.hist(list(paper_per_person.values()),300,histtype='stepfilled')
# plt.ylabel('people')
# plt.xlabel('papers')
# plt.title('paper distribusion')
# plt.savefig('./paper_d.png')
# plt.show()
# plt.clf()




# plt.hist(paper_per_person.values())
# plt.ylabel('people')
# plt.xlabel('papers')
# plt.title('paper distribusion')
# plt.savefig('./paper_d.png')
# plt.show()
# plt.clf()
