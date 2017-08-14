# -*- coding: utf-8 -*-
import codecs
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

from gensim import corpora, models, similarities


def similarity(article):
    dictionary = corpora.Dictionary.load('./topic_model/papers.dict')
    # corpus = corpora.MmCorpus('topic_model/papers.mm')
    lsi = models.LsiModel.load('./topic_model/model.lsi')
    index = similarities.MatrixSimilarity.load('./topic_model/papers.index')

    query_bow = dictionary.doc2bow(article.lower().split())
    query_lsi = lsi[query_bow]
    sims = index[query_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    # print(list(enumerate(sims)))
    if sims[0][1] > 0.3:
        return True
    else:
        return False


# print(str(similarity('ArnetMiner: extraction and mining of academic social networks')))

# with codecs.open('../../aminernetwork/AMiner-Paper.txt', 'r', encoding='utf-8', errors='ignore') as f:
#     for line in f:
#         if line != '\n':
#             l = line.rstrip().split(' ',1)
#             if len(l) > 1:
#                 mess[l[0]] = l[1]
#         if line == '\n':
#             if '#@' in mess and '#*' in mess:
#                 authors = mess['#@'].split(';')
#                 for a in authors:
#                     if a not in author_dict:
#                         author_dict[a]=[]
#                         author_dict[a].append(mess['#*'])
#                     else:
#                         author_dict[a].append(mess['#*'])
#     mess = {}


network = json.load(open('./network_dict_0809_first_site_first_time_with_cheneh.json'))
papers_per_author = json.load(open('./topic_model/papers_per_author.json'))

numbers_of_ppa = dict.fromkeys(papers_per_author, 0)
for item in numbers_of_ppa:
    numbers_of_ppa[item] = len(papers_per_author[item])
i = 0
index = 0
for neighbors in network['2136372366']:
    # if i == 1 :
    #     break
    if neighbors in network:
        for items in network[neighbors]:

            # index += 1
            # if index > 10000:
            #     i = 1

            #     break
            # print('find 2000 nodes!')
            for paper in papers_per_author[items]:
                if similarity(paper) == False:
                    numbers_of_ppa[items] -= 1
                    network[neighbors][items] -= 1

for i in network:
    for j in network[i]:
        if numbers_of_ppa[j] == 0:
            network[i][j] = 0
        else:
            network[i][j] = network[i][j] / int(numbers_of_ppa[j])

fr = open('./topic_model/network_del_others.json', 'w', encoding='utf-8', errors='ignore')
json.dump(network, fr, ensure_ascii=False)




#