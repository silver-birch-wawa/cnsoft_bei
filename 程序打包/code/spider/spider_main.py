#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 29 16:57:48 2017

@author: wang bei bei
"""
import sys
sys.path.append("..")
import queue,socketserver,re,time,requests
from spider_ip_and_port.TCP_sender import TCP_sender
from spider_ip_and_port.check_proxy import check_proxy
from spider_ip_and_port.receiving_ip_and_port import receiving_ip_and_port

#去重的函数
from de_weight.de_weight import de_weight
#创建driver
from create_driver import Driver
#拓展用函数
from receiver import TCP_receiver
#切换UA用的库
#from fake_useragent import UserAgent
#bs处理超链接
from bs4 import BeautifulSoup
#引进线程锁
thread_elements_num=1
thread_list_num=1
thread_goods_num=1
thread_num=thread_elements_num+thread_list_num+thread_goods_num
#thread_num=4


from lock import semaphore
import threading
lock=threading.Lock()
lock=semaphore(lock,thread_list_num)

spider_ip='127.0.0.1'
remoted_ip='127.0.0.1'


#待装填队列
from Tornado_Browser.parameter import pr,po
#pr=queue.Queue()  存放id
#po=queue.Queue()  存放port
#########杂七杂八的端口##############
ip_sending_port=8880
ip_receiving_port=8870
url_checking_receiving_port=9990
url_checking_sending_port=8770

url_sending_port=url_receiving_port=9000
root_url_receiving_port=9100
#存放去重后的内链url
#url_queue=queue.Queue()
#unrepeated_url_queue=queue.Queue()
waiting_url=queue.Queue()
unrepeated_list_url=queue.Queue()
unrepeated_good_url=queue.Queue()
#########去重容器#########
unrepeated_url_io=0

from url_set import url_set

#######信号量用于判断已接受到相应的ip与port########
signal_ip=0
######存放内链标记#######
inner_href=".com"
##############接受####################
pr_=[]
po_=[]
start_signal=0
###############数据存储对象#################
from redis_module.redis_store import database
d=database()
############## URL填充 ################
def extend_the_url(url):
    if('http'!=url[:4]):
        url='http:'+url
        return url
    else:
        return url
#################单独开一个守候线程#####################
def receiving_ip_and_port_from_server(spider_ip='127.0.0.1',ip_sending_port=8880,pr=0,po=0):
    global signal_ip,inner_href,pr_,po_,start_signal
    while(1):
        try:
            pr_,po_,inner_href=receiving_ip_and_port(spider_ip,ip_sending_port)
        except Exception as e:
            print("sth happended in receiving_ip_and_port():")
            print(e)
        #time.sleep(90)
        try:
            pr_,po_=check_proxy(pr_,po_)
        except Exception as e:
            print(e)
        #time.sleep(90)
        #print("\n----------可以联通的代理----------\n")
        while(pr_.qsize()>0):
            pr.put(pr_.get())
            po.put(po_.get())
        print("\n观察是否为空!!!!!")
        print("共接收到ip:%d个\n"%pr.qsize())
        start_signal=start_signal+1
        #time.sleep(4)
        signal_ip=0
    print('Receiving ip Server is running...')
#一次性使用只是抽取首页的入口地址用用
def receiving_the_root_url_and_handling_them(spider_ip='127.0.0.1',url_sending_port=9000):
    global waiting_url,start_signal
    print("看看能不能跑到这1")
    addr,data=TCP_receiver(spider_ip,url_sending_port)
    data=data.decode("utf-8")
    print(data)
    print("看看能不能跑到这2")
    for i in re.finditer("#.*?#",data):
        url=i.group()[1:-1]
        print("root_url: ",url)
        if(inner_href in url):  #防止非url因素的干扰
            if(de_weight(url_set,url)==0):
                waiting_url.put(url)
    start_signal=start_signal+1
    return True
##如果队列中ip数量较少,则发送请求并修改请求的信号量.
def if_the_ip_is_thirsty(remoted_ip='127.0.0.1',remoted_port=8880,pr=0,t_num=1):
    global signal_ip
    while(1):
        if(pr.qsize()<thread_num+1 and signal_ip==0):
            #lock.wait(t_num)
            print("sending the proxy ip ask..............")
            #time.sleep(4)
            try:
                TCP_sender(remoted_ip,remoted_port,"1111") #向主机请求资源
            except Exception as e:
                print(e)
            #lock.signal(t_num)
            signal_ip=1
            print("\n还有%d个可用ip"%pr.qsize())
##########接受url并填充至队列###########################
#from receiver import receiving_the_unrepeated_url
'''
TCP_sender('127.0.0.1',8880,"1111") #向主机请求资源以开启程序
receiving_ip_and_port(pr,po)             #开启一个守候线程单独给这个函数
'''
#receiving_the_root_url_and_handling_them("127.0.0.1",url_sending_port,url_queue)

#当信号量signal_ip为1时在等待接受ip，所以要想触发ip请求的话要if(signal_ip!=1 and pr.qsize()<thread_num+1)

################检查是否是商品页####################
def check_if_the_page_is_goods_pages(url):
    if("item" in url):
        r=requests.get(url)
        if("加入购物车" in r.text):
            return True
    return False
##################################################
def pick_up_the_price(text):
    #单纯提取数字会跟划去的价格混淆,计算机无法理解促销价以及售价,京东价是什么东西.....所以迫于无奈只能强行一对一匹配
    #淘宝,天猫还有的price有毒别人都是125.84它偏偏来个124.98-238.45
    #利用class中存在price/rmb的特点,一个一个class抽取匹配过去,然后根据相对位置定位具体位置      ￥  ¥
    price_stack=[]
    if("¥" in text):   #京东是¥ 网易严选是¥
        for i in re.findall("¥.*>\d+\.\d+-\d+\.\d+<?",text):
            try:
                if(len(i)<80):
                    print(i)
                    price=re.search("\d+\.\d+-\d+\.\d+",i)
                    if(price!=None):
                        price_stack.append(price.group())
                        print(price)
                        if(len(price_stack)==2):
                            return str(price_stack)[1:-1]
            except Exception as e:
                print("Error in Money 1:  "+e)
        if(len(price_stack)==1):
            return str(price_stack)[1:-1]
        elif(len(price_stack)==0):
            try:
                for i in re.findall("¥.*>\d+\.\d+<?",text):
                    print(i)
                    if(len(i)<80):
                        price=re.search(">\d+\.\d+<",i)
                        if(price!=None):
                            price=price.group()
                            print(price[1:-1])
                            return price[1:-1]
                        else:
                            print("竟然为空？")
            except Exception as e:
                print("Error in Money 2:  "+e)
        try:
            for i in re.findall(">¥.*\d+.*<",text):
                return re.search("\d+\.\d+",i).group()
        except Exception as e:
            print("Error in Money 3:  "+e)
    ##########另一种￥###########
    elif("￥" in text):
        for i in re.findall("￥.*>\d+\.\d+-\d+\.\d+<?",text):
            if(len(i)<80):
                price=re.search("\d+\.\d+-\d+\.\d+",i)
                if(price!=None):
                    price_stack.append(price.group())
                    print(price)
                    if(len(price_stack)==2):
                        return str(price_stack)[1:-1]
        if(len(price_stack)==1):
            return str(price_stack)[1:-1]
        elif(len(price_stack)==0):
            for i in re.findall("￥.*>\d+\.\d+<?",text):
                if(len(i)<80):
                    price=re.search("\d+\.\d+",i)
                    if(price!=None):
                        price=price.group()
                        print(price)
                        return price
                    else:
                        print("竟然为空？")
        for i in re.findall(">￥.*\d+.*<",text):
            return re.search("\d+\.\d+",i).group()

def pick_up_store_name(text,bs4):
    #进入店铺 或者 进店逛逛 的链接跟 店铺名的链接一样.....抓出来链接地址再匹配href中的链接地址就可以了
    #先把html编码进行一下转换
    text=text.replace('&gt;','>')
    text=text.replace('&lt;','<')
    bs4=BeautifulSoup(text)
    try:
        for i in re.findall("<a.*>.*</a>?",text):
            #print(i)
            if('进入店铺' in i or '进店逛逛' in i):
                href=re.search('href="[^"]+"?',i).group()[6:-1]
    except Exception as e:
        print('店铺匹配bug1: ',e)
    try:
        for i in re.findall("<a.*>.*</a>?",text):
            if("店" in i):
                store_name=re.search('[^\W]+店',i).group()
                if(len(store_name)>4):
                    print(store_name)
                    return store_name
    except Exception as e:
        print('店铺匹配bug2: ',e)
    try:
        for i in bs4.find_all('a'):
                if(i.get('href') in href or href in i.get('href')):
                    #print(i.get_text())
                    #print(href)
                    store_name=re.search('[^\s]+',i.get_text()).group()
                    if(len(store_name)>4):
                        #店铺名一般都比较长。。。
                        return store_name
    except Exception as e:
        print('店铺匹配bug3: ',e)
    return ''

def pick_up_the_elements_and_store_in(text):
    global goods_price_class,d
    #text=driver.page_source
    #print("打印页面信息测试一下：",text)
    if("加入购物车" in text):
        bs4=BeautifulSoup(text)
        #print("测试---------------------11111111")  #ok
        try:
            #goods_name=re.findall('[^-]+',driver.title)[0]
            goods_name=re.search("<title>.*</title>?",text).group()[7:-8]
            #print("\n到达11111\n")
            goods_price=pick_up_the_price(text)
            #print("\n到达22222\n")
            store_name=pick_up_store_name(text,bs4)
            #print("\n测试---------------------222222222\n")
            if(goods_price!=None and store_name!=None and goods_name!=None):
                print('\ntitle: \n',goods_name)
                print('\nprice: \n',goods_price)
                print('\nstore name: \n',store_name)
                lock.wait(1)
                d.store(goods_name,goods_price,store_name)
                lock.signal(1)
            else:
                print("\n\n奇怪啊，竟然匹配到了None.....\n\n")
        except Exception as e:
            print("********Bug in picking the elements***********",e)
#高并发的商品信息收割机
def pick_up_elements():
    global unrepeated_good_url,pr,po
    #d=database()
    while(pr.qsize()==0):
        #print("ip 枯竭等待中....")
        time.sleep(1)
        pass
    while(unrepeated_good_url.qsize()==0):
        time.sleep(3)
        print("Goods_URL的时机未到。")
        pass
    #使用的user-agent切换库
    driver=Driver(40)
    while(1):
        while(unrepeated_good_url.qsize()>0):
            url=unrepeated_good_url.get()
            if("#" in url):  #把锚给拉黑
                url_set.add(url)
                continue
            #print("\n\n>>>>>>>>>>>>开始采集商品信息:"+url+"\n\n")
            #if(de_weight(url_set,url)==0):
            url_set.add(url)
            print("\n\n>>>>>>>>>>>>开始采集商品信息:"+url+"\n\n")
            try:
                driver.get(url)
                #print("刷新浏览器成功!")
            except Exception as e:
                print("浏览器刷新页面报错：",e)
            try:
                pick_up_the_elements_and_store_in(driver.page_source)
            except Exception as e:
                print("Error occur in the outter of pick up the elements........",e)

############爬虫的正式抓取阶段#######开启多线程(每个线程)进行抓爬###########
#分为 1.(可能)商品页面链接采集(利用/list这个通用标签) 注意别的网站添加http就可以,但是网易要添加http://you.163.com在前面
#     2.商品信息抓取利用//item(京东,天猫)或者/item(网易)或者//detail(天猫)
class_click_next_page=''
def pick_up_the_page_num(text):
    try:
        page_number=re.search("共.*[0-9]+.*页",text).group()
        page_number=int(re.search("[0-9]+",page_number).group())
    except Exception as e:
        if 'NoneType' in e:
            return 0
        print(e)
        page_number=1
        print('page_number: ',page_number)
    return page_number
def find_click_button(page):
    result=''
    bs4=BeautifulSoup(page)
    for i in bs4.find_all('a'):
        if(re.search('下.*一.*页?',str(i))):
            result=str(i.get('class'))[2:-2]
    print('总页数: ',result)
    return result
def click_next_page(driver,class_click_next_page):
    #global driver,class_click_next_page
    if(class_click_next_page==''):
        try:
            class_click_next_page=find_click_button(driver.page_source)
        except Exception as e:
            print(e)
        print("wait!!!!!!!!!!!:",class_click_next_page)
        driver.find_element_by_class_name(class_click_next_page).click()
    else:
        print("wait!!!!!!!!!!!:",class_click_next_page)
        driver.find_element_by_class_name(class_click_next_page).click()

def good_url_added(url,http):
    global unrepeated_good_url,url_set
    if(de_weight(url_set,url)==0):
        if("http"!=url[:4]):
            url=http+str(url)
        print('\n\n***goods url -> '+url)
        print("\n\n")
        unrepeated_good_url.put(url)

def pick_up_all_the_goods_url(page):
    global unrepeated_good_url,url_set
    bs4=BeautifulSoup(page)
    for i in bs4.find_all("a"):
        #print(i.get('href'))
        try:
            url=i.get('href')
            url=str(url)
            url=extend_the_url(url)
            if(inner_href in url):    # error: argument of type 'NoneType' is not iterable
                if('//item' in url and '#detail' not in url and '163.com' not in url):
                    good_url_added(url,"http:")
                if('/item' in url):
                    good_url_added(url,'http://you.163.com')
                if('//detail' in url and '163.com' not in url):       #淘宝中的detail为重复链接需要去掉
                    good_url_added(url,"http:")
        except Exception as e:
            print('Error in pick_up_all_goods_url:',e)

#单独开一个线程抓取列表中的所有商品页面url
def pick_up_goods_url_in_lists():
    global inner_href,url_set,class_click_next_page,unrepeated_list_url,pr,po
    #为避免IP枯竭而等待
    while(pr.qsize()==0):
        #print("ip 枯竭等待中....")
        time.sleep(1)
        pass
    while(unrepeated_list_url.qsize()==0):
        print("LIST_URL的时机未到。")
        time.sleep(4)
        pass
    #使用的user-agent切换库
    driver=Driver(40)
    while(1):
        while(unrepeated_list_url.qsize()>0):
            url=unrepeated_list_url.get()
            print("开始采集list:%s里面的good_url"%url)
            driver.get(url)
            try:
                page_num=pick_up_the_page_num(driver.page_source)
            except Exception as e:
                pick_up_all_the_goods_url(driver.page_source)  #bug happen here
                print(e)
                continue
            bs4=BeautifulSoup(driver.page_source)
            pick_up_all_the_goods_url(driver.page_source)  #bug happen here
            for i in bs4.find_all('a'):
                try:
                    if(re.search('下.*一.*页?',str(i))):
                        #print("get the page class:",class_click_next_page)
                        for j in range(page_num):
                            click_next_page(driver,class_click_next_page)
                            print("\n开始翻页\n")
                            #bs4=BeautifulSoup(driver.page_source,'lxml')
                            pick_up_all_the_goods_url(driver.page_source)
                        break
                except Exception as e:
                    print(e)

#单独开一个线程处理lists
def pick_up_all_lists_url():
    global inner_href,waiting_url,pr,po,start_signal,remoted_ip,url_checking_sending_port
    url=''
    #为避免IP枯竭而等待
    while(pr.qsize()==0):
        #print("ip 枯竭等待中....")
        time.sleep(1)
        pass
    #使用的user-agent切换库
    while(start_signal<2):  #循环等待开启(root url 获取后才能开跑)
        print("url_list is waiting for start.")
        time.sleep(1)
    driver=Driver(40)
    #print("\n\nstart_signal:%d 为什么你不跑啊??\n\n"%start_signal)
    #time.sleep(4)
    while(waiting_url.qsize()>0):
        url=waiting_url.get()
        #print("getting waiting url-------"+url)
        driver.get(url)
        bs4=BeautifulSoup(driver.page_source)
        for i in bs4.find_all('a'):
            try:
                url=i.get('href')
                if(inner_href in url):
                    url=extend_the_url(url)
                    if(de_weight(url_set,url)==0):
                        if('list' in url):
                            if(inner_href!='163.com' and '163.com' not in url or inner_href=='163.com'):
                                #print("#pick up lists_url: ",url)
                                #lock.wait(1)
                                TCP_sender(remoted_ip,url_checking_sending_port,url)
                                #lock.signal(1)
                                #pick_up_all_lists_url(i.get('href'))
                        else:
                            #lock.wait(1)
                            TCP_sender(remoted_ip,url_checking_sending_port,url)
                            #lock.signal(1)
            except Exception as e:
                print("Error in pick_up_all_lists_url: ",e)

    print("\n\npick_up_all_lists_url()因为堆栈为空正常退出............\n\n")
    print("各个堆栈大小: waiting_url:%d,  unrepeated_list_url:%d,  unrepeated_good_url:%d"%(waiting_url.qsize(),unrepeated_list_url.qsize(),unrepeated_good_url.qsize()))
    time.sleep(10)

##########################接受验证了的url#################################
class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        global unrepeated_good_url,unrepeated_list_url,waiting_url
        conn = self.request
        #cur_thread = threading.current_thread()
        while (1):
            #lock.acquire()
            #print("*************注意：URL接收模块运行正常。")
            #time.sleep(1)
            try:
                data = conn.recv(1024)
                #data=bytes(data).decode("utf-8")   #因为有中文的原因需要转码
            except Exception as e:
                print(e)
                continue
            #lock.release()
            data=str(data)
            if(data!="b''"):
                print("URL接受模块收到 data: "+data)
                if("unrepeated" in data and "\\x" not in data):
# 莫名其妙的中文编码错误...暂时无法解决，所以直接过滤了。
# //search.jd.com/Search?keyword=%E9%BA%A6%E5%AF%8C%E8%BF%AA%E7%8B%97%E7%B2%AE&enc=utf-8&wq=\xe9\xba\xa6\xe5\xaf\x8c\xe8
                    data=data[2:-13]
                    #print(cur_thread.name,"   : ",data)      # 加入到去重的set当中。
                    if('list' in data):
                        print("\n\n-->unrepeated list_url: ",data)
                        unrepeated_list_url.put(data)
                    elif('/item' in data):
                        print("\n\n-->unrepeated good_url: ",data)
                        unrepeated_good_url.put(data)
                    elif('//detail' in data):       #淘宝中的detail为重复链接需要去掉
                        print("\n\n-->unrepeated good_url: ",data)
                        unrepeated_good_url.put(data)
                    else:
                        print("\n\n-->other types url:",data)
                        waiting_url.put(data)
                else:
                    data=data[2:-13]
                    print("put the %s into url_set"%data)
                    url_set.add(data)

def receiving_the_unrepeated_url(remoted_ip='127.0.0.1',url_checking_port=8770):
    global unrepeated_url_queue,unrepeated_list_url,unrepeated_good_url
    server = socketserver.ThreadingTCPServer((remoted_ip,url_checking_port),MyServer)
    ip,port=server.server_address
    server.serve_forever()
#单独开一个线程
#receiving_the_unrepeated_url
##################主函数########################

if __name__ == "__main__":
    '''

    1.先挂起一个ip检测线程。
    if_the_ip_is_thirsty(remoted_ip='127.0.0.1',remoted_port=8880,pr=0,t_num=1)
    2.再挂起一个ip接受进程
    receiving_ip_and_port(spider_ip='127.0.0.1',ip_sending_port=8880,pr=0,po=0)
    3.然后再挂起一个url接受进程

    receiving_the_unrepeated_url(remoted_ip,url_checking_port,url_queue)

    开始run 1.2.3

    4.获取网页入口地址
    receiving_the_root_url_and_handling_them(spider_ip='127.0.0.1',url_sending_port=9000,url_queue=0)
    5.开启一个进程运行scraping函数（发送验证信息）
    ------------
    6.从队列中取出经加工后的url,抓取数据

    question1.怎么在商品页上翻页并且不会翻页翻到最后卡死?
    question2.
    '''
    #############################################################################################
    threads=[]
    #请求ip同时开启ip池监视模块
    t=threading.Thread(target=if_the_ip_is_thirsty,args=(remoted_ip,ip_sending_port,pr,1,))#t_num=1
    threads.append(t)
    #开启ip接受模块
    t=threading.Thread(target=receiving_ip_and_port_from_server,args=(spider_ip,ip_receiving_port,pr,po,))
    threads.append(t)
    #提前开启url接受模块
    t=threading.Thread(target=receiving_the_unrepeated_url,args=(spider_ip,url_checking_receiving_port,))
    threads.append(t)

    #先把goods url爬成功再来搞信息提取

    for i in range(thread_elements_num):
        t=threading.Thread(target=pick_up_elements,args=())
        threads.append(t)

    for i in range(thread_goods_num):
        t=threading.Thread(target=pick_up_goods_url_in_lists,args=())
        threads.append(t)

    for i in range(len(threads)):
        print("start第%d个线程"%i)
        threads[i].start()
    #接收root url
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx:")
    receiving_the_root_url_and_handling_them(spider_ip,root_url_receiving_port)
    print("跑通啦!!!!!!!!!!!!!!!!!!!!!!!")

    #开始爬取并且边爬边发送去重请求。
    for i in range(thread_list_num):
        t=threading.Thread(target=pick_up_all_lists_url,args=())#t_num=1
        threads.append(t)
        t.start()
    for i in range(len(threads)):
        threads[i].join()
    #receiving_the_root_url_and_handling_them(spider_ip=spider_ip,url_sending_port=url_sending_port,url_queue=url_queue)
