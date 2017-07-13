#!/usr/bin/env python
#coding:utf-8
#auther:王兴伟

import datetime,sys,string

#函数先检测是否有外部参数，如果有外部参数则返回外部参数相对应的日期，如果没有外部参数则返回今天日期
def getToday():
    try: 
        return sys.argv[1]
    except:
        return  datetime.date.today().strftime('%Y%m%d')
#函数先检测是否有外部参数，如果有外部参数则返回外部参数所对应的前一天的日期，如果没有外部参数则返回当前时间
#的前一天的日期
def getYesterday():
    try:
        #将字符串格式化成时间    
        day = datetime.datetime(string.atoi(str(sys.argv[1])[0:4]),string.atoi(str(sys.argv[1])[4:6]),string.atoi(str(sys.argv[1])[6:8]))
        #将时间减去一天的时间间隔，获得前一天的时间
        yesterday = day + datetime.timedelta(days = -1)
        return yesterday.strftime('%Y%m%d')
    except:    
        yesterday = datetime.date.today() - datetime.timedelta(days = 1)
        return yesterday.strftime('%Y%m%d')
#函数先检测是否有外部参数，如果有外部参数则返回外部参数所对应的后一天的日期，如果没有外部参数则返回当前时间
#的后一天的日期
def getTomorrow():
    try:
        #将字符串格式化成时间 
        day = datetime.datetime(string.atoi(str(sys.argv[1])[0:4]),string.atoi(str(sys.argv[1])[4:6]),string.atoi(str(sys.argv[1])[6:8]))
        #将时间加上一天的时间间隔，获得后一天的时间
        tomorrow = day + datetime.timedelta(days = 1)
        return tomorrow.strftime('%Y%m%d')
    except:
        tomorrow = datetime.date.today()+datetime.timedelta(days=1)
        return tomorrow.strftime('%Y%m%d')

#获得月份的函数
def getMonth():
    try:
        return str(sys.argv[1])[0:6]
    except:
        return datetime.date.today().strftime('%Y%m')
#获得上月的函数
def getPreMonth(time):
    try:
        day = datetime.datetime(string.atoi(str(time)[0:4]),string.atoi(str(time)[4:6]),string.atoi('1'))
        time_new = day + datetime.timedelta(days = -1)
        return time_new.strftime('%Y%m')

    except:
        day = datetime.date.today().strftime('%Y%m%d')
        day = datetime.datetime(string.atoi(day[0:4]),string.atoi(day[4:6]),string.atoi('1'))
        time_new = day + datetime.timedelta(days = -1)
        return time_new.strftime('%Y%m')
