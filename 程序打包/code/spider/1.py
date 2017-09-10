#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 16:57:48 2017

@author: wang bei bei
"""

from bs4 import BeautifulSoup
import redis,queue,re
from bs4 import BeautifulSoup
from selenium import webdriver
class database():
    def __init__(self):
        self.r=redis.Redis(host='127.0.0.1', port=6379,db=0)
    def store(self,goods_name,goods_price,store_name):
        try:
            self.r.lpush(goods_name, store_name)
            self.r.lpush(goods_name,goods_price)
        except Exception as e:
            print("error in storing.....",e)
    def read(self):
        data={}
        for i in self.r.keys():
            name=str(i)[2:-1]
            print(name)
            value=self.r.lrange(name,0,-1)
            for j in range(len(value)):
                value[j]=str(value[j])[2:-1]
            data[name]=value
        return data
################检查是否是商品页####################
def check_if_the_page_is_goods_pages(url):
    if("item" in url):
        r=requests.get(url)
        if("加入购物车" in r.text):
            return True
    return False
##################################################
def pick_up_the_price(text):
    #单纯提取数字会跟划去的价格混淆,计算机无法理解促销价以及售价,京东价是什么东西.....所以迫于无奈只能强行一对一匹配
    #淘宝,天猫还有的price有毒别人都是125.84它偏偏来个124.98-238.45
    #利用class中存在price/rmb的特点,一个一个class抽取匹配过去,然后根据相对位置定位具体位置      ￥  ¥
    price_stack=[]
    if("¥" in text):   #京东是¥ 网易严选是¥
        for i in re.findall("¥.*>\d+\.\d+-\d+\.\d+<?",driver.page_source):
            try:
                if(len(i)<80):
                    print(i)
                    price=re.search("\d+\.\d+-\d+\.\d+",i)
                    if(price!=None):
                        price_stack.append(price.group())
                        print(price)
                        if(len(price_stack)==2):
                            return str(price_stack)[1:-1]
            except Exception as e:
                print("Error in Money 1:  "+e)
        if(len(price_stack)==1):
            return str(price_stack)[1:-1]
        elif(len(price_stack)==0):
            try:
                for i in re.findall("¥.*>\d+\.\d+<?",driver.page_source):
                    print(i)
                    if(len(i)<80):
                        price=re.search(">\d+\.\d+<",i)
                        if(price!=None):
                            price=price.group()
                            print(price[1:-1])
                            return price[1:-1]
                        else:
                            print("竟然为空？")
            except Exception as e:
                print("Error in Money 2:  "+e)
        try:
            for i in re.findall(">¥.*\d+.*<",driver.page_source):
                return re.search("\d+\.\d+",i).group()
        except Exception as e:
            print("Error in Money 3:  "+e)          
    ##########另一种￥###########
    elif("￥" in text):
        for i in re.findall("￥.*>\d+\.\d+-\d+\.\d+<?",driver.page_source):
            if(len(i)<80):
                price=re.search("\d+\.\d+-\d+\.\d+",i)
                if(price!=None):
                    price_stack.append(price.group())
                    print(price)
                    if(len(price_stack)==2):
                        return str(price_stack)[1:-1]
        if(len(price_stack)==1):
            return str(price_stack)[1:-1]
        elif(len(price_stack)==0):
            for i in re.findall("￥.*>\d+\.\d+<?",driver.page_source):
                if(len(i)<80):
                    price=re.search("\d+\.\d+",i)
                    if(price!=None):
                        price=price.group()
                        print(price)
                        return price
                    else:
                        print("竟然为空？")
        for i in re.findall(">￥.*\d+.*<",driver.page_source):
            return re.search("\d+\.\d+",i).group()  
def pick_up_store_name(text,bs4):
    #进入店铺 或者 进店逛逛 的链接跟 店铺名的链接一样.....抓出来链接地址再匹配href中的链接地址就可以了
    #先把html编码进行一下转换
    text=text.replace('&gt;','>')
    text=text.replace('&lt;','<')
    bs4=BeautifulSoup(text)
    try:
        for i in re.findall("<a.*>.*</a>?",driver.page_source):
            #print(i)
            if('进入店铺' in i or '进店逛逛' in i):
                href=re.search('href="[^"]+"?',i).group()[6:-1]
    except Exception as e:
        print('店铺匹配bug1: ',e)
    try:
        for i in re.findall("<a.*>.*</a>?",driver.page_source):
            if("店" in i):
                store_name=re.search('[^\W]+店',i).group()
                if(len(store_name)>4):
                    print(store_name)
                    return store_name
    except Exception as e:
        print('店铺匹配bug2: ',e)
    try:
        for i in bs4.find_all('a'):
                if(i.get('href') in href or href in i.get('href')):
                    #print(i.get_text())
                    #print(href)
                    store_name=re.search('[^\s]+',i.get_text()).group()
                    if(len(store_name)>4):
                        #店铺名一般都比较长。。。
                        return store_name
    except Exception as e:
        print('店铺匹配bug3: ',e)
    return ''

def pick_up_the_elements_and_store_in(driver,d):
    global goods_price_class
    text=driver.page_source
    if("加入购物车" in text):
        bs4=BeautifulSoup(text)
        try:
            goods_name=re.findall('[^-]+',driver.title)[0]
            goods_price=pick_up_the_price(driver.page_source)
            store_name=pick_up_store_name(text,bs4)
            if(goods_price!=None and store_name!=None and goods_name!=None):
                print('title: ',goods_name)
                print('price: ',goods_price)
                print('store name: ',store_name)
                #d.store(goods_name,goods_price,store_name)
            else:
                print("\n\n奇怪啊，竟然匹配到了None.....\n\n")
                print('title: ',goods_name)
                print('price: ',goods_price)
                print('store name: ',store_name)
                #d.store(goods_name,goods_price,store_name)
        except Exception as e:
            print(e)

driver=webdriver.PhantomJS()
#url="http://you.163.com/item/detail?id=1233003&_stat_area=mod_newItem_item_4&_stat_referer=index"
#url="http://you.163.com/item/detail?id=1221000&_stat_area=mod_newItem_item_1&_stat_referer=index"
#url="https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.32.4c637810lnWd70&id=45643677847&skuId=87162814824&user_id=353646075&cat_id=50026637&is_b=1&rn=e80ca2ed42d55c7c7aa46358122c2107"
#url="https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.186.4c6378106tDUQd&id=528602202134&user_id=709120984&cat_id=50025174&is_b=1&rn=d4d13201db25d57d67fa1d5adb80d58e"
#url="https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.14.4c6378106tDUQd&id=544847283618&skuId=3404049988921&user_id=94399436&cat_id=50025174&is_b=1&rn=d4d13201db25d57d67fa1d5adb80d58e"
#url="https://item.taobao.com/item.htm?spm=a219r.lm895.14.66.3d86c53cexgtJa&id=550339972541&ns=1&abbucket=9"
#url="https://item.taobao.com/item.htm?spm=a219r.lm895.14.128.3d86c53cexgtJa&id=539328497400&ns=1&abbucket=9"
#url="https://item.jd.com/3342046.html?cpdad=1DLSUE"
#url="https://item.jd.com/12155418.html"
#url="http://item.jd.com/10620059864.html"
#url="https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.9.4c637810lcVdYe&id=538977545879&skuId=3433030082653&user_id=765391429&cat_id=56148012&is_b=1&rn=6ca2564ec281051a1a646be589b32cc7"
#url="https://item.taobao.com/item.htm?spm=a219r.lm869.14.1.43820727unCQgF&id=556853859479&ns=1&abbucket=9#detail"
#url="https://item.taobao.com/item.htm?spm=a219r.lm869.14.16.43820727wyRDQF&id=556726483850&ns=1&abbucket=9#detail"
driver.get(url)
#d=database()
d=""
pick_up_the_elements_and_store_in(driver,d)     
#driver.close()

  