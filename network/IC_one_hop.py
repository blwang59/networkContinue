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
last_time = {}
# only construct v from elder node to yonger node
with codecs.open('D:/WBL/networkContinue/scrap/tests/bigger_all.csv', 'r', encoding='utf-8') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        authors = row[2].split(',')
        time = float(row[4].split('-')[0])
        for a in authors:
            if a not in first_time:
                first_time[a] = time
            else:
                if time < first_time[a]:
                    first_time[a] = time

            if a not in last_time:
                last_time[a] = time
            else:
                if time > last_time[a]:
                    last_time[a] = time
# construct network
one_hop = []
with codecs.open('D:/WBL/networkContinue/scrap/tests/bigger_all.csv', 'r', encoding='utf-8') as f:
    f_csv = csv.reader(f)

    for row in f_csv:
        authors = row[2].split(',')

        if '2136372366' in authors and authors.index['2136372366'] != 1:
            one_hop.append(authors[0])

with codecs.open('D:/WBL/networkContinue/scrap/tests/bigger_all.csv', 'r', encoding='utf-8') as f:
    for authors in one_hop:





# for author1 in network:
#     for author2 in network[author1]:
#         network[author1][author2] = float(network[author1][author2])/float(ppa[author2])
fr = open('./network_dict_0802_time_weight.json', 'w', encoding='utf-8')
json.dump(network, fr, ensure_ascii='false')

# frname = open('./inter_res/paper_per_author.json', 'w', encoding='utf-8')
# json.dump(ppa, frname, ensure_ascii='false')

