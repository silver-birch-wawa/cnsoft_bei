# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 17:49:24 2017

@author: wang bei bei
"""
import socket
import time
import threading
import re,queue
from receiver import TCP_receiver
##############TCP一次性通讯模块,接受报文中含#与:的数据##############
def TCP_receiver(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip,port))
    s.listen(3) 
    sock, addr = s.accept()                            #接收一个新连接
    #print("Sending the ask............")
    while True:
        #print("???????")
        data = sock.recv(4096)                         #接受其数据
        #print("data: ",data)
        #time.sleep(1)                                  #延迟
        if data !=None:        #如果数据为空或者'quit'，则退出
            break
    sock.close()                                      #关闭连接
    print('Connection from %s:%s closed.' %addr) 
    return data
##################正则表达式抽取ip与port######################
def pick_up_the_ip_and_url(data):
    proxy_ip=queue.Queue()
    proxy_port=queue.Queue()
    for i in re.finditer("(#.*?):",data):
        try:
            ip=i.group()
        except Exception as e:
            print(e)
        proxy_ip.put(ip[1:-1])
        #print("ip:",ip[1:-1])
    for j in re.finditer(":(.*?)#",data):
        try:
            port=j.group()
        except Exception as e:
            print(e)
        proxy_port.put(port[1:-1])
        #print("port:",port[1:-1])
    return proxy_ip,proxy_port
def pick_up_the_href(data):
    return re.search("hr-[^ ]*",data).group()[3:]
#############总函数,返回ip与port的队列queue##############
def receiving_ip_and_port(ip,port):   
    data=""
    while(1):
        data=TCP_receiver(ip,port)
        if(data!=None):
            #print(type(data))
            #print(data)
            data=data.decode("utf-8")
            data=str(data)
            print("data: ",data)
            #time.sleep(10)
            proxy_ip,proxy_port=pick_up_the_ip_and_url(data)
            inner_href=pick_up_the_href(data)
            return proxy_ip,proxy_port,inner_href
#print(receiving_ip_and_port('127.0.0.1',8880))
#返回接受的信息
    
    
    
    
