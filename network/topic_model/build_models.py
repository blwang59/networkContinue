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
import matplotlib.pyplot as plt
from gensim import corpora,models,similarities



def build_models():

    papers = []

    with codecs.open('../../scrap/tests/all0808_new.csv', 'r', encoding='utf-8', errors='ignore') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            papers.append(row[0])

    st = LancasterStemmer()
    english_stopwards = stopwords.words('english')

    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']


    texts_tokensized = [[word.lower() for word in word_tokenize(document)] for document in papers]
    texts_filtered_stopwords = [[word for word in document if not word in english_stopwards] for document in
                                texts_tokensized]
    texts_filtered = [[word for word in document if not word in english_punctuations] for document in
                      texts_filtered_stopwords]
    texts_stemmed = [[st.stem(word) for word in document] for document in texts_filtered]

    all_stems = sum(texts_stemmed, [])
    stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
    texts = [[stem for stem in text if stem not in stems_once] for text in texts_stemmed]

    dictionary = corpora.Dictionary(texts)

    dictionary.save('./tmp/papers.dict')

    corpus = [dictionary.doc2bow(text) for text in texts]

    corpora.MmCorpus.serialize('./tmp/papers.mm', corpus)

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
    lsi.save('./tmp/model.lsi')

    index.save('./tmp/papers.index')
    ###################################


def get_corpus(author):
    papers_per_author = json.load(open('./papers_per_author.json'))
    if author not in papers_per_author:
        return []
    # if author in papers_per_author:
    papers = papers_per_author[author]
    st = LancasterStemmer()
    english_stopwards = stopwords.words('english')
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
    texts_tokensized = [[word.lower() for word in word_tokenize(document)] for document in papers]
    texts_filtered_stopwords = [[word for word in document if not word in english_stopwards] for document in
                                texts_tokensized]
    texts_filtered = [[word for word in document if not word in english_punctuations] for document in
                      texts_filtered_stopwords]
    texts_stemmed = [[st.stem(word) for word in document] for document in texts_filtered]

    all_stems = sum(texts_stemmed, [])
    stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) == 1)
    texts = [[stem for stem in text if stem not in stems_once] for text in texts_stemmed]

    dictionary = corpora.Dictionary(texts)

    # dictionary.save('./tmp/papers'+str(author)+'.dict')

    corpus = [dictionary.doc2bow(text) for text in texts]

    # corpora.MmCorpus.serialize('./tmp/papers'+str(author)+'.mm', corpus)
    return corpus

    
def similarity_corpus(author1,author2):
    lsi = models.LsiModel.load('./tmp/model.lsi')
    corpus1 = get_corpus(author1)
    corpus2 = get_corpus(author2)

    if corpus1 == [] or corpus2 ==[] :
        return 0

    #Get the mean of all topic distributions in one corpus
    corpus1_topic_vectors = []

    # corpus1 = corpora.MmCorpus('./tmp/papers' + str(author1) + '.mm')
    # corpus2 = corpora.MmCorpus('./tmp/papers' + str(author2) + '.mm')
    for paper in corpus1:
        if paper != []:
            corpus1_topic_vectors.append(lsi[paper])
    corpus1_average = numpy.average(numpy.array(corpus1_topic_vectors), axis=0)

    # Get the mean of all topic distributions in another corpus
    corpus2_topic_vectors = []
    for paper in corpus2:
        if paper != []:
            corpus2_topic_vectors.append(lsi[paper])
    corpus2_average = numpy.average(numpy.array(corpus2_topic_vectors), axis=0)

    # Calculate the distance between the distribution of topics in both corpora
    difference_of_distributions = numpy.linalg.norm(corpus1_average - corpus2_average)
    return difference_of_distributions

if __name__=="__main__":

    # build_models()
    # print(float(similarity_corpus('2126330539','2121939561')))
    # print(float(similarity_corpus('2305185572', '2125104194')))

    # network = json.load(open('../inter_res/network_dict_cotimes.json', encoding='utf-8', errors='ignore'))
    # for author1 in network:
    #     for author2 in network[author1]:
    #         t = network[author1][author2]
    #         network[author1][author2] = [t, float(similarity_corpus(author1,author2))]
    #
    # fr = open('./tmp/codatas.json', 'w', encoding='utf-8', errors='ignore')
    # json.dump(network, fr, ensure_ascii='false')

    network = json.load(open('./tmp/codatas.json'))
    for author1 in network:
        for author2 in network[author1]:
            network[author1][author2][1] = 1.0/(network[author1][author2][1]+1)
    d = []
    for author1 in network:
        for author2 in network[author1]:
            d.append(network[author1][author2])

    plt.xlabel('cooperate times')
    plt.ylabel('similarity')
    plt.scatter(*zip(*d), marker='.')
    plt.show()
