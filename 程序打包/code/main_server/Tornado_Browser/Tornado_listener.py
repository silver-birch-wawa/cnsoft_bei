#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tornado_Browser.parameter import input_url,data,DATA
import tornado.ioloop
import tornado.web
from tornado import websocket
import socket,psutil

class DATA(websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def check_origin(self, origin):
        return True

    def on_message(self, message):
        #from parameter import url,data
        global data
        try:
            #print("接受到数据：",message)
            #print(data.goods_to_String())
            #self.write_message(data.to_String())
            #print("data.GOODS_NAME",data.data["GOODS_NAME"])
            if(data.goods["GOODS_NAME"]!="None"):
                data.get_inner_ip()
                #print(data.goods_to_String())
                self.write_message(data.goods_to_String())
                #data.data["CPU_COST"]="None"
                data.goods["GOODS_NAME"]="None"
                #data.data["MEMORY_COST"]="None"
                #data.data["PRICE"]="None"
                #data.data["STORE_NAME"]="None"
            else:
                data.get_inner_ip()
                #print(data.timesly_to_String())
                self.write_message(data.timesly_to_String())
        except Exception as e:
            print(e)
    def on_close(self):
        print("WebSocket closed")

###############################################################
class URL(websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def check_origin(self, origin):
        return True

    def on_message(self, message):
        #from parameter import url,data
        global input_url
        print("url is: ",message)
        input_url[0]=message
        self.write_message(u"郑老板，您好,我已经收到url：" + message)

    def on_close(self):
        print("WebSocket closed")

if __name__ == "__main__":
    application = tornado.web.Application([
    (r"/", DATA),
])
    url_receiving = tornado.web.Application([
    (r"/url", URL),
])
    application.listen(10008)
    url_receiving.listen(10000)
    tornado.ioloop.IOLoop.instance().start()
