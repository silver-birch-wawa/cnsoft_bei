# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 21:24:26 2017

@author: wang bei bei


pr,po=post_get_proxy()
pr,po=check_proxy(pr,po)
print("\n----------可以联通的代理----------\n")
print("%s:%s"%(pr,po))
#106.46.136.17:808

"""
import threading
import requests
import queue
#from spider_ip_and_port import receiving_ip_and_port
####线程个数#####
thread_num=150
####合格代理的容器####
proxy=queue.Queue()
proxy_port=queue.Queue()
#############检测代理是否可用#############
def check_proxy(proxy_id,port):
    global proxy,proxy_port
    threads=[]
    for i in range(thread_num):
        t=threading.Thread(target=check,args=(proxy_id,port))
        threads.append(t)
    for i in range(thread_num):
        print("start第%d个线程"%i)
        threads[i].start()
    for i in range(thread_num):
        threads[i].join()
    #proxy_id=proxy
    #port=proxy_port
    #print("可用代理：")
    #print("%s"%proxy_id)
    return proxy,proxy_port  #返回ip与port
#######################################
def check(proxy_id,port):
    global proxy,proxy_port
    headers={
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
            }
    while(proxy_id.qsize()>0):
        ip=proxy_id.get()
        ip_port=port.get() 
        proxies={"http":ip+":"+ip_port}
        #print(proxies)
        try:
            r=requests.get("http://www.baidu.com",proxies= proxies,timeout=4)    
            if(r.status_code==200):
                print(proxies," pass")
                proxy.put(ip)  
                proxy_port.put(ip_port)
            else:
                print("fuck the bug in ip checking.")
        except Exception as e:
            #print(e)            
            #print(proxies,"请求失败！")    
            pass
