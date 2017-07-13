#!/usr/bin/env python
#coding:utf-8

#导入模块
import datetime,codecs,re,sys,ConfigParser
from operator import itemgetter, attrgetter
sys.path.append('../../utils')
import dateUtil,fileUtil,configUtil,dateUtil

#加载配置文件
config = configUtil.loadConfig()


##########################跟据渠道配置文件生成渠道字典“bcmm13:豌豆荚”
def makeQuaodict(file):
    #定义空字典用于存储“bcm13：豌豆荚”这样的键值对
    dic = dict()
    f = open(file)

    #逐行读取渠道字典将"bcm*"作为键，豌豆荚之类的应用渠道作为值写入空字典
    for i in f.readlines():
        n = i.strip('\n').strip('\t').split(':')
        if n[0]=="Web渠道":
            dic[n[-1]]=n[0]
    f.close()
    return dic

#############################生成当天各渠道的和新增用户数对应字典#####################
def versionAddUserDay(qudao_day_add,day,qdict):   #参数为当天各渠道的新增用户文件，哪一天，渠道字典

    #用于存储渠道代码为key，和对应的当天用户增量为value的字典
    dictqudao = dict()

    #用于判断，渠道字典中的渠道代码是否有用户增加，遍历渠道字典键，如果在数据文件中找不到对应的用户增量
    #dictqudao键值就不会增加，len也不会增加，这是就将dictqudao[key]="0"加入dictqudao
    y=1
    #根据渠道字典的key进行遍历，遍历过程中读取qudaodao-ri-zengliang文件，找到当天和key相对应的渠道新增用户
    #并以渠道字典为key生成新的渠道代码对应的用户增量字典
    for key in qdict.keys():
        f = open(qudao_day_add)
        for i in f:
            l = i.split()
            #只有当此行有三个字段，是今天，渠道代码等于渠道字典键值时才写入字典
            if len(l)>2 and key==l[1] and l[-1]==day:
                dictqudao[key] = l[0]
        f.close()
        n = len(dictqudao)
        if n != y:
            dictqudao[key] = "0"
        y=y+1
    return dictqudao

#将结果写入结果文件"new_users.txt"  like  "自有平台 3049 3083 -1.12"
def makeResultfile(resultfile,dicttoday,dictyesterday):
    #调用工具类，创建结果文件
    fileUtil.cleanFile(resultfile)
    #创建列表，将个渠道新增用户情况生成元组存入其中,根据新增用户数量排序
    yuanzulist = list()
    #用于存储今天新增用户总量
    today_add_user_num_all=0
    #用于存储昨天新增用户总量
    yestoday_add_user_num_all=0
    #对今天渠道用户增量字典的key进行遍历
    for key in dicttoday.keys():
        #如果今天的key的value为0则不计算百分率，将今天的新增用户和同key的昨天的新增用户组成集合存入列表
        if dicttoday[key]=="0":
            if dictyesterday[key]=="0":
                continue
            else:
                yuanzulist.append((key,int(dicttoday[key]),int(dictyesterday[key]),'-'))
                #昨天新增用户总数增加
                yestoday_add_user_num_all+=int(dictyesterday[key])
        else:
            #今天新增用户总数增加
            today_add_user_num_all+=int(dicttoday[key])
            #昨天新增用户总数增加
            yestoday_add_user_num_all+=int(dictyesterday[key])
            #计算增长百分率前先将今昨两天的新增用户数变为float类型
            a = float(dicttoday[key])
            b = float(dictyesterday[key])
            #增长百分率为（今天-昨天）/今天
            c = (a-b)/a
            #先将百分率取四位小数，再乘100，使之在表格中直接显示百分数的分子
            c = round(c,4)*100
            c = str(c)
            #将今昨两天的新增用户数和增长百分率组成元组，存入列表
            yuanzulist.append((key,int(a),int(b),c))
    #计算今天昨天新增用户总量的增长百分率
    d = (float(today_add_user_num_all)-float(yestoday_add_user_num_all))/float(today_add_user_num_all)
    d = round(d,4)*100
    #根据今天和昨天新增用户数进行降序排列
    yuanzulist = sorted(yuanzulist, key=itemgetter(1,2),reverse = True)
    #将列表中的元组按顺序写入文件中
    f = open(resultfile,'a')
    for i in yuanzulist:
        f = open(resultfile,'a')
        if len(i)==3:
            a = i[1]
            b = i[2]
            f.write(i[0]+" "+str(a)+" "+str(b)+"\n")
        else:
            a = i[1]
            b = i[2]
            f.write(i[0]+" "+str(a)+" "+str(b)+" "+i[3]+"\n")
    #将最后一行合计写入文件
    f.write("合计"+" "+str(today_add_user_num_all)+" "+str(yestoday_add_user_num_all)+" "+str(d)+"\n")
#####定义变量###################################

#获取今天的日期
today = dateUtil.getToday()
#获取昨天的日期
yesterday = dateUtil.getYesterday()
#将配置文件中datafile部分的日期设为今天
config.set("datafile","date",today)
#将配置文件中datafile部分的昨天设为yesterday
config.set("datafile","yesterday",yesterday)
#将配置文件中resultfile部分的日期设为今天
config.set("resultfile","date",today)
#获取处理的渠道日增量文件路径qudao-ri-zengliang
qudao_ri_zengliang_datafile_today = config.get("datafile","new_user_today")
#获取处理昨天的渠道日增量文件路径qudao-ri-zengliang
qudao_ri_zengliang_datafile_yesterday = config.get("datafile","new_user_yesterday")
#获取渠道编号字典配置文件路径
qudaodictfile = config.get("datafile","qudao_dict")
#今天渠道新增用户数结果存放的地址
web_qudao_adduser_resultfiletoday = config.get("resultfile","web_new_user")

#根据渠道字典文件生成渠道字典
qudaodict = makeQuaodict(qudaodictfile)


#生成今天每个渠道新增用户数字典
today_qudao_adduser_dict = versionAddUserDay(qudao_ri_zengliang_datafile_today,today,qudaodict)
#生成昨天每个渠道新增用户数字典
yesterday_qudao_adduser_dict = versionAddUserDay(qudao_ri_zengliang_datafile_yesterday,yesterday,qudaodict)


#将个渠道的今天新增用户数，昨天新增用户数以及增长百分率写入结果文件供主程序调用
makeResultfile(web_qudao_adduser_resultfiletoday,today_qudao_adduser_dict,yesterday_qudao_adduser_dict)

