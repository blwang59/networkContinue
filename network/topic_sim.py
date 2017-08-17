# -*- coding: utf-8 -*-
import codecs
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

from gensim import corpora, models, similarities
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

def similarity(article,author):
    dictionary = corpora.Dictionary.load('./topic_model/papers'+str(author)+'.dict')
    # corpus = corpora.MmCorpus('topic_model/papers.mm')
    lsi = models.LsiModel.load('./topic_model/model'+str(author)+'.lsi')
    index = similarities.MatrixSimilarity.load('./topic_model/papers'+str(author)+'.index')

    query_bow = dictionary.doc2bow(article.lower().split())
    query_lsi = lsi[query_bow]
    sims = index[query_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1]) #descendent

    sum = 0
    for item in sims:
        sum+=item[1]
    avg = sum/float(len(sims))

    # delete the others by average value
    if avg >= 0.2:
        return True
    else:
        return False
    #####################################

    # delete the others by the highest threshold
    # if sims[0][1] > 0.3:
    #     return True
    # else:
    #     return False
    ######################################

network = json.load(open('./network_dict_0809_first_site_first_time_with_cheneh.json'))
papers_per_author = json.load(open('./topic_model/papers_per_author.json'))



first_time = json.load(open('./first_time_0809_first_site_first_time_with_cheneh.json'))
time = json.load(open('./time_per_paper_0809_first_site_first_time_with_cheneh.json'))


def add_networks(dic1, key_a, key_b, val):
    if key_a in dic1:
        dic1[key_a].update({key_b: val})
    else:
        dic1.update({key_a: {key_b: val}})


def add_edges(network_this,union_ab,node1,node2,author):
    if node1 in papers_per_author and node2 in papers_per_author and node1 in first_time and node2 in first_time:
        for paper in (set(papers_per_author[node1]) | set(papers_per_author[node2])):

            if similarity(paper,author) == True:
                if paper in papers_per_author[node2]:
                    weight = float(2017.0 - time[paper] + 1) / (2017.0 - first_time[node2] + 1)
                else:
                    weight = float(2017.0 - time[paper] + 1) / (2017.0 - first_time[node1] + 1)
                if node1 not in union_ab or node2 not in union_ab[node1]:
                    add_networks(union_ab, node1, node2, [weight])
                else:
                    union_ab[node1][node2].append(weight)
        for paper in (set(papers_per_author[node1]) & set(papers_per_author[node2])):

            if similarity(paper, author) == True:
                if node1 not in network_this or node2 not in network_this[node1]:

                    add_networks(network_this, node1, node2,
                                 [float(2017.0 - time[paper] + 1) / (2017.0 - first_time[node2] + 1)])
                else:
                    weight = float(2017.0 - time[paper] + 1) / (2017.0 - first_time[node2] + 1)
                    network_this[node1][node2].append(weight)


def select_most_sim(author):
    network_this = {}
    union_ab = {}

    for neighbors in network[author]:
        add_edges(network_this, union_ab, author, neighbors, author)
        if neighbors in network:
            for items in network[neighbors]:
                # for paper in papers_per_author[items]:
                add_edges(network_this, union_ab, neighbors, items, author)

    for author1 in network_this:
        for author2 in network_this[author1]:
            network_this[author1][author2] = sum(network_this[author1][author2]) / sum(union_ab[author1][author2])

                    # if similarity(paper) == False:
                    #     numbers_of_ppa[items] -= 1
                    #     network[neighbors][items] -= 1

    fr = open('./topic_model/network_del_others_avg_'+str(author)+'.json', 'w', encoding='utf-8', errors='ignore')
    json.dump(network_this, fr, ensure_ascii=False)

if __name__=="__main__":

    # select_most_sim('2136372366')#Enhong Chen
    select_most_sim('2153710278')# Hui Xiong
    select_most_sim('2126330539')# Jian Pei
    select_most_sim('2121939561')#Jiawei Han




