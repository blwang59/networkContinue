# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17th  11:06:00 2017

@author: wangbl
Purpose: find some useful features in networks

"""
import json
import random
import codecs
import pickle
import os
import networkx as nx
import requests
import json
import re
import codecs
import csv
from time import sleep
import random
import matplotlib.pyplot as plt
network = pickle.load(open('../relationship/inter_res/netx/xionghui_onlyNum.pkl', 'rb'))

degree_centralities = nx.degree_centrality(network)
in_degree_centralities = nx.in_degree_centrality(network)
out_degree_centralities = nx.out_degree_centrality(network)

page_ranks = nx.pagerank(network)

CitationCount = {}
totalPaper ={}




def main():
    # names = json.load(open('../inter_res/name_per_author.json', encoding='utf-8', errors='ignore'))
    # CitationCount = pickle.load(open('./inter_res/CitationCount.pkl','rb'))
    # totalPaper = pickle.load(open('./inter_res/totalPaper.pkl', 'rb'))

    for authorNum in network.nodes():
        auID = authorNum

        url = "https://academic.microsoft.com/api/browse/GetEntityDetails?entityId="+auID+"&correlationId=065e52cf-f6b1-4e89-ad4b-f2627cbb6130"
        # url = "https://academic.microsoft.com/#/detail/2136372366"
        headers = {"X-Requested-With": "XMLHttpRequest",
                   "x-ms-request-id": "BOHeG",
                   "Referer": "https://academic.microsoft.com/",
                   "Accept-Encoding": "gzip, deflate, br",
                   "Accept-Language": "zh-CN,zh;q=0.8",
                   "Cookie": "MC1=GUID=8670236b1d1d554798b84e763d033c6d&HASH=6b23&LV=201708&V=4&LU=1502255002053; A=I&I=AxUFAAAAAAACCAAAeVQSRl5HMeDFOimxW+W7YQ!!&V=4; MUID=3E09D7FDE05E6E680B59DD24E45E6DF6; optimizelyEndUserId=oeu1502786157036r0.7162413590518786; WT_FPC=id=2a38e14d977c7f47afc1502728703504:lv=1502728703504:ss=1502728703504; omniID=1502786303943_250f_1e8a_6a1d_d36601667d4c; MSFPC=ID=8670236b1d1d554798b84e763d033c6d&CS=3&LV=201708&V=1; visid_incap_743080=lK+dZp/UTnezq3R3R3+AOXKmllkAAAAAQUIPAAAAAAClNqabNtzv34m281ZgIbck; msacademic=43c24a41-4399-4b66-ac02-c960e23ab886; ai_user=gYti1|2017-08-31T01:11:26.970Z; RPSShare=1; ANON=A=16B332EB098F5CA686B6D141FFFFFFFF&E=1426&W=1; NAP=V=1.9&E=13cc&C=YmPWfgc9dWxfB8qwkXJb9YJawfkZtXfb60IKrSKsn4ALe7Ai4GjNTQ&W=1; MSCC=1505290470; ARRAffinity=5a6dd6480c1b98b17d999353b0c9c06d5bd94d7eb0b539de7aa1e956b6f29aff; __RequestVerificationToken=vyd9gOoGMpatlo_pW0GAz2BW-FwmQBiEwXJO0HWMaqMPUzrAMDAG7MCa_5ozXDiGxV83cMBUmX7M3i5_rsHz7yS-p7qNiYS88uplskbvuQg1; WRIgnore=true; __CT_Data=gpv=3&apv_32381_www07=3&cpv_32381_www07=3; MS0=fab3d4f21b964f108630569336eed919; ai_session=TZns9|1508307882619|1508310961609.31"
        }

        content = requests.get(url,headers = headers) # 用post提交form data
        contents = json.loads(content.text)

        CitationCount[auID]=contents['estimatedCitationCount']
        totalPaper[auID] = contents['publications']['m']['lt']

    fn = './inter_res/xionghui_CitationCount.pkl'
    pickle.dump(CitationCount, open(fn, 'wb'))
    f = './inter_res/xionghui_totalPaper.pkl'
    pickle.dump(totalPaper, open(f, 'wb'))

    # x = list(CitationCount.keys())
    # y1 = list(CitationCount.values())
    # y1 = [y * 0.0001 for y in y1]
    # y2 = list(degree_centralities.values())
    # # y2 = [y*10000 for y in y2]
    # y3 = list(page_ranks.values())
    # # y3 = [y * 10000 for y in y3]
    # y4 = list(totalPaper.values())
    # y4 = [float(y) * 0.001 for y in y4]
    # plt.scatter(x, y1,marker ='o',label = 'citation count*0.0001')
    # plt.scatter(x,y2, marker= '*', label ='degree centrality')
    # plt.scatter(x,y3, marker= '^',label = 'page rank')
    # plt.scatter(x, y4, marker='v', label='total paper*0.001')
    # plt.legend()
    # plt.show()



if __name__ == '__main__':
    main()




