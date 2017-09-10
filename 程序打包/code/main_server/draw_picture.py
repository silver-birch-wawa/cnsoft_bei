# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 23:48:31 2017

@author: wang bei bei
"""
import numpy as np  
import matplotlib  
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig  
from matplotlib.font_manager import FontProperties
def draw_picture(x,y):
    matplotlib.use('Agg')
    #X轴，Y轴数据    
    plt.figure(figsize=(16,8)) #创建绘图对象   
    ax = plt.gca()
    ax.set_aspect(2)
    #折线图中的单位以及标题
    plt.xlabel(u"Time line - t",fontsize=20) #X轴标签  
    plt.ylabel(u"URL I/0 times/s",fontsize=20)  #Y轴标签  
    plt.xticks(range(len(x)), x)    
    plt.plot(x,y,color='r',linestyle='--',marker='o',label='y1 data',linewidth=2.5)   #在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
    #plt.show()  #显示图
    plt.savefig('../1.jpg') 
    plt.close()
'''
y= [1,3,7,11,1,3,4,5,2,1,0] 
x= [0,1,2,3,4,5,6,7,8,9,10] 
draw_picture(x,y)
'''
