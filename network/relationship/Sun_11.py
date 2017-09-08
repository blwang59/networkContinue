# -*- coding: utf-8 -*-
"""
Created on Fri Sep 1st 10:40:37 2017

@author: wangbl
Purpose: meta path-based topology in Co-Author Relationship Prediction in Heterogeneous Bibliographic Networks
by Y.Sun et al,2011


"""

import codecs
import csv
import json

with codecs.open('../data/data.csv', 'r', encoding='utf-8', errors='ignore') as f:
    f_csv = csv.reader(f)
    time = 2099
    for row in f_csv:
        if "Enhong Chen" in row[1]:

            if time > int(row[4].split('-')[0]):
                time = int(row[4].split('-')[0])
print (time)