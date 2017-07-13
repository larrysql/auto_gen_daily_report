#!/usr/bin/env python
# -*- coding: utf-8 -*-
'获取文件根目录'
import datetime
import os
import sys
sys.path.append('../..')
from utils.dateUtil import getYesterday
from utils.configUtil import getDataPath, getResultPath, getConfigProperty
from utils.fileUtil import writeStr2File

__author__ = '秦欢'

yesterday = getYesterday()
# 将 list 中的字符串类型数字相加
def sumStrNum(x,y):
    return int(x) + int(y)

# 将历史数据写入文件         
def writeHistory2File(path, str1):
    if os.path.exists(path):
        date = str1.split()[0]
        data = str1.split()[1].strip('\r').strip('\n')
        strBuffer = []
        # 假定是新数据
        flag = True
        # 打开该文件
        with open(path,'r') as f:
            # 一行行读取文件中的数据
            for x in f.readlines():
                # 如果重复执行，执行结果跟上次一致，退出方法
                if x.strip('\r').strip('\n') == str1.strip('\r').strip('\n'):
                    return
                # 如果重复执行，且执行结果不一致，则覆盖就数据
                if x.startswith(date) and x.split()[1].strip('\r').strip('\n') != data:
                    flag = False
                    # 用新数据覆盖旧数据
                    x = str1
                strBuffer.append(x)
        # 如果是新数据，也就是说文件中没有该月份的数据，则追加上
        if flag:
            strBuffer.append(str1)
        writeStr2File(path, ''.join(sorted(strBuffer)),'w')  
    # 如果目标文件及文件夹不存在，即每月第一号
    else:
        writeStr2File(path, str1,'w') 

# 用户规模 A4:C4
def cmpTotalNum(Ymd = yesterday):
    # 数据文件路径
    readPath = getDataPath(Ymd)
    # 打开数据文件，并读取文件中数字
    with open('%sdaoda-cnt%s.txt' % (readPath, Ymd), 'r') as f:
        l = [line.split()[0] for line in f.readlines() if not ('COUNT' in line or '-' in line) and len(line.strip()) > 0]
    # 计算'用户总量'
    totalNum = reduce(sumStrNum, l)
    # 待写入文件的'用户总量'数据
    completProgress = str('%.1f'%(float(totalNum) / int(getConfigProperty("scaleActive", "exp_userScale")) * 100)) + '%'
    userScale = getConfigProperty('scaleActive', 'name_userScale') + ' ' + str(totalNum) + ' ' + completProgress 
    # 写入文件
    writePath = getResultPath(Ymd) + 'scaleActive.txt'
    writeStr2File(writePath, userScale + '\n','w')

# 新增用户数    
def cmpNewUserNumToday(Ymd = yesterday): 
    # 数据文件路径
    readPath = getDataPath(Ymd)
    # 打开数据文件，并读取文件中数字
    with open('%squdao-ri-zengliang%s.txt' % (readPath, Ymd), 'r') as f:
        l = [line.split()[0].strip() for line in f.readlines() if (len(line.split()) > 0 and line.split()[-1].strip() == Ymd)]
    totalNum = reduce(sumStrNum, l)
    # 待写入文件的'用户总量'数据
    completProgress = str('%.1f'%(float(totalNum) / int(getConfigProperty("scaleActive", "exp_userAddNumOfToday")) * 100)) + '%'
    newUserNumToday = getConfigProperty('scaleActive', 'name_userAddNumOfToday') + ' ' + str(totalNum) + ' ' + completProgress 
    # 写入文件
    writePath = getResultPath(Ymd) + 'scaleActive.txt'
    writeStr2File(writePath, newUserNumToday + '\n')
    
    writeHistory2File(getResultPath(Ymd[:-2]) + 'dailyIncrement.txt', Ymd + ' ' + str(totalNum) + '\n')
    
# 当月累计新增用户数    
def cmpNewUserNumMonth(Ymd = yesterday): 
    # 数据文件路径
    readPath = getDataPath(Ymd)
    Ym = Ymd[0:6]
    # 打开数据文件，并读取文件中数字
    with open('%squdao-ri-zengliang%s.txt' % (readPath, Ymd), 'r') as f:
        l = [line.split()[0].strip() for line in f.readlines() if (len(line.split()) > 0 and line.split()[-1].strip().startswith(Ym) and int(line.split()[-1].strip()) >= int(Ym + '01') and int(line.split()[-1].strip()) <= int(Ymd))]
    totalNum = reduce(sumStrNum, l)
    # 待写入文件的'用户总量'数据
    completProgress = str('%.1f'%(float(totalNum) / int(getConfigProperty("scaleActive", "exp_userAddNumOfMonth")) * 100)) + '%'
    newUserNumMonth = Ymd[4:6] + getConfigProperty('scaleActive', 'name_userAddNumOfMonth') + ' ' + str(totalNum) + ' ' + completProgress 
    # 写入文件
    writePath = getResultPath(Ymd) + 'scaleActive.txt'
    writeStr2File(writePath, newUserNumMonth + '\n')
    
# 当日活跃用户数    
def cmpActiveUserToday(Ymd = yesterday): 
    # 数据文件路径
    readPath = getDataPath(Ymd)
    # 打开数据文件，并读取文件中数字
    with open('%sact_groupver%s.txt' % (readPath, Ymd), 'r') as f:
        l = [line for line in f.readlines()]
    flag = False
    activList = []
    for x in l:
        if '活跃:' in x:
            flag = True
            continue
        elif '全量:' in x or '本周:' in x or '本月:' in x:
            flag = False
        elif len(x.strip()) == 0:
            continue
        if flag:
            activList.append(x.split()[-1]) 
    
    totalNum = reduce(sumStrNum, activList)
    # 待写入文件的'用户总量'数据
    completProgress = str('%.1f'%(float(totalNum) / int(getConfigProperty("scaleActive", "exp_activeUserOfToday")) * 100)) + '%'
    newUserNumMonth = getConfigProperty('scaleActive', 'name_activeUserOfToday') + ' ' + str(totalNum) + ' ' + completProgress 
    # 写入文件
    writePath = getResultPath(Ymd) + 'scaleActive.txt'
    writeStr2File(writePath, newUserNumMonth + '\n')

# 获取用户总量即B4
def getTotalUserNum(today = yesterday):
    writePath = getResultPath(today) + 'scaleActive.txt'
    with open(writePath, 'r') as f:
        totalUserNum = f.readline().split()[1]
    return totalUserNum
        
# 新增月活、累积活跃用户数、累计活跃度
def activeUserMonth(today = yesterday):      
     
    nowTime = datetime.datetime.strptime(today, "%Y%m%d").date()
    # 数据文件路径
    readPath = getDataPath(today)
    # 打开数据文件，并读取文件中数字
    with open('%stotal_login%s.txt' % (readPath, today), 'r') as f:
        todayNum = f.readline().split()[-1].strip()
     
    if today.endswith('01'):
        yestodayNum = 0
    else:
        yestoday = (nowTime - datetime.timedelta(days=1)).strftime('%Y%m%d')
        with open('%stotal_login%s.txt' % (getDataPath(yestoday), yestoday), 'r') as f:
            yestodayNum = f.readline().split()[-1].strip() 
            
    # 新增月活  
    newActiveUserMonthInt = int(todayNum) - int(yestodayNum) 
    # 新增月活期望值 
    exp_totalActiveUserAddOfMonth = getConfigProperty("scaleActive", "exp_totalActiveUserAddOfMonth")
    # 新增月活目标值 - 新增月活实际值
    diff = int(exp_totalActiveUserAddOfMonth) - newActiveUserMonthInt
    writeHistory2File(getResultPath(today[:-2]) + 'newIncrementDiffrenceTrend.txt', today + ' ' + str(diff) + '\n')
    newActUsrCmpProgress = str('%.1f'%(float(newActiveUserMonthInt) / int(exp_totalActiveUserAddOfMonth) * 100)) + '%'
    newActiveUserNumMonth = getConfigProperty('scaleActive', 'name_totalActiveUserAddOfMonth') + ' ' + str(newActiveUserMonthInt) + ' ' + newActUsrCmpProgress + '\n' 
     
    # X月累计活跃用户数
    # 累计活跃用户期望值
    exp_totalActiveUserOfMonth = int(getConfigProperty("scaleActive", "exp_totalActiveUserOfMonth"))
    diff = exp_totalActiveUserOfMonth - int(todayNum)
    writeHistory2File(getResultPath(today[:-2]) + 'totalIncrementDiffrenceTrend.txt', today + ' ' + str(diff) + '\n')
    totalActiveUserMonthProgress = str('%.1f'%(float(todayNum) / exp_totalActiveUserOfMonth * 100)) + '%'
    totalActiveUserMonth = today[4:6] + getConfigProperty('scaleActive', 'name_totalActiveUserOfMonth') + ' ' + str(todayNum) + ' ' + totalActiveUserMonthProgress + '\n'
    
    # X月累计活跃度 
    activeDegree = str('%.1f%%'%(float(todayNum)/float(getTotalUserNum(today))*100))
    activeDegreeProgress = str('%.1f%%'%(float(activeDegree[:-1])/float(getConfigProperty('scaleActive', 'exp_activeRate')[:-1])*100))
    activeDegreeMonth = today[4:6] + getConfigProperty('scaleActive', 'name_activeRate') + ' ' + activeDegree + ' ' + activeDegreeProgress
    # 写入文件
    writePath = getResultPath(today) + 'scaleActive.txt'
    writeStr2File(writePath, newActiveUserNumMonth + totalActiveUserMonth + activeDegreeMonth +'\n')    
        
def cmpScaleActiveModule(date = yesterday):
    cmpTotalNum(date)
    cmpNewUserNumToday(date)
    cmpNewUserNumMonth(date)
    cmpActiveUserToday(date)              
    activeUserMonth(date)        
        
if __name__ == '__main__':
    if len(sys.argv) > 1: 
        cmpScaleActiveModule(str(sys.argv[1]))
    else:
        cmpScaleActiveModule()  

# cmpScaleActiveModule('20160906')      
        
        