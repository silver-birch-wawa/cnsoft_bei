#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append("..")

from Tornado_Browser.Tornado_listener import DATA,URL
import tornado.ioloop
import tornado.web
from Tornado_Browser.Tornado_API import URL_AND_DATA_LISTEN_AND_SEND
from Tornado_Browser.parameter import input_url,data,set_,goods
import random,time,threading
from tornado import websocket
from redis_module.redis_store import database
d=database()
def pick_up_goods():
    global data,set_,goods
    #goods=d.read()
    pre_length=0
    while(1):
        time.sleep(0.5)
        goods=d.read()
        #print("----goods: ",goods)
        length=len(goods)
        try:
            if(length>0 and length!=pre_length):
                pre_length=length
                print("okkkkkkkkkkkkk...........")
                for i in goods.items():
                    goods_name=i[0]
                    if(goods_name not in set_):
                        price=i[1][0]
                        store_name=i[1][1]
                        set_.add(goods_name)
                        print("\n****goods_name: ",goods_name)
                        print("\n****price",price)
                        print("\n****store_name",store_name)
                        data.get_data(goods_name,store_name,price)
                        time.sleep(0.5)
        except Exception as e:
            print(e)
                    #print(input_url)
                    #print(data.to_String())
def run_tolnado():
    application = tornado.web.Application([
    (r"/", DATA),
    ])

    url_receiving = tornado.web.Application([
    (r"/url", URL),
    ])

    threads=[]
    t=threading.Thread(target=pick_up_goods,args=())
    threads.append(t)

    for i in range(len(threads)):
        print("start No.%d..."%i)
        threads[i].start()

    application.listen(10008)
    url_receiving.listen(10000)
    tornado.ioloop.IOLoop.instance().start()
#run_tolnado()
