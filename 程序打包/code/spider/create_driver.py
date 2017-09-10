from selenium import webdriver
from fake_useragent import UserAgent
#将port与ip的队列深拷贝给Driver对象
from Tornado_Browser.parameter import pr,po
import time

class Driver(webdriver.PhantomJS):
    def __init__(self,largest_ask_times):
        #设置最大相应次数
        global pr,po
        try:
            ua=UserAgent()
        except Exception as e:
            print(e)
            ua=UserAgent()
        self.pr=pr
        self.po=po
        self.ua=ua
        self.largest_ask_times=largest_ask_times
        #设置已经相应次数
        self.url_ask_times=0
        self.page_source=''
        self.driver=self.create_driver(pr.get(),po.get())
    def page_source(self):
        return self.driver.page_source
    def get(self,url):
        #time.sleep(10)
        self.url_ask_times=self.url_ask_times+1
        self.driver.get(url)
        self.page_source=self.driver.page_source
        if(self.url_ask_times==self.largest_ask_times):
            self.url_ask_times=0
            while(self.pr.qsize()==0):
                pass
            ip=self.pr.get()
            port=self.po.get()
            self.change_proxy(ip,port)
    def change_proxy(self,ip,port):
        script = "phantom.setProxy('{ip}', {port})".format(ip=ip, port=port)
        self.driver.command_executor._commands['EXECUTE_PHANTOM_SCRIPT'] = ('POST', '/session/$sessionId/phantom/execute')
        self.driver.execute('EXECUTE_PHANTOM_SCRIPT', {'script': script, 'args': []})
    def create_driver(self,pr,po):
        try:
            UA=self.ua.chrome
        except Exception as e:
            print(e)
        service_args=[]
        service_args.append("--load-images=no")
        #拒绝加载图片
        service_args.append("--disk-cache=yes")
        #开启缓存
        service_args.append("--ignore-ssl-errors=true")
        #忽略https错误
        service_args.append('--proxy=%s:%s'%(pr,po))
        service_args.append('--proxy-type=http')
        #dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap={}
        dcap["phantomjs.page.settings.userAgent"] = (UA)
        #driver=webdriver.PhantomJS(service_args=service_args,desired_capabilities=dcap)
        #driver.implicitly_wait(65)
        
        #driver=webdriver.PhantomJS(service_args=service_args,desired_capabilities=dcap)
        #driver=webdriver.Chrome(service_args=service_args,desired_capabilities=dcap)
        try:
            #driver=webdriver.Firefox(service_args=service_args,desired_capabilities=dcap)
            driver=webdriver.Chrome(service_args=service_args,desired_capabilities=dcap)
            #driver=webdriver.PhantomJS(service_args=service_args,desired_capabilities=dcap)
        except Exception as e:
            print("浏览器bug: ",e)
        return driver

    def __del__(self):
        print("抱歉，您的浏览器已退出。")
        self.driver.quit()
#可用代理:
'''
49.83.9.100:808
139.224.237.33:8888
175.170.189.223:80
125.124.227.95:8118
110.73.4.46:8123
116.255.153.137:8082
116.226.90.12:808
'''
'''
ua=UserAgent()
driver=Driver(ua.chrome,'175.170.189.223',80,30)
driver.change_proxy('49.83.9.100',808)
driver.get('http://1212.ip138.com/ic.asp')
print('1:',driver.page_source)
driver.get('http://httpbin.org/headers')
print()
print('2',driver.page_source)
#driver.__del__()
'''
