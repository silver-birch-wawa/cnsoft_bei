# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 20:40:45 2017

@author: wang bei bei
"""
def de_weight(set_,add_thing):
    if(add_thing in set_):
        print("Sorry, the url %s is repeated."%add_thing)
        return -1
    else:
        print("Adding this url %s into the set"%add_thing)
        set_.add(add_thing)
        return 0
'''
set_=set(['b','c'])
print(de_weight(set_,"http://baidu.com"))
'''
