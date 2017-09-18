# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18th 1:00 2017

@author: wangbl
Purpose: merge the slices into a whole tree,and save the cooperate time when diffusion

"""
import pickle
import re
import os
import networkx as nx
import matplotlib.pyplot as plt

pattern = re.compile(r'.*dot$')
with open('../../results/chenenhong_shift_2.dot','w') as f:
    f.write('strict digraph G{\n')
    for files in os.listdir('./shift2/'):
        if os.path.isfile('./shift2/'+files) and pattern.match('./shift2/'+files):
            with open('./shift2/'+files) as fsource:
                for line in fsource:
                    f.write(line)



