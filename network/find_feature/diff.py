# -*- coding: utf-8 -*-
"""
Created on Mon OCt 16th  19:05:00 2017

@author: wangbl
Purpose: compare the difference between the two files in this dir

"""

import codecs
import json
import re

import os
# import pydot
from IPython.display import Image
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
                    fw.write(line.strip()+'[color = red]\n')
                else:
                    fw.write(line)

    with codecs.open(after, 'r', encoding='utf-8', errors='ignore') as f2:
        with codecs.open(result2, 'w', encoding='utf-8', errors='ignore') as fw:
            for line in f2:

                if line in diff:
                    fw.write(line.strip() + '[color = red]\n')
                else:
                    fw.write(line)

# names = json.load(open('../inter_res/name_per_author.json', encoding='utf-8', errors='ignore'))
#
# compare('chenenhong_10.dot','chenenhong_shift_2.dot','./comp/chenenhong_10.dot','./comp/chenenhong_shift_2.dot')

from subprocess import check_call
check_call(['dot','-Tpng','./comp/chenenhong_10.dot','-o','./comp/chenenhong_10.png'])
check_call(['dot','-Tpng','./comp/chenenhong_shift_2.dot','-o','./comp/chenenhong_shift_2.png'])