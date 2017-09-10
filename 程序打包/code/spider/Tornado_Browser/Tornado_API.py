# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 16:14:51 2017

@author: wang bei bei
"""
#####负责发送给浏览器的数据：
from Tornado_Browser.Tornado_listener import DATA,URL
import tornado.ioloop
import tornado.web

def DATA_LISTEN_AND_SEND(port=10008):    
    application = tornado.web.Application([
    (r"/", DATA),
    ])
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()

def URL_LISTEN_AND_SEND(port=10000):    
    application = tornado.web.Application([
    (r"/url", URL),
    ])
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()

'''
####### API使用方法 #######
from Tornado_Browser.Tornado_API import LISTEN_AND_SEND
from Tornado_Browser.parameter import data,DATA
import random,time,threading
def test():
    global data
    while(1):
        time.sleep(1)
        data.get_data(random.random(),random.random(),random.random(),random.random(),random.random())

threads=[]
t=threading.Thread(target=test,args=())
threads.append(t)
    
t=threading.Thread(target=LISTEN_AND_SEND,args=())
threads.append(t)

for i in range(len(threads)):
    print("start第%d个线程"%i)
    threads[i].start()

for i in range(len(threads)):
    print("start第%d个线程"%i)
    threads[i].join()
'''