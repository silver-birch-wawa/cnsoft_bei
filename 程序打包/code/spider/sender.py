# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 11:27:58 2017

@author: wang bei bei
"""
import socket
import time
import threading
def no_retry_TCP_sender(ip,port,input):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #创建一个socket
    s.connect((ip,port))                       #建立连接
    while True:                                           #接受多次数据
        data = input               #接收数据
        if data == 'quit':                                #如果为'quit',则退出
            break
        s.send(data.encode())                             #发送编码后的数据
    s.close()                                             #关闭socket    
#TCP_sender('127.0.0.1',8888,"************")
def TCP_sender(ip,port,data):
    while(1):
        try:
            no_retry_TCP_sender(ip,port,data)
        except Exception as e:
            #print(e)
            if("远程主机强迫关闭了一个现有的连接" in str(e)):
                break
            else:
                continue
