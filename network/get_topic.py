# -*- coding: utf-8 -*-
import codecs
import json
import nltk
import csv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import numpy

from gensim import corpora,models,similarities
import pprint

# import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# # get the paper titles#################################
# papers_per_author = {}
# with codecs.open('../scrap/tests/all0808_new.csv', 'r', encoding='utf-8', errors='ignore') as f:
#     f_csv = csv.reader(f)
#     for row in f_csv:
#         nums = row[2].split(',')
#         for num in nums:
#             if num not in papers_per_author:
#                 papers_per_author[num] = [row[0]]
#             else:
#                 papers_per_author[num].append(row[0])
#
#
# fr = open('./topic_model/papers_per_author.json', 'w', encoding='utf-8', errors='ignore')
# json.dump(papers_per_author, fr, ensure_ascii='false')
#############################################################

# st = LancasterStemmer()
# papers = []
# papers_per_author = json.load(open('./topic_model/papers_per_author.json'))
# # with codecs.open('../../aminernetwork/AMiner-Paper.txt', 'r', encoding='utf-8', errors='ignore') as f:
# #     for line in f:
# #         if line[:2]=='#*':
# #         	papers.append(line[2:].rstrip())
#         	# print(papers)
#
# english_stopwards = stopwords.words('english')
#
# english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
#
# papers = papers_per_author['2136372366']
#
#
# # texts_tokensized = [[word.lower() for word in word_tokenize(document)] for document in papers]
# # texts_filtered_stopwords = [[word for word in document if not word in english_stopwards] for document in texts_tokensized]
# # texts_filtered = [[word for word in document if not word in english_punctuations]for document in texts_filtered_stopwords]
# # texts_stemmed = [[st.stem(word) for word in document]for document in texts_filtered]
# #
# # all_stems = sum(texts_stemmed, [])
# # stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
# # texts = [[stem for stem in text if stem not in stems_once] for text in texts_stemmed]
#
# texts = [[word for word in document.lower().split()
#           if word not in english_stopwards and word.isalnum()]
#          for document in papers]
#
# dictionary = corpora.Dictionary(texts)
#
# dictionary.save('./topic_model/papers.dict')
# # print(dictionary)
#
#
# corpus = [dictionary.doc2bow(text) for text in texts]
#
#
#
# corpora.MmCorpus.serialize('./topic_model/papers.mm',corpus)
# # print(corpus)
#
#
# ##LDA model##
# # num_topics = 5
# # num_words = 5
# # passes =20
# # lda = models.LdaModel(corpus,id2word=dictionary, num_topics=num_topics, passes=passes)
# # print(str(texts))
# # pp = pprint.PrettyPrinter(indent=4)
# # pp.pprint(lda.print_topics(num_words=num_words))
# #
# # index = similarities.MatrixSimilarity(lda[corpus])
# # lda.save('./topic_model/model.lda')
# #
# # index.save('./topic_model/papers.index')
#
#
# ###################
# # lsi model:###################
#
#
# tfidf = models.TfidfModel(corpus)
#
# corpus_tfidf = tfidf[corpus]
#
# lsi = models.LsiModel(corpus_tfidf,id2word = dictionary,num_topics = 10)
#
# index = similarities.MatrixSimilarity(lsi[corpus])
# lsi.save('./topic_model/model.lsi')
#
# index.save('./topic_model/papers.index')
# ###################################
#


def get_topic(author):
    st = LancasterStemmer()
    papers = []
    papers_per_author = json.load(open('./topic_model/papers_per_author.json'))
    # with codecs.open('../../aminernetwork/AMiner-Paper.txt', 'r', encoding='utf-8', errors='ignore') as f:
    #     for line in f:
    #         if line[:2]=='#*':
    #         	papers.append(line[2:].rstrip())
    # print(papers)

    english_stopwards = stopwords.words('english')

    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']

    papers = papers_per_author[author]

    # texts_tokensized = [[word.lower() for word in word_tokenize(document)] for document in papers]
    # texts_filtered_stopwords = [[word for word in document if not word in english_stopwards] for document in texts_tokensized]
    # texts_filtered = [[word for word in document if not word in english_punctuations]for document in texts_filtered_stopwords]
    # texts_stemmed = [[st.stem(word) for word in document]for document in texts_filtered]
    #
    # all_stems = sum(texts_stemmed, [])
    # stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
    # texts = [[stem for stem in text if stem not in stems_once] for text in texts_stemmed]

    texts = [[word for word in document.lower().split()
              if word not in english_stopwards and word.isalnum()]
             for document in papers]

    dictionary = corpora.Dictionary(texts)

    dictionary.save('./topic_model/papers'+str(author)+'.dict')
    # print(dictionary)


    corpus = [dictionary.doc2bow(text) for text in texts]

    corpora.MmCorpus.serialize('./topic_model/papers'+str(author)+'.mm', corpus)
    # print(corpus)


    ##LDA model##
    # num_topics = 5
    # num_words = 5
    # passes =20
    # lda = models.LdaModel(corpus,id2word=dictionary, num_topics=num_topics, passes=passes)
    # print(str(texts))
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(lda.print_topics(num_words=num_words))
    #
    # index = similarities.MatrixSimilarity(lda[corpus])
    # lda.save('./topic_model/model.lda')
    #
    # index.save('./topic_model/papers.index')


    ###################
    # lsi model:###################


    tfidf = models.TfidfModel(corpus)

    corpus_tfidf = tfidf[corpus]

    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10)

    index = similarities.MatrixSimilarity(lsi[corpus])
    lsi.save('./topic_model/model'+str(author)+'.lsi')

    index.save('./topic_model/papers'+str(author)+'.index')
    ###################################


get_topic('2136372366')#Enhong Chen
get_topic('2153710278')# Hui Xiong
get_topic('2126330539')# Jian Pei
get_topic('2121939561')#Jiawei Han


