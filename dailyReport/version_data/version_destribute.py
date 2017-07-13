#!/usr/bin/env python
#coding:utf-8

import datetime,codecs,re,os,sys,ConfigParser
from operator import itemgetter, attrgetter
sys.path.append('../../utils')
sys.path.append('../user_active')
import dateUtil,fileUtil,configUtil,dateUtil,versionListUtil
from gen_totalNum import *

#加载配置文件
config = configUtil.loadConfig()


def versionNewUser(data):

    dic = dict()
    f = open(data)
    #定义一个参数用于控制数据的读取，当遇到“当日新增用户数”时将其置为1，循环中会进行判断只有insert=1才会进行数据操作
    insert=0
    #开始对文件进行逐行遍历
    for i in f.readlines():
        i = i.strip()
        #每行中都要寻找如下字符串
        m = re.search(r'当日新增用户数',i)
        n = re.search(r'selected',i)
        q = re.search(r'老用户登陆数',i)
        #将该行格式化成列表
        i = i.split()
        #如果该行中有“当日新增用户数”字符串，则将insert置为1，开始进行数据操作
        if m:
            insert=1
        #如果遇到“当日新增用户数”，“selected”，或者空行，则跳出本次循环，开始操作下一行
        if m or n or len(i)==0:
            continue
        #如果没有“当日新增用户数”，“selected”，或者空行的情况，开始进行判断
        else:
            #如果有'老用户登陆数'说明要读取的数据已经操作完，直接跳出循环
            if q:
                break
            #如果没有'老用户登陆数'则判断insert值
            else:
                #如果insert值为1，将版本号作为key，用户总量做为value写入定义好的字典
                if insert==1:
                    dic[i[0]]=i[1]
    f.close()
    return dic

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

def getUserAddALL(datafile,day):
    dict_add_user = {'all':0,'ios':0,'and':0}
    f = open(datafile)
    for i in f.readlines():
        l = i.split()
        if len(l) > 1 and l[-1]==day:
            dict_add_user['all']=dict_add_user['all']+int(l[0])
            if l[1]=="app" or l[-2]=="app_store":
                dict_add_user['ios']=dict_add_user['ios']+int(l[0])
            else:
                dict_add_user['and']=dict_add_user['and']+int(l[0])
    return dict_add_user

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

def getBeforeversionNum(version_list,main_version):
    n = 0
    before_version = main_version - 1
    for version in version_list:
        if version.split("_")[-1].split(".")[0] == str(before_version):
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

##################################################
today = dateUtil.getToday()
month = dateUtil.getMonth()
config.set("datafile","date",today)
config.set("resultfile","date",today)
config.set("resultfile","cur_month",month)

and_version_file = config.get("datafile","and_version")
ios_version_file = config.get("datafile","ios_version")

new_user_add_all_datefile = config.get("datafile","new_user_today")
version_new_user_datafile = config.get("datafile","version_user_datafile")  #提取各个版本新用户的日志
version_user_all_datafile = config.get("datafile","version_user_all_datafile_today") #提取各个版本用户总数的日志
version_distribute_result = config.get("resultfile","version_distr_data")#生成的数据统计结果文件

month_version_proportion = config.get("resultfile","month_version_proportion")

dict_newuser_add_all=getUserAddALL(new_user_add_all_datefile,today)

every_version_new_user = versionNewUser(version_new_user_datafile)  #各个版本的今天的新用户数字典

every_version_user_all = getEveryVersionUserAll(version_user_all_datafile) #各个版本的用户总数字典

user_all=getUserALL(every_version_user_all) #获得用户总数

#生成IOS和and的版本列表
and_version_list = versionListUtil.makeVersionList(and_version_file)
ios_version_list = versionListUtil.makeVersionList(ios_version_file)

and_main_version = getBigestVersion(and_version_list) #当前安卓的最大主版本号
ios_main_version = getBigestVersion(ios_version_list) #当前IOS的最大主版本号
max_main_version = max(int(and_main_version),int(ios_main_version))

fileUtil.cleanFile(version_distribute_result)
and_add_all=0
ios_add_all=0
ios_user=0
and_user=0
biaotou=list()
month_proportion=list()

f=open(version_distribute_result,"a")
cycle_num=str(max_main_version)
while True:
    if compareVersion(and_version_list[-1],and_version_list[-1]) == "equel":
        if and_version_list[-1].split("_")[-1].split(".")[0] != cycle_num:
            break
        else:
            and_add_user = every_version_new_user.get(and_version_list[-1],"0")
            and_add_all+=int(and_add_user)
            ios_add_user = every_version_new_user.get(ios_version_list[-1],"0")
            ios_add_all+=int(ios_add_user)
            add_all = int(and_add_user)+int(ios_add_user)

            and_version_user = every_version_user_all.get(and_version_list[-1],"0")
            and_user+=int(and_version_user)
            ios_version_user = every_version_user_all.get(ios_version_list[-1],"0")
            ios_user+=int(ios_version_user)
            version_all=int(and_version_user)+int(ios_version_user)

            proportion=round(float(float(version_all)*100/float(user_all)),2)
            version=and_version_list[-1].split("_")[-1]
            biaotou.append(version)
            month_proportion.append(str(proportion))
            f.write(and_version_list[-1].split("_")[-1]+" "+and_add_user+" "+ios_add_user+" "+str(add_all)+" "+and_version_user+" "+ios_version_user+" "+str(version_all)+" "+str(proportion)+"\n")
            and_version_list.pop()
            ios_version_list.pop()
    elif compareVersion(and_version_list[-1],and_version_list[-1]) == "and":
        if and_version_list[-1].split("_")[-1].split(".")[0] != cycle_num:
            break
        else:
            and_add_user = every_version_new_user.get(and_version_list[-1],"0")
            and_add_all+=int(and_add_user)
            add_all = and_add_user
            and_version_user = every_version_user_all.get(and_version_list[-1],"0")
            and_user+=int(and_version_user)
            version_all = and_version_user
            proportion=round(float(float(version_all)*100/float(user_all)),2)

            version=and_version_list[-1].split("_")[-1]
            biaotou.append(version)
            month_proportion.append(str(proportion))
            f.write(and_version_list[-1].split("_")[-1]+" "+and_add_user+" -  "+add_all+" "+and_version_user+" - "+version_all+" "+str(proportion)+"\n")
            and_version_list.pop()

    else:
        if ios_version_list[-1].split("_")[-1].split(".")[0] != cycle_num:
            break
        else:
            ios_add_user = every_version_new_user.get(ios_version_list[-1],0)
            ios_add_all+=int(ios_add_user)
            add_all = ios_add_user
            ios_version_user = every_version_user_all.get(ios_version_list[-1],0)
            ios_user+=int(ios_version_user)
            version_all = ios_version_user
            proportion=round(float(float(version_all)*100/float(user_all)),2)

            version=and_version_list[-1].split("_")[-1]
            biaotou.append(version)
            month_proportion.append(str(proportion))

            f.write(ios_version_list[-1].split("_")[-1]+" - "+ios_add_user+" "+str(add_all)+" - "+ios_version_user+" "+str(version_all)+" "+str(proportion)+"\n")
            ios_version_list.pop()


n = max_main_version
ios_versions_user=0
and_versions_user=0
version_list=list()
proportion_list=list()

while n > 4:

    and_version_user=0
    ios_version_user=0
    and_version3_user=0
    ios_version3_user=0

    n = n-1
    version_list.append(str(n)+".x")
    for key in every_version_user_all.keys():
         if key.split("_")[-1].split(".")[0]==str(n):
            if key.split("_")[-2]=="and":
                and_version_user+= int(every_version_user_all[key])
                and_versions_user+=int(and_version_user)
            else:
                ios_version_user+=int(every_version_user_all[key])
                ios_versions_user+=int(ios_version_user)
         if len(key.split("_")[-1])==0:
            if key.split("_")[-2]=="and":
                and_version3_user+= int(every_version_user_all[key])
                and_versions_user+=int(every_version_user_all[key])
            else:
                ios_version3_user+=int(every_version_user_all[key])
                ios_versions_user+=int(every_version_user_all[key])
         else:
            if int(key.split("_")[-1].split(".")[0]) <= 3:
                if key.split("_")[-2]=="and":
                    and_version3_user+=int(every_version_user_all[key])
                    and_versions_user+=int(every_version_user_all[key])
                else:
                    ios_version3_user+=int(every_version_user_all[key])
                    ios_versions_user+=int(every_version_user_all[key])
    version_all=int(and_version_user)+int(ios_version_user)
    proportion=round(float(float(version_all)*100/float(user_all)),2)
    biaotou.append(str(n)+'.x')
    month_proportion.append(str(proportion))
    proportion_list.append(str(proportion))

version3_user_all=int(ios_version3_user)+int(and_version3_user)
proportion=round(float(float(version3_user_all)*100/float(user_all)),2)

biaotou.append('3.x')
version_list.append('3.x')
month_proportion.append(str(proportion))
proportion_list.append(str(proportion))

add_all = dict_newuser_add_all["all"]
versions_and_add = dict_newuser_add_all["and"] - and_add_all
versions_ios_add = dict_newuser_add_all["ios"] - ios_add_all
versions_add_all = versions_and_add + versions_ios_add

versions_user_all = and_versions_user + ios_versions_user

f=open(version_distribute_result,"a")

v = "|".join(version_list)
p = "|".join(proportion_list)
f.write(v+" "+str(versions_and_add)+" "+str(versions_ios_add)+" "+str(versions_add_all)+" "+str(and_versions_user)+" "+str(ios_versions_user)+" "+str(versions_user_all)+" "+p+"\n")

and_all = and_user + and_versions_user
ios_all = ios_user + ios_versions_user
all_user = and_all + ios_all

total_user_num = getTotalUserNum(today)
f.write("合计"+" "+str(dict_newuser_add_all["and"])+" "+str(dict_newuser_add_all["ios"])+" "+str(add_all)+" "+str(and_all)+" "+str(ios_all)+" "+str(total_user_num)+" "+"-"+"\n")


biaotou.append("day")
month_proportion.append(today)
list_proportion=list()
if os.path.isfile(month_version_proportion):
    f = open(month_version_proportion,"r+")
    flist = f.readlines()
    if len(flist[0].split()) <= len(biaotou):
        biaotou.reverse()
        flist[0] = " ".join(biaotou)+"\n"
        f.close()
        f = open(month_version_proportion,"w")
        f.write(flist[0])
        f.close()
    else:
        f = open(month_version_proportion,"w")
        f.write(flist[0])
        f.close()

    l = len(flist)
    n = 1
    while  n<l:
        list_line = flist[n].split()
        if list_line[0]==today:
            continue
        else:
            tuple_line = tuple(list_line)
            list_proportion.append(tuple_line)
        n+= 1
    month_proportion.reverse()
    list_proportion.append(tuple(month_proportion))
    list_proportion = list(set(list_proportion))
    list_proportion = sorted(list_proportion, key=lambda day:day[0],reverse = False)
    f = open(month_version_proportion,"a")
    for i in list_proportion:
        line = list(i)
        f.write(" ".join(line)+"\n")

else:
    f = open(month_version_proportion,"w+")
    biaotou.reverse()
    f.write(" ".join(biaotou)+"\n")
    month_proportion.reverse()
    f.write(" ".join(month_proportion)+"\n")
    f.close()

