# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 16:10:27 2017

@author: wang bei bei
"""
import socket,psutil,queue
input_url=['aaa']
pr=queue.Queue()  #����id
po=queue.Queue()  #����port
class DATA:
    def __init__(self):
        self.data={}
        self.IP=""
        self.MEMORY_COST=0
        self.CPU_COST=0
        self.get_inner_ip()
        mem=psutil.virtual_memory()
        mem_cost=((mem.total-mem.free)/mem.total)*100
        cpu_cost=psutil.cpu_percent(0)
        self.get_data(mem_cost,cpu_cost)
    def get_inner_ip(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        ipList = socket.gethostbyname_ex(hostname)
        for i in ipList[2]:
            if(i[:3]=="172" or i[:3]=="192" or i[:3]=="10."):
                print(i)
                self.IP=i
    def get_data(self,memory_cost,cpu_cost):
        self.data["MEMORY_COST"]=memory_cost
        self.data["CPU_COST"]=cpu_cost
        self.data["IP"]=self.IP
    def to_String(self):
        return str(self.data)
data=DATA()
