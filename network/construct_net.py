import codecs
import csv
import json


def add_networks(dic1, key_a, key_b, val):
    if key_a in dic1:
        dic1[key_a].update({key_b: val})
    else:
        dic1.update({key_a: {key_b: val}})


network = {}
ppa = {}
first_time = {}
# only construct v from elder node to yonger node
with codecs.open('./data/all.csv', 'r', encoding='utf-8') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        authors = row[2].split(',')

        for a in authors:
            if a not in first_time:
                first_time[a] = int(row[4])
            else:
                if int(row[4]) < first_time[a]:
                    first_time[a] = int(row[4])
# construct network
with codecs.open('./data/all.csv', 'r', encoding='utf-8') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        authors = row[2].split(',')     

        for a in authors:
            if a not in ppa:
                ppa[a] = 1
            else:       
                ppa[a] += 1    

        for author1 in authors:
            for author2 in authors:
                if author1 != author2:
                    if first_time[author1] < first_time[author2]:
                        if author1 not in network or author2 not in network[author1] :
                            add_networks(network, author1, author2, 1)
                        else:
                            network[author1][author2] += 1

for author1 in network:
    for author2 in network[author1]:
        network[author1][author2] = float(network[author1][author2])/float(ppa[author2])
fr = open('./network_dict_0728_weight_time.json', 'w', encoding='utf-8')
json.dump(network, fr, ensure_ascii='false')

# frname = open('./inter_res/paper_per_author.json', 'w', encoding='utf-8')
# json.dump(ppa, frname, ensure_ascii='false')

