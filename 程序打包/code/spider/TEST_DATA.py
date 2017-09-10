#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tornado_Browser.Tornado_API import DATA_LISTEN_AND_SEND
from Tornado_Browser.parameter import data
import random,time,threading
def test():
    global data
    while(1):
        time.sleep(1)
        data.get_data(random.random(),random.random())

threads=[]
t=threading.Thread(target=test,args=())
threads.append(t)
    
t=threading.Thread(target=DATA_LISTEN_AND_SEND,args=(10008,))
threads.append(t)

for i in range(len(threads)):
    print("start NO.%d"%i)
    threads[i].start()

for i in range(len(threads)):
    print("start No.%d"%i)
    threads[i].join()