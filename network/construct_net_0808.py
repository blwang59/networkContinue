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
# last_time = {}
union_ab = {}
time_per_paper={}
# only construct v from elder node to yonger node
with codecs.open('../scrap/tests/all0808_new.csv', 'r', encoding='utf-8', errors='ignore') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        authors = row[2].split(',')
        time = float(row[4].split('-')[0])
        time_per_paper[row[0]] = time
        # for a in authors:
        if authors[0] not in first_time:
            first_time[authors[0]] = time
        else:
            if time < first_time[authors[0]]:
                first_time[authors[0]] = time

            # if a not in last_time:
            #     2017.0 = time
            # else:
            #     if time > 2017.0:
            #         2017.0 = time

# print('Yanjie Fu:'+str(first_time['2168873515']))
# print('Zijun Yao:'+str(first_time['2229271911']))
# print('Junming Liu:'+str(first_time['2226988312']))
# print('Guannan Liu:'+str(first_time['2273869953']))


with codecs.open('D:/WBL/networkContinue/scrap/tests/all0808_new.csv', 'r', encoding='utf-8', errors='ignore') as f:
   f_csv = csv.reader(f)
   for row in f_csv:
       authors = row[2].split(',')
       time = float(row[4].split('-')[0])

       for a in authors:
           if a not in ppa:
               ppa[a] = set(row[0].split())
           else:
               # weight = (2017.0 - time + 1) / (2017.0 - first_time[a] + 1)
               ppa[a].add(row[0])

       if len(authors) > 1:
           for author1 in authors[1:]:
           # for author2 in authors:
               author2 = authors[0]
               if author1 in ppa and author2 in ppa and author1 in first_time and author2 in first_time:
                   for paper in (ppa[author1] | ppa[author2]):
                       if paper in ppa[author2]:
                           weight = float(2017.0-time+1)/(2017.0-first_time[author2]+1)
                       else:
                           weight = float(2017.0 - time + 1) / (2017.0 - first_time[author1] + 1)
                       if author1 not in union_ab or author2 not in union_ab[author1]:
                           add_networks(union_ab, author1, author2, [weight])
                       else:
                           union_ab[author1][author2].append(weight)



               if author1 in first_time and author2 in first_time\
                              and first_time[author1] <= first_time[author2]:
                   if author1 not in network or author2 not in network[author1]:
                       add_networks(network, author1, author2, [float(2017.0-time+1)/(2017.0-first_time[author2]+1)])
                   else:
                       weight = float(2017.0-time+1)/(2017.0-first_time[author2]+1)
                       network[author1][author2].append(weight)



                        # elif (2017.0-time+1)/(2017.0-first_time[author2]+1) > network[author1][author2]:
                        #     network[author1][author2] = (2017.0-time+1)/(2017.0-first_time[author2]+1)

for author1 in network:
   for author2 in network[author1]:
       network[author1][author2] = sum(network[author1][author2])/sum(union_ab[author1][author2])


fr = open('./network_dict_0809_first_site_first_time_with_cheneh.json', 'w', encoding='utf-8', errors='ignore')
json.dump(network, fr, ensure_ascii='false')



