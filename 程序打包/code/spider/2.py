from lock import semaphore
import threading,time
lock=threading.Lock()
lock=semaphore(lock,4)


def thirsty(i):
    while(1):
        lock.wait(1)
        print(i)
        time.sleep(0.1)
        lock.signal(1)
threads=[]
for i in range(4):
    t=threading.Thread(target=thirsty,args=(i,))
    threads.append(t)
for i in range(len(threads)):
    threads[i].start()  
for i in range(len(threads)):
    threads[i].join()  