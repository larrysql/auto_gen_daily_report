#!/usr/bin/env python
#coding:utf-8:

import datetime,codecs,re,sys,ConfigParser
from operator import itemgetter, attrgetter
sys.path.append('../../utils')
import dateUtil,fileUtil,configUtil,dateUtil,versionListUtil

config = ConfigParser.ConfigParser()
config.read('../../../resource/init.conf')


def getEveryVersionUserAll(data):
    dic = dict()
    f = open(data)
    insert=0
    for i in f.readlines():
        m = re.search(r'全量:',i)
        q = re.search(r'本周:',i)
        i = i.split()
        if m:
            insert=1
        if m or len(i)==0:
            continue
        else:
            if q:
                break
            else:
                if insert==1:
                    if len(i)==1:
                        continue
                    else:
                        dic[i[0]]=i[1]
    f.close()
    return dic

def getBigestVersion(version_list):
    version_num = list()
    for i in version_list:
        i = i.strip()
    big_version_num = int(i.split("_")[-1].split(".")[0]) #取5.0.1中的大版本号
    version_num.append(big_version_num)
    c = max(version_num)     #取当前的主版本号
    return c

def getUserALL(every_verion_user_num_dict):
    n = 0
    for key  in every_verion_user_num_dict.keys():
        n+=int(every_verion_user_num_dict[key])
    return n

def getMainversionNum(version_list,main_version):
    n = 0
    for version in version_list:
        if version.split("_")[-1].split(".")[0] == str(main_version):
            n=n+1
    return n

def getVersionNum(version):
    bai = int(version.split("_")[-1].split(".")[0])
    shi = int(version.split("_")[-1].split(".")[1])
    ge  = int(version.split("_")[-1].split(".")[2])
    return bai*100+shi*10+ge

def compareVersion(version_list_and,version_list_ios):
    a = getVersionNum(and_version_list[-1])
    b = getVersionNum(ios_version_list[-1])
    if a==b:
        return "equel"
    if a>b:
        return "and"
    else:
        return "ios"

#############################################################
today = dateUtil.getToday()
yesterday = dateUtil.getYesterday()
config.set("datafile","date",today)
config.set("datafile","yesterday",yesterday)
config.set("resultfile","date",today)

#安卓和IOS版本配置文件
and_version_file = config.get("datafile","and_version")
ios_version_file = config.get("datafile","ios_version")

version_user_all_datafile_today = config.get("datafile","version_user_all_datafile_today") #提取各个版本用户总数的日志
version_user_all_datafile_yesterday = config.get("datafile","version_user_all_datafile_yesterday") #提取各个版本用户总数的日志
version_update_result = config.get("resultfile","old_version_data") #生成的数据统计结果文件

version_user_today = getEveryVersionUserAll(version_user_all_datafile_today)
version_user_yesterday = getEveryVersionUserAll(version_user_all_datafile_yesterday)

and_version_list = versionListUtil.makeVersionList(and_version_file) #获得安卓版本列表
ios_version_list = versionListUtil.makeVersionList(ios_version_file) #获得IOS版本列表


and_main_version = getBigestVersion(and_version_list) #当前安卓的最大主版本号
ios_main_version = getBigestVersion(ios_version_list) #当前IOS的最大主版本号
max_main_version = max(int(and_main_version),int(ios_main_version))

fileUtil.cleanFile(version_update_result)

f=open(version_update_result,"a")
and_version_list.pop()
ios_version_list.pop()
cycle_num=str(max_main_version)
and_update_all=0
ios_update_all=0

while True:
    if compareVersion(and_version_list[-1],and_version_list[-1]) == "equel":
        if and_version_list[-1].split("_")[-1].split(".")[0] != cycle_num:
            break
        else:
            and_user_today = version_user_today[and_version_list[-1]]
            and_user_yesterday = version_user_yesterday[and_version_list[-1]]
            and_update = int(and_user_yesterday)-int(and_user_today)
            and_update_all+=int(and_update)

            ios_user_today = version_user_today[ios_version_list[-1]]
            ios_user_yesterday = version_user_yesterday[ios_version_list[-1]]
            ios_update = int(ios_user_yesterday)-int(ios_user_today)
            ios_update_all+=int(ios_update)

            update_all = and_update+ios_update_all
            f.write(and_version_list[-1].split("_")[-1]+" "+str(and_update)+" "+str(ios_update)+" "+str(update_all)+"\n")
            and_version_list.pop()
            ios_version_list.pop()
    elif compareVersion(and_version_list[-1],and_version_list[-1]) == "and":
        if and_version_list[-1].split("_")[-1].split(".")[0] != cycle_num:
            break
        else:
            and_user_today = version_user_today[and_version_list[-1]]
            and_user_yesterday = version_user_yesterday[and_version_list[-1]]
            and_update = int(and_user_yesterday)-int(and_user_today)
            and_update_all+=int(and_update)

            update_all = and_update
            f.write(and_version_list[-1].split("_")[-1]+" "+str(and_update)+" - "+str(update_all)+"\n")

            and_version_list.pop()

    else:
        if ios_version_list[-1].split("_")[-1].split(".")[0] != cycle_num:
            break
        else:
            ios_user_today = version_user_today[ios_version_list[-1]]
            ios_user_yesterday = version_user_yesterday[ios_version_list[-1]]
            ios_update = int(ios_user_yesterday)-int(ios_user_today)
            ios_update_all+=int(ios_update)

            update_all = ios_update
            f.write(ios_version_list[-1].split("_")[-1]+" - "+str(ios_update)+" "+str(update_all)+"\n")

            ios_version_list.pop()
#安卓有计算2.x和一个没有版本的号的，将其改变计算出月3.x相加
and2_user_today=0
and2_user_yestersay=0
for key in version_user_today.keys():
    k_list = key.split("_")
    if k_list[-1].split(".")[0]=="2" or k_list[-1]=="":
       and2_user_today=and2_user_today+int(version_user_today[key])

for key in version_user_yesterday.keys():
    k_list = key.split("_")
    if k_list[-1].split(".")[0]=="2" or k_list[-1]=="":
       and2_user_yestersay=and2_user_yestersay+int(version_user_yesterday[key])
and2_update = and2_user_yestersay-and2_user_today

n = max_main_version
while n > 3:
    and_version_user_today=0
    ios_version_user_today=0
    and_version_user_yesterday=0
    ios_version_user_yesterday=0

    n = n-1
    for key in version_user_today.keys():
        if key.split("_")[-1].split(".")[0]==str(n):
            if key.split("_")[-2]=="and":
                and_version_user_today+=int(version_user_today[key])

            else:
                ios_version_user_today+=int(version_user_today[key])

    for key in version_user_yesterday.keys():
        if key.split("_")[-1].split(".")[0]==str(n):
            if key.split("_")[-2]=="and":
                and_version_user_yesterday+=int(version_user_yesterday[key])

            else:
                ios_version_user_yesterday+=int(version_user_yesterday[key])
    if n==3:
        and_update=int(and_version_user_yesterday)-int(and_version_user_today) + and2_update
    else:
        and_update=int(and_version_user_yesterday)-int(and_version_user_today)
    and_update_all+=int(and_update)

    ios_update=int(ios_version_user_yesterday)-int(ios_version_user_today)
    ios_update_all+=int(ios_update)

    update_all=and_update+ios_update

    f=open(version_update_result,"a")
    f.write(str(n)+".x版本"+" "+str(and_update)+" "+str(ios_update)+" "+str(update_all)+"\n")
    f.close()


f = open(version_update_result,"a")
f.write("总计"+" "+str(and_update_all)+" "+str(ios_update_all)+" "+str(and_update_all+ios_update_all)+"\n")
f.close()
