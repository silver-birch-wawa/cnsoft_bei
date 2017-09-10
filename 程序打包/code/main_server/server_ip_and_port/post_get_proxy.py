# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 21:10:42 2017

@author: wang bei bei
"""
import requests
import time
import re
from bs4 import BeautifulSoup
#具体爬取的页数
N=3
pages=N

proxy_list=[]
port=[]
#########采集代理###########
def post_get_proxy():
    global pages
    proxy_list=[]
    pr=re.compile("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+")
    po=re.compile("^[0-9]+$")
    headers = {
"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}   
    for i in range(pages-1,pages+1):
        time.sleep(1)
        if(i==0):
            r=requests.get("http://www.xicidaili.com/nn",headers=headers,)
        else:
            r=requests.get("http://www.xicidaili.com/nn/"+str(i),headers=headers,)
        bs4=BeautifulSoup(r.text)
        for i in bs4.find_all("td"):
            pi=pr.match(i.text)
            #proxy=pi.group()
            if(pi!=None):
                proxy=pi.group()
                #print("proxy:",proxy)
                proxy_list.append(proxy)
            pi=po.match(i.text)
            if(pi!=None):
                proxy=pi.group()
                #print("port:",proxy)
                port.append(proxy)
    pages=pages+N
    return proxy_list,port,pages
'''
pr,po=post_get_proxy()
print(pr,po)
'''
