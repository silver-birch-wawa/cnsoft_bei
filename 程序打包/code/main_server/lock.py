# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 19:38:04 2017

@author: wang bei bei
"""
import queue
import threading
# empty表示空的进程, full表示忙碌
# queue的设计就是自带锁的,所以很安全,理论上不会死锁

#############33整型信号量##################
#lock信号量为1为空，可以运行程序,0表示有线程已经占用，
#为在函数中修改值将lock信号量改为类中的成员变量
class lock:
    '''
    需要让信号量的加减放在锁前面
    '''
    def __init__(self,lock):
        self.lock=lock
        self.sign=1
    def wait(self,i):
        while(self.sign==0):
            ##print("为避免死锁,No.%d循环等待....."%i)
            if(self.sign==1):
                self.sign=self.sign-1
                self.lock.acquire()
                break
    def signal(self,i):
        #print("No.%d打开锁"%i)
        self.lock.release()
        self.sign=self.sign+1
        
'''
def wait(sig,i,lock):
    while(sig.sign==0):
        sleep(0.05)
        prinit("为避免死锁,No.%d循环等待....."%i)
        if(sig.sign==1):
            break
    sig.sign=sig.sign-1
    lock.acquire()
'''
########记录型信号量###########
class semaphore:
    def __init__(self,lock,queue_length):
        self.lock=lock
        self.thread_num=0  #一个临时变量
        self.sign=1    #信号量1/0
        self.block_list=queue.Queue(queue_length)   #有优先顺序的阻塞队列
    def wait(self,i):  #i是线程的编号
        q=self.block_list
        if(self.sign==0):
            while(self.block_list.empty()==False):
                self.thread_num=self.block_list.get()
                if(i==self.thread_num):
                    break
                self.block_list.put(self.thread_num)
            while(self.sign==0):
                #print("为避免死锁,No.%d循环等待....."%i)
                if(self.sign==1):
                    print("***No.%d 申请资源成功...."%i)
                    self.sign=self.sign-1
                    self.lock.acquire()
                    break
        elif(self.sign==1):
            print("---No.%d 申请资源成功...."%i)
            self.sign=self.sign-1
            self.lock.acquire()
    
    def signal(self,i):
        print("No.%d 释放锁......"%i)
        self.lock.release()
        self.sign=self.sign+1

'''
def wait(sem,i,lock):
    sem.value=sem.value-1
    q=sem.block_list
    if(q.sign==0):
        while(q.empty()==False):
            #消费者非空才可以调用lock
            thread_num=q.get()
            if(i==thread_num):
                break
            q.put(thread_num)
            
        while(q.sign==0):
            q.get()
            #print("为避免死锁,%d循环等待.....")
            if(q.sign==1):
                break
            sleep(0.05)
    elif(q.sign==1):
        q.get()
        q.sign=q.sign-1
        lock.acquire()
'''
#value=6
#sem=semephore(value)

        
        
        
        
        
