# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 11:27:58 2017

@author: wang bei bei
"""
import socket,socketserver
import time
def no_retry_TCP_sender(ip,port,input):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #创建一个socket
    s.connect((ip,port))                       #建立连接
    data = input               #接收数据
    s.send(data.encode())                             #发送编码后的数据
    s.close()                                             #关闭socket
def TCP_sender(ip,port,data):
    while(1):
        try:
            no_retry_TCP_sender(ip,port,data)
        except Exception as e:
            print('error in TCP_sending',e)
            if("远程主机强迫关闭了一个现有的连接" in str(e)):
                break
            else:
                continue
        break
#######################多线程接受url+去重模块#############################
def processing_the_url(conn,lock,data,set_,t_num):
    if data in set_:
        q=data+"  repeated"
        lock.wait(t_num)
        try:
            conn.sendall(q.encode())
            lock.signal(t_num)
        except Exception as e:
            lock.signal(t_num)
    else:
        q=data+"  unrepeated"
        lock.wait(t_num)
        set_.add(data)
        try:
            conn.sendall(q.encode())
            lock.signal(t_num)
        except Exception as e:
            print(e)
            lock.signal(t_num)

class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        global q,set_#去重用的set还有接受用的队列
        conn = self.request
        while (1):
            print("start listening.")
            try:
                data = conn.recv(1024)
            except Exception as e:
                print(e)
                continue
            cur_thread = threading.current_thread()
            if(data!=b""):
                data=str(data)[1:]
                print(cur_thread.name,"  :",data)
                processing_the_url(conn,lock,data,set_,str(cur_thread.name))
                #导入TCP，数据，去重容器，当前线程名

def TCP_threads_receiver(ip='127.0.0.1',port=8888,set_=''):
    server = socketserver.ThreadingTCPServer((ip,port),MyServer)
    ip,port=server.server_address
    server.serve_forever()
#TCP_sender('127.0.0.1',8888,'y')
