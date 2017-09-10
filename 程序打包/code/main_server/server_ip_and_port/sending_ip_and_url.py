# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 17:32:30 2017

@author: wang bei bei
"""
import socket
import time
import threading
def no_retry_sending_ip_and_url(ip,port,proxy_ip,proxy_port,inner_href):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #创建一个socket
    s.connect((ip,port))                       #建立连接
    temp=""
    str="#"
    while(len(proxy_ip)>0):  
        p_ip=proxy_ip.pop()
        p_port=proxy_port.pop()
        temp="%s:%s"%(p_ip,p_port)
        str=str+temp
        #print(len(proxy_ip))
        str=str+"#"
        if str == 'quit':                                #如果为'quit',则退出
            break
    str=str+"  in_hr-"+inner_href
    #print("str:",str)
    s.send(str.encode())                             #发送编码后的数据
    #print(s.recv(1024).decode('utf-8'))
    s.close()                                             #关闭socket 
def sending_ip_and_url(ip,port,proxy_ip,proxy_port,inner_href):
    while(1):
        try:
            no_retry_sending_ip_and_url(ip,port,proxy_ip,proxy_port,inner_href)
        except Exception as e:
            #print(e)
            if("远程主机强迫关闭了一个现有的连接" in str(e)):
                break
            else:
                continue
        break
#sending_ip_and_url("127.0.0.1",8888,["127.0.0.1","127.0.0.2"],[80,90],"aaa")
