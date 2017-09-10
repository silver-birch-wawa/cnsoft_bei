#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 17:15:00 2017

@author: wang bei bei
"""

#from sender import TCP_sender
#用于ip与port的TCP传输的函数
from server_ip_and_port.post_get_proxy import post_get_proxy
from server_ip_and_port.sending_ip_and_url import no_retry_sending_ip_and_url,sending_ip_and_url
from server_ip_and_port.TCP_sender import TCP_sender
#from server_ip_and_port.TCP_receiver import TCP_threads_receiver
from server_ip_and_port.TCP_receiver import receiver_with_string_compare
#from server_ip_and_port.TCP_receiver import *

from selenium import webdriver
#用于去重的函数，重复返回-1，不重复返回0
#from de_weight.de_weight import de_weight

#import time
#import queue
#import requests
import socketserver
import re,queue,time
url_queue=queue.Queue()

from bs4 import BeautifulSoup
####################################
# 端口列表
ip_sending_port=8870
ip_receiving_port=8880

url_checking_sending_port=9990
url_checking_receiving_port=8770
url_sending_port=9000

root_url_sending_port=9100


from url_set import set_

#####################################
#引进线程锁
thread_num=1
import threading
from lock import lock
#做内链的全局变量
inner_href=''
#remoted_ip="127.0.0.1"
Lock=threading.Lock()
lock=lock(Lock)

### 计算吞吐量 ###
#unrepeated_url_io=0
import sys
sys.path.append("..")
from Tornado_Browser.parameter import unrepeated_url_io,input_url
from tolnado_module import run_tolnado

def extend_the_url(url):
    if('http'!=url[:4]):
        url='http:'+url
        return url
    else:
        return url
#################生成吞吐量表####################
'''
def create_picture():
    global unrepeated_url_io,unrepeated_url_io_stack
    y=[0,1,2,3,4,5]
    for i in range(len(y)):
        unrepeated_url_io_stack.append(0)
    pre=unrepeated_url_io
    while(1):
        time.sleep(1)
        print("画图程序正在运行,当前的计数为: ",unrepeated_url_io)
        for i in range(1,len(y)):
            unrepeated_url_io_stack[i-1]=unrepeated_url_io_stack[i]
        unrepeated_url_io_stack[len(y)-1]=unrepeated_url_io-pre
        draw_picture(unrepeated_url_io_stack,y)
        pre=unrepeated_url_io
'''
################main#################
def waiting_and_sending_ip_and_port(remoted_ip='127.0.0.1',ip_receiver_port=8880,inner_href=''):
    while(1):
        r=receiver_with_string_compare(remoted_ip,ip_receiver_port,"1111")  #1111 is 验证用的字符串,报文中出现1111则发送ip
        if(r=="ok"):
            #print("\n\n\n&spider is receiving the ip and port\n")
            proxy_ip,proxy_port,ppp=post_get_proxy()
            sending_ip_and_url(remoted_ip,ip_sending_port,proxy_ip,proxy_port,inner_href)
###########获取url并且分配任务到人################
def get_url_and_post_them(remoted_ip='127.0.0.1',url_sending_port=9100,url='',spider_ip=[]):
    #区分内外链tmail.com与jd.com
    #print("你有没有在跑啊？？？？")
    global unrepeated_url_io
    stack=set()
    q=[]
    t_num=1
    for i in range(len(spider_ip)):
        q.append("#")
    global inner_href
    print("url: ",url)
    print(type(url))
    inner_href=re.search("\.[^.]*\.com",url).group()[1:]
    driver=webdriver.PhantomJS()
    driver.get(url)
    bs4=BeautifulSoup(driver.page_source)
    for i in bs4.find_all("a"):
        try:
            href=i["href"]
            #判断是不是内链
            if(inner_href in href):
            #判断是不是缺少http头然后补上
                if("http" not in href[:4]):
                    href="http:"+href
                    print("sending root url:",href)
                    set_.add(href)
                    stack.add(href)
        except Exception as e:
            print("在拼装的时候出了点问题： ",e)
    i=1
    while(len(stack)>0):
        if(int(i/len(spider_ip))==1):#确定url分发的对象,均匀分配
            q[i-1]=q[i-1]+stack.pop()+'#'
            i=1
        else:
            q[i-1]=q[i-1]+stack.pop()+'#'
            i=i+1
    for i in range(len(spider_ip)):
        try:
            try:
                #lock.wait(t_num)
                unrepeated_url_io[0]=unrepeated_url_io[0]+1
                TCP_sender(spider_ip[i],root_url_sending_port,q[i])
                #lock.signal(t_num)
                print("root url 发送成功")
            except Exception as e:
                #lock.signal(t_num)
                print("Error in root url sending: ",e)
        except Exception as e:
            print(e)
##########################(因为跨文件共享变量的问题暂时这么处理(后来解决了，但懒得改了)##########################################
def processing_the_url(data):
    global set_,url_queue
    #global unrepeated_url_io
    if data in set_:
        q=data+"  repeated"
        #lock.wait(t_num)
        #print("接受到重复的url: ",q)
        url_queue.put(q)
        """
        try:
            conn.sendall(q.encode())
        except Exception as e:
            print(e)
        """
        #lock.signal(t_num)
    else:
        q=data+"  unrepeated"
        #print("接受到未重复的url: ",q)
        #print('\n吞吐量计数: ',unrepeated_url_io,'\n')
        #lock.wait(t_num)
        set_.add(data)
        url_queue.put(q)
        """
        try:
            conn.sendall(q.encode())
        except Exception as e:
            print(e)
        """
class MyServer(socketserver.BaseRequestHandler):
    '''
    def __init__(self,client_address,,set_):
        self.set_=set_
        socketserver.BaseRequestHandler.__init__(ip,port)
    '''
    def __init__(self, request,client_address,server):
        global set_
        socketserver.BaseRequestHandler.__init__(self,request,client_address,server)
    def handle(self):
        global unrepeated_url_io,set_
        #去重用的set还有接受用的队列
        conn = self.request
        try:
            while (1):
                #print("start listening.")
                try:
                    data = conn.recv(1024)
                    #data=data.decode("utf-8")
                except Exception as e:
                    if('主机'in str(e)):  #对方切断连接后会不断报错,所以要掐掉这种报错。
                        break
                    else:
                        print("无关紧要的bug: ",e)
                        continue
                data=str(data)
                #cur_thread = threading.current_thread()
                #print("******data:",str(data))
                time.sleep(1)
                if(data!="b''"):
                    data=str(data)[2:-1]
                    data=extend_the_url(data)
                    unrepeated_url_io[0]=unrepeated_url_io[0]+1
                    print("\n当前吞吐量为:%d\n"%unrepeated_url_io[0])
                    #print(cur_thread.name,"  :",data)
                    processing_the_url(data)
                    #导入TCP，数据，去重容器，当前线程名
                    #conn,lock,data,t_num
        except Exception as e:
                print(e)

def TCP_threads_receiver(ip='127.0.0.1',port=8888):
    server = socketserver.ThreadingTCPServer((ip,port),MyServer)
    ip,port=server.server_address
    server.serve_forever()
    #print("注意一下这里,说不定没启动守候进程....")

############获取并检测url是否重复(要开多线程反馈)###################使用开挂的socketserver接受并塞入队列然后返回
def check_the_url_is_repeated(receiving_ip="127.0.0.1",receiving_port=8770,t_num=1):
    TCP_threads_receiver(receiving_ip,receiving_port)

def url_queue_sending(spider_ip):
    global url_queue,url_checking_sending_port
    i=0
    length=len(spider_ip)
    while(1):
        if(url_queue.qsize()>0):
            url=url_queue.get()
            print("发送url: ",url)
            try:
                TCP_sender(spider_ip[i%length],url_checking_sending_port,url)
            except Exception as e:
                print(e)
            i=i+1
############################
if __name__ == "__main__":
    #global root_url_sending_port
    spider_ip=["127.0.0.1"]
    print("输入入口地址:      请严格按https://www.jd.com/这样的标准输入,谢谢。")
    #get_url_and_post_them('http://3c.tmall.com/?acm=lb-zebra-148799-667863.1003.8.708026&amp;scm=1003.8.lb-zebra-148799-667863.ITEM_14561662186585_708026&amp;go=digt')
    """
    input_url=""
    input_url=input()
    """
    threads=[]
    local_ip='127.0.0.1'
    t1=threading.Thread(target=run_tolnado,args=())
    #threads.append(t)
    t1.start()

    while(input_url[0]==""):
        #print("waiting for entering....")
        continue
    get_url_and_post_them(local_ip,root_url_sending_port,input_url[0],spider_ip)

    t=threading.Thread(target=waiting_and_sending_ip_and_port,args=(local_ip,ip_receiving_port,inner_href,))
    threads.append(t)

    t=threading.Thread(target=check_the_url_is_repeated,args=(local_ip,url_checking_receiving_port,1,))
    threads.append(t)

    t=threading.Thread(target=url_queue_sending,args=(spider_ip,))
    threads.append(t)

    for i in range(len(threads)):
        print("start第%d个线程"%i)
        threads[i].start()
    threads.append(t1)
    for i in range(len(threads)):
        print("start第%d个线程"%i)
        threads[i].join()
    '''
    spider_ip=["127.0.0.1"]
    get_url_and_post_them(remoted_ip,url_sending_port,'https://www.jd.com/',spider_ip)
    '''
