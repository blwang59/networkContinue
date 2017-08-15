# -*- coding: utf-8 -*-
import codecs
import json

def compare(before, after, result1, result2):
    before_set = set()
    after_set = set()
    with codecs.open(before, 'r', encoding='utf-8', errors='ignore') as f1:
        for line in f1:
            before_set.add(line.split('[')[0])
    with codecs.open(after, 'r', encoding='utf-8', errors='ignore') as f2:
        for line in f2:
            after_set.add(line.split('[')[0])

    # diff = set()
    diff = (before_set | after_set) - (before_set & after_set)
    with codecs.open(before, 'r', encoding='utf-8', errors='ignore') as f1:
        with codecs.open(result1, 'w', encoding='utf-8', errors='ignore') as fw:
            for line in f1:

                if line.split('[')[0] in diff:
                    fw.write(line[:-1]+'[color = red]\n')
                else:
                    fw.write(line)

    with codecs.open(after, 'r', encoding='utf-8', errors='ignore') as f2:
        with codecs.open(result2, 'w', encoding='utf-8', errors='ignore') as fw:
            for line in f2:

                if line in diff:
                    fw.write(line[:-1] + '[color = red]\n')
                else:
                    fw.write(line)

# names = json.load(open('./inter_res/name_per_author.json', encoding='utf-8', errors='ignore'))

compare('./inter_res/IC0815/Enhong Chen_0001.dot','./inter_res/IC0815/Enhong Chen_0001_topic_avg_20.dot','./inter_res/IC0815/compare/Enhong Chen_0001.dot','./inter_res/IC0815/compare/Enhong Chen_0001_topic_avg_20.dot')
compare('./inter_res/IC0815/Hui Xiong_0001.dot','./inter_res/IC0815/Hui Xiong_0001_topic_avg_20.dot','./inter_res/IC0815/compare/Hui Xiong_0001.dot','./inter_res/IC0815/compare/Hui Xiong_0001_topic_avg_20.dot')
compare('./inter_res/IC0815/Jian Pei_0001.dot','./inter_res/IC0815/Jian Pei_0001_topic_avg_20.dot','./inter_res/IC0815/compare/Jian Pei_0001.dot','./inter_res/IC0815/compare/Jian Pei_0001_topic_avg_20.dot')
compare('./inter_res/IC0815/Jiawei Han_0001.dot','./inter_res/IC0815/Jiawei Han_0001_topic_avg_20.dot','./inter_res/IC0815/compare/Jiawei Han_0001.dot','./inter_res/IC0815/compare/Jiawei Han_0001_topic_avg_20.dot')



