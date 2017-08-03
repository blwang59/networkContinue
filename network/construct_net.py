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
with codecs.open('D:/WBL/networkContinue/scrap/tests/bigger_all.csv', 'r', encoding='utf-8', errors='ignore') as f:
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
with codecs.open('D:/WBL/networkContinue/scrap/tests/bigger_all.csv', 'r', encoding='utf-8', errors='ignore') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        authors = row[2].split(',')
        time = float(row[4].split('-')[0])

        for a in authors:
            if a not in ppa:
                ppa[a] = 1
            else:       
                ppa[a] += 1    

        for author1 in authors:
            for author2 in authors:
                if author1 != author2:
                    if author1 in first_time and author2 in first_time\
                        and author1 in last_time and author2 in last_time\
                                   and first_time[author1] < first_time[author2]:
                        if author1 not in network or author2 not in network[author1]:
                            add_networks(network, author1, author2, [(last_time[author2]-time+1)/(last_time[author2]-first_time[author2]+1)])
                        else:
                            weight = (last_time[author2]-time+1)/(last_time[author2]-first_time[author2]+1)
                            network[author1][author2].append(weight)


                        #
                        # elif (last_time[author2]-time+1)/(last_time[author2]-first_time[author2]+1) > network[author1][author2]:
                        #     network[author1][author2] = (last_time[author2]-time+1)/(last_time[author2]-first_time[author2]+1)

for author1 in network:
    for author2 in network[author1]:
        network[author1][author2] = sum(network[author1][author2])/float(len(network[author1][author2]))

#         network[author1][author2] = float(network[author1][author2])/float(ppa[author2])
fr = open('./network_dict_0803_avg_weight.json', 'w', encoding='utf-8', errors='ignore')
json.dump(network, fr, ensure_ascii='false')

# frname = open('./inter_res/paper_per_author.json', 'w', encoding='utf-8')
# json.dump(ppa, frname, ensure_ascii='false')

