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
with codecs.open('D:/WBL/networkContinue/scrap/tests/all.csv', 'r', encoding='utf-8') as f:
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

with codecs.open('D:/WBL/networkContinue/scrap/tests/all.csv', 'r', encoding='utf-8') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        authors = row[2].split(',')
        time = float(row[4].split('-')[0])

        for a in authors:
            if a not in ppa:
                ppa[a] = [(last_time[a] - time + 1) / (last_time[a] - first_time[a] + 1)]
            else:
                weight = (last_time[a] - time + 1) / (last_time[a] - first_time[a] + 1)
                ppa[a].append(weight)
for a in ppa:
    ppa[a] = sum(ppa[a])
             # /float(len(ppa[a]))


one_hop = []
with codecs.open('D:/WBL/networkContinue/scrap/tests/all.csv', 'r', encoding='utf-8') as f:
    f_csv = csv.reader(f)

    for row in f_csv:
        authors = row[2].split(',')
        time = float(row[4].split('-')[0])
        if '2136372366' in authors:
            if authors[0] != '2136372366' and first_time['2136372366'] < first_time[authors[0]]:
                one_hop.append(authors[0])
                if '2136372366' not in network or authors[0] not in network['2136372366']:
                    # add_networks(network, '2136372366', authors[0], 1)
                    add_networks(network, '2136372366', authors[0],
                                 [(last_time[authors[0]] - time + 1) / (last_time[authors[0]] - first_time[authors[0]] + 1)])
                else:
                    # network['2136372366'][authors[0]] += 1
                    weight = (last_time[authors[0]]-time+1)/(last_time[authors[0]]-first_time[authors[0]]+1)
                    network['2136372366'][authors[0]].append(weight)
                # elif (last_time[authors[0]] - time + 1) / (last_time[authors[0]] - first_time[authors[0]] + 1) > \
                #                                         network['2136372366'][authors[0]]:
                #     network['2136372366'][authors[0]] = (last_time[authors[0]] - time + 1) / (
                #                                             last_time[authors[0]] - first_time[authors[0]] + 1)
                # add_networks(network, '2136372366', authors[0],
                #             (last_time[authors[0]] - time + 1) / (last_time[authors[0]] - first_time[authors[0]] + 1))
# for i in one_hop:
#     print(i)
with codecs.open('D:/WBL/networkContinue/scrap/tests/all.csv', 'r', encoding='utf-8') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        authors = row[2].split(',')
        time = float(row[4].split('-')[0])
        if authors[0] in one_hop:
            for author in authors[1:]:
                if author in one_hop and first_time[author] < first_time[authors[0]]:
                    if author not in network or authors[0] not in network[author]:
                        add_networks(network, author, authors[0], [(last_time[authors[0]]-time+1)/(last_time[authors[0]]-first_time[authors[0]]+1)])
                    else:
                        # network[author][authors[0]] += 1
                        weight = (last_time[authors[0]]-time+1)/(last_time[authors[0]]-first_time[authors[0]]+1)
                        network[author][authors[0]].append(weight)
                    # elif (last_time[authors[0]] - time + 1) / (last_time[authors[0]] - first_time[authors[0]] + 1) > \
                    #         network[author][authors[0]]:
                    #     network[author][authors[0]] = (last_time[authors[0]] - time + 1) / (
                    #         last_time[authors[0]] - first_time[authors[0]] + 1)

                    # add_networks(network, author, authors[0], (last_time[authors[0]]-time+1)/(last_time[authors[0]]-first_time[authors[0]]+1))

for author1 in network:
    for author2 in network[author1]:
        network[author1][author2] = (sum(network[author1][author2])/float(ppa[author2]))
# for author1 in network:
#     for author2 in network[author1]:
#         network[author1][author2] = float(network[author1][author2])/float(ppa[author2])

fr = open('./network_dict_0804_one_hop_right_weight.json', 'w', encoding='utf-8')
json.dump(network, fr, ensure_ascii='false')

# frname = open('./inter_res/paper_per_author.json', 'w', encoding='utf-8')
# json.dump(ppa, frname, ensure_ascii='false')

