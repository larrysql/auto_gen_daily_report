#!/usr/bin/env python
#coding=utf-8

import datetime,codecs,re,sys,ConfigParser
from operator import itemgetter, attrgetter
sys.path.append('../../utils')
import dateUtil,fileUtil,configUtil,versionListUtil

#加载配置文件
config = configUtil.loadConfig()

#从4-0-0report文件获得最新的大版本（5.x）中各小版本的用户总量
def getVersionUserNumber(data):
    #定义一个字典用于存储各个版本的用户总量
    dic = dict()
    f = open(data)
    #定义一个参数用于控制数据的读取，当遇到“当日新增用户数”时将其置为1，循环中会进行判断只有insert=1才会进行数据操作
    insert=0
    for i in f.readlines():
 #       i = i.strip()
        #每行中都要寻找如下字符串
        m = re.search(r'版本用户数',i)
        n = re.search(r'selected',i)
        q = re.search(r'当日新增用户数',i)
        i = i.split()
        #如果该行中有“版本用户数”字符串，则将insert置为1，开始进行数据操作
        if m:
            insert=1
        #如果遇到“版本用户数”，“selected”，或者空行，则跳出本次循环，开始操作下一行
        if m or n or len(i)==0:
            continue
        #如果没有“版本用户数”，“selected”，或者空行的情况，开始进行判断
        else:
            #如果有'当日新增用户数'说明要读取的数据已经操作完，直接跳出循环
            if q:
                break
            #如果没有'老用户登陆数'则判断insert值
            else:
                #如果insert值为1，将版本号作为key，用户总量做为value写入定义好的字典
                if insert==1:
                    dic[i[0]]=i[1]

    f.close()
    return dic
#从4-0-0report文件获得最新的大版本（5.x）中各小版本的当日新增用户数，返回字典
def getTodayAddUser(data):
    dic = dict()
    f = open(data)
    insert=0
    for i in f.readlines():
        i = i.strip()
        m = re.search(r'当日新增用户数',i)
        n = re.search(r'selected',i)
        q = re.search(r'老用户登陆数',i)
        i = i.split()
        if m:
            insert=1
        if m or n or len(i)==0:
            continue
        else:
            if q:
                break
            else:
                if insert==1:
                    dic[i[0]]=i[1]
    f.close()
    return dic

#获取新增用户总量，作为今天的基数
def getNewUserOfNewversionBaseNum(file):
    base_num = list()
    f = open(file)
    for i in f:
        i = i.strip()
        a = i.split(":")
        if a[0]=="and":
            base_num.append(a[1])
        if a[0]=="ios":
            base_num.append(a[1])
    return base_num

######################################################################
#获得今天的日期
today = dateUtil.getToday()
#获得明天的日期
tomorrow = dateUtil.getTomorrow()

#设置配置文件时间
config.set("datafile","date",today)
config.set("resultfile","date",today)
config.set("datafile","tomorrow",tomorrow)

#获得and版本配置文件地址
and_version_file = config.get("datafile","and_version")
#获得ios版本配置文件地址
ios_version_file = config.get("datafile","ios_version")

#获得今天新增用户技术文件地址
newversion_newuser_basenum_config_file_today = config.get("datafile","newversion_base_num_file_today")
#获得明天新增用户基数地址
newversion_newuser_basenum_config_file_tomorrow = config.get("datafile","newversion_base_num_file_tomorrow")
#获得最新版本的新增用户数，和用户总量的配置文件
version_user_datafile = config.get("datafile","version_user_datafile")
#生成的新版本数据存放地址
new_version_add_data_result = config.get("resultfile","latest_version_data")

#生成新版本用户总量字典
user_num_dict = getVersionUserNumber(version_user_datafile)
#生成新版本今天新增用户字典
add_user_num_dict = getTodayAddUser(version_user_datafile)

#生成安卓和ios的版本列表
and_version_list = versionListUtil.makeVersionList(and_version_file)
ios_version_list = versionListUtil.makeVersionList(ios_version_file)

#获取当天的的版本用户基数生成列表
new_version_add_base_num=getNewUserOfNewversionBaseNum(newversion_newuser_basenum_config_file_today)

#安卓最新版本用户总数量（str）
and_newversion_user_all = user_num_dict[and_version_list[-1]]
#ios最新版本用户总量（str）
ios_newversion_user_all = user_num_dict[ios_version_list[-1]]
#最新版本用户总量
newversion_user_all = int(and_newversion_user_all)+int(ios_newversion_user_all)
#安卓最新版本新增用量（今天新增用户+基数）
and_newversion_adduser_today = int(add_user_num_dict.get(and_version_list[-1],"0"))+int(new_version_add_base_num[0])
#安卓最新版本新增用量（今>天新增用户+基数）
ios_newversion_adduser_today = int(add_user_num_dict.get(ios_version_list[-1],"0"))+int(new_version_add_base_num[1])
#最新版本新增用量(int)
newversion_adduser_today = and_newversion_adduser_today+ios_newversion_adduser_today

#安卓今天老版本更新为最新版本的用户数（用户总数-新增用户数）
and_oldversion_user_to_newversion_num=int(and_newversion_user_all)-int(and_newversion_adduser_today)
#ios今天老版本更新为最新版本的用>户数（用户总数-新增用户数）
ios_oldversion_user_to_newversion_num=int(ios_newversion_user_all)-int(ios_newversion_adduser_today)
#今天老版本更新为最新版本的用>户数(int)
oldversion_user_to_newversion_num = and_oldversion_user_to_newversion_num+ios_oldversion_user_to_newversion_num

############先清空新增用户基数配置文件######################
fileUtil.cleanFile(newversion_newuser_basenum_config_file_tomorrow)
f = open(newversion_newuser_basenum_config_file_tomorrow,"w")
f.close()
############将新的基数写入配置文件##########################
f = open(newversion_newuser_basenum_config_file_tomorrow,"a")
f.write("and:"+str(and_newversion_adduser_today)+"\n")
f.write("ios:"+str(ios_newversion_adduser_today)+"\n")
f.close

#######################新建结果文件#######################
fileUtil.cleanFile(new_version_add_data_result)
file = open(new_version_add_data_result,"w")
file.close()

#######################将数据写入结果文件##################
f = open(new_version_add_data_result,"a")
f.write("新注册用户数"+" "+str(and_newversion_adduser_today)+" "+str(ios_newversion_adduser_today)+" "+str(newversion_adduser_today)+"\n")
f.write("老用户更新用户"+" "+str(and_oldversion_user_to_newversion_num)+" "+str(ios_oldversion_user_to_newversion_num)+" "+str(oldversion_user_to_newversion_num)+"\n")
f.write("合计"+" "+and_newversion_user_all+" "+ios_newversion_user_all+" "+str(newversion_user_all)+"\n")
f.close()
