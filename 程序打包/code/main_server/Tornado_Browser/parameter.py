# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 16:10:27 2017

@author: wang bei bei
"""
import socket,psutil,json,random
input_url=[""]
set_=set()
goods={}
unrepeated_url_io=[0]
class DATA:
    def __init__(self):
        self.timesly={}
        self.goods={}
        self.GOODS_NAME="None"
        self.STORE_NAME="None"
        self.PRICE=0
        self.IP=""
        self.get_inner_ip()
        #mem=psutil.virtual_memory()
        #self.MEMORY_COST=((mem.total-mem.free)/mem.total)*100
        #self.CPU_COST=psutil.cpu_percent(0)

    def get_inner_ip(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        ipList = socket.gethostbyname_ex(hostname)
        for i in ipList[2]:
            if(i[:3]=="172" or i[:3]=="192" or i[:3]=="10."):
                #print(i)
                self.IP=i
        mem=psutil.virtual_memory()
        self.timesly["MEMORY_COST"]=((mem.total-mem.free)/mem.total)*100
        self.timesly["CPU_COST"]=psutil.cpu_percent(0)
        self.timesly["IP"]=self.IP
        self.timesly["URL"]=unrepeated_url_io[0]

        self.goods["MEMORY_COST"]=self.timesly["MEMORY_COST"]
        self.goods["CPU_COST"]=self.timesly["CPU_COST"]
        self.goods["IP"]=self.IP
        self.goods["URL"]=unrepeated_url_io[0]

    def get_data(self,goods_name,store_name,price):
        self.get_inner_ip()
        self.goods["GOODS_NAME"]=goods_name
        self.goods["STORE_NAME"]=store_name
        self.goods["PRICE"]=price
        self.goods["URL"]=unrepeated_url_io[0]
        #self.get_inner_ip()
        #self.data["MEMORY_COST"]=memory_cost
        #self.data["CPU_COST"]=cpu_cost
        #self.data["IP"]=self.IP

    def timesly_to_String(self):
        #Str=json.dumps(self.goods)
        return str(self.timesly)
    def goods_to_String(self):
        #Str=json.dumps(self.goods)
        return str(self.goods)
data=DATA()
