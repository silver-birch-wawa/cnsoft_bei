#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 20:52:17 2017

@author: wang bei bei
"""
import socket
import time,socketserver
import threading,time,queue
def TCP_receiver(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip,port))
    s.listen(1)
    print('Server is running...')  
    sock, addr = s.accept()                            #接收一个新连接
    data = sock.recv(2024)                         #接受其数据
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

while(1):
    receiver('127.0.0.1',8888)
'''

##########################接受验证了的url#################################
class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        global unrepeated_good_url,unrepeated_list_url,waiting_url
        conn = self.request
        while (1):
            lock.acquire()
            print("start listening.")
            try:
                data = conn.recv(1024)
            except Exception as e:
                print(e)
                continue
            lock.release()
            cur_thread = threading.current_thread()
            if(data!=b"" and "unrepeated" in data):
                data=str(data)[1:]
                print(cur_thread.name,"  :",data)    
                if("unrepeated" in data):
                    if('list' in data):
                        print("unrepeated list_url: ",data)
                        unrepeated_list_url.put(data)
                    elif('/item' in data):
                        print("unrepeated good_url: ",data)
                        unrepeated_good_url.put(data)
                    elif('//detail' in data):       #淘宝中的detail为重复链接需要去掉
                        print("unrepeated good_url: ",data)
                        unrepeated_good_url.put(data)
                    else:
                        print("other types url:",data)
                        waiting_url.put(data)
                time.sleep(1)
            #time.sleep(2)

def receiving_the_unrepeated_url(remoted_ip='127.0.0.1',url_checking_port=8770):
    global unrepeated_url_queue,unrepeated_list_url,unrepeated_good_url
    server = socketserver.ThreadingTCPServer((remoted_ip,url_checking_port),MyServer)
    ip,port=server.server_address
    server.serve_forever()

 