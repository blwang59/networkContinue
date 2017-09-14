# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11th 09:43:37 2017

@author: wangbl
Purpose: transform these dot into png or pdf,convenient to read.


"""
import pydotplus
import re
import os
# import pydot
from IPython.display import Image

def show_dot_in(dir_path,des_path):
    pattern = re.compile(r'.*dot$')
    for files in os.listdir(dir_path):
        # print(files)
        if os.path.isfile(dir_path+files) and pattern.match(dir_path+files):
        #     print('1')
            graph = pydotplus.graphviz.graph_from_dot_file(dir_path+files)
            # print ('1')
            graph.write_png(des_path+files.split('.')[0]+'.png')
            # Image(graph.create_png(), width = 800, height = 800)
show_dot_in('./results/include_seeds/shift2/','./results/include_seeds/shift2/')