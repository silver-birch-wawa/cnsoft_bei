# 项目文件说明书
## 文件结构
```
├─main_server
│  │  draw_picture.py
│  │  ghostdriver.log
│  │  lock.py
│  │  phantomjs.exe
│  │  sender.py
│  │  server_main.py
│  │  __init__.py
│  │
│  ├─de_weight
│  │  │  de_weight.py
│  │  │  __init__.py
│  │  │
│  │  └─__pycache__
│  │          de_weight.cpython-35.pyc
│  │          __init__.cpython-35.pyc
│  │
│  ├─server_ip_and_port
│  │  │  draw_picture.py
│  │  │  lock.py
│  │  │  post_get_proxy.py
│  │  │  sending_ip_and_url.py
│  │  │  TCP_receiver.py
│  │  │  __init__.py
│  │  │
│  │  └─__pycache__
│  │          draw_picture.cpython-35.pyc
│  │          lock.cpython-35.pyc
│  │          post_get_proxy.cpython-35.pyc
│  │          sending_ip_and_url.cpython-35.pyc
│  │          TCP_receiver.cpython-35.pyc
│  │          __init__.cpython-35.pyc
│  │
│  └─__pycache__
│          draw_picture.cpython-35.pyc
│          lock.cpython-35.pyc
│          sender.cpython-35.pyc
│          server_main.cpython-35.pyc
│          temp.cpython-35.pyc
│          __init__.cpython-35.pyc
│
├─redis
│      redis_store.py
│
└─spider
    │  create_driver.py
    │  ghostdriver.log
    │  lock.py
    │  phantomjs.exe
    │  receiver.py
    │  sender.py
    │  spider_main.py
    │  webdriver_change_proxy.py
    │
    ├─de_weight
    │  │  de_weight.py
    │  │  __init__.py
    │  │
    │  └─__pycache__
    │          de_weight.cpython-35.pyc
    │          __init__.cpython-35.pyc
    │
    ├─spider_ip_and_port
    │  │  check_proxy.py
    │  │  lock.py
    │  │  receiver.py
    │  │  receiving_ip_and_port.py
    │  │  TCP_sender.py
    │  │  __init__.py
    │  │
    │  └─__pycache__
    │          check_proxy.cpython-35.pyc
    │          receiving_ip_and_port.cpython-35.pyc
    │          TCP_sender.cpython-35.pyc
    │          __init__.cpython-35.pyc
    │
    └─__pycache__
            create_driver.cpython-35.pyc
            lock.cpython-35.pyc
            receiver.cpython-35.pyc
            webdriver_change_proxy.cpython-35.pyc
```


## 1. redis数据库的存储结构:
* ### 以店铺名为主键,价格与商品名为主键对应键值
* #### goods_name---|--->store_name
#### 　　　　　　　|--->goods_price

---
### >>> 技术细节:
* ### 使用了redis库
* ### 在redis_store.py中打包为database类,通过store方法
* ### 存储goods_name,goods_price,store_name为两个键值对

```
├─redis
│      redis_store.py
```
---
## 2. TCP通讯模块
* ### 实现spider节点与主服务器之间的通讯
* ### 分为IP分发补充与URL分发去重

## >>>IP分发补充:

```
├─spider_ip_and_port
│  │  check_proxy.py
│  │  lock.py
│  │  receiver.py
│  │  receiving_ip_and_port.py
│  │  TCP_sender.py
│  │  __init__.py

├─server_ip_and_port
│  │  draw_picture.py
│  │  lock.py
│  │  post_get_proxy.py
│  │  sending_ip_and_url.py
│  │  TCP_receiver.py
│  │  __init__.py
```
## >>>URL分发还有通讯用到的自己写的库文件
```
    │  TCP_sender.py
    │  receiver.py
    │  sender.py
    │  TCP_receiver.py
```
---
## 3.去重模块:
### >>> 使用python自带的基于红黑树的set,从算法上看复杂度最差为O(nlogn)
```
├─de_weight
│  │  de_weight.py
│  │  __init__.py
│  │
│  └─__pycache__
│          de_weight.cpython-35.pyc
│          __init__.cpython-35.pyc
```
---
## 4.模拟浏览器请求模块:
### >>> 使用selenium库还有phantomJS引擎执行ajax页面上js代码
### >>> 从而加载所有页面信息
```
└─spider
    │  create_driver.py
```
---
### 技术细节:
### >>> Driver类继承webdriver.PhantomJS类
### >>> 有change_proxy,get,page_source等方法
### >>> get函数中内置有触发器,类成员url_ask_times变量会记录请求次数
### >>> 在请求次数超过50次时自动切换代理。
---
## 5.Lock模块:
### >>>为了避免多线程发生死锁,特地加入了带有信号量的线程锁导入为全局变量使用
