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
    #while True:                                           #接受多次数据
    data = input               #接收数据
    s.send(data.encode("utf-8"))                             #发送编码后的数据
    s.close()                                             #关闭socket
def TCP_sender(ip,port,data):
    while(1):
        try:
            no_retry_TCP_sender(ip,port,data)
        except Exception as e:
            print("xxxx: ",e)
            if("无法连接" in str(e)):
                break
            else:
                continue
'''
no_retry_TCP_sender('127.0.0.1',9990,"1111")
no_retry_TCP_sender('127.0.0.1',9990,"2222")
no_retry_TCP_sender('127.0.0.1',9990,"3333")
'''
