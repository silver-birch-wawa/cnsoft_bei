#!/usr/bin/env python
# -*- coding:utf-8 -*-
import redis

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
            #print(i)
            goods_name=str(i.decode("utf-8"))
            #print(goods_name)
            value=self.r.lrange(goods_name,0,-1)
            #print(value)
            for j in range(len(value)):
                value[j]=str(value[j].decode("utf-8"))
                #print(value[j])
            data[goods_name]=value
        return data
'''
d1=database()
d2=database()
d3=database()
d1.store('1','2','3')
d2.store('2','3','4')
d3.store('3','4','5')

d1=database()
#d1.store('1','2','3')
print(d1.read())
'''

#d1=database()
#d1.store('test1','test2','test3')
#print(d1.read())
