#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 20:52:17 2017

@author: wang bei bei
"""
import socket
import time
import threading
def TCP_receiver(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(ip,port)
    s.bind((ip,port))
    s.listen(100)
    print('Server is running...')
    sock, addr = s.accept()                            #接收一个新连接
    try:
        data = sock.recv(2024)                         #接受其数据
    except Exception as e:
        print(e)
    sock.close()                                      #关闭连接
    print('Connection from %s:%s closed.' %addr)
    return addr,data
def receiver(ip,port):
    data=""
    while(1):
        addr,data=TCP_receiver(ip,port)
        if(data!=None):
            print(type(data))
            print(data)
            return data

'''
thread_num=5
threads=[]
for i in range(thread_num):
    t=threading.Thread(target=TCP_receiver,args=('127.0.0.1',8888,))
    threads.append(t)
for i in range(thread_num):
    print("start第%d个线程"%i)
    threads[i].start()
for i in range(thread_num):
    threads[i].join()
#返回接受的信息
'''
