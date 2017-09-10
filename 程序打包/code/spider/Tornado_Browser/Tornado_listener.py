#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Tornado_Browser.parameter import input_url,data
import tornado.ioloop
import tornado.web
from tornado import websocket

class DATA(websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")
        
    def check_origin(self, origin):  
        return True  
    
    def on_message(self, message):
        #from parameter import url,data
        global data
        print("接受到数据：",message)
        self.write_message(data.to_String())

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
    (r"/", EchoWebSocket),
])
    url_receiving = tornado.web.Application([
    (r"/url", URL),
])
    application.listen(10008)
    url_receiving.listen(10000)
    tornado.ioloop.IOLoop.instance().start()