#coding:utf-8
import datetime
import ConfigParser
import sys,os
sys.path.append('../../../utils/')
from toolUtil import *

if len(sys.argv) ==1:
    pre_day = get_date_fmt('pre_day')
else:
    pre_day = sys.argv[1]
#读取配置文件
cf = ConfigParser.ConfigParser()
init_path = "../../../../resource/init.conf"
cf.read(init_path)

cf.set('path','date',pre_day)
data_file = cf.get("path", "data_path") + '/'  + 'RI' + pre_day + '.txt'
#print data_file
cf.set('resultfile','date',pre_day)
result_file = cf.get("resultfile","perf_mon_login_succ")

data_dir = cf.get("path", "data_path")
result_dir = '/'.join(result_file.split('/')[:-1])

#检查目录是否存在，如果不存在则创建
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

#开始处理数据
pre_pre_day = get_delta_day(pre_day,1)
d_all_ver_cur_login_way = get_all_ver_login_stat(pre_day,init_path) #当天所版本登陆信息
d_latest_ver_cur_login_way = get_latest_ver_login_stat(pre_day,init_path) #当天最新版本登陆信息
d_all_ver_pre_login_way = get_all_ver_login_stat(pre_pre_day,init_path) #昨天所版本登陆信息
d_latest_ver_pre_login_way = get_latest_ver_login_stat(pre_pre_day,init_path) #昨天最新版本登陆信息

cur_lastest_ver_no = get_lastest_ver_no(pre_day,init_path) #当天最新版本号
pre_lastest_ver_no = get_lastest_ver_no(pre_pre_day,init_path) #昨天最新版本号
#if cur_lastest_ver_no <> pre_lastest_ver_no:
    #print '今日版本与昨日版本不同',cur_lastest_ver_no,pre_lastest_ver_no
#else:
#    print '版本未发生变化',cur_lastest_ver_no,pre_lastest_ver_no
#print '昨日登录统计-------------------------'
#print '所有版本--------'
#for k,v in d_all_ver_pre_login_way.items():
#    print k,v
#print '最新版本--------',get_lastest_ver_no(pre_day,init_path)
#for k,v in d_latest_ver_pre_login_way.items():
#    print k,v
#print '今日登录统计-------------------------'
#for k,v in d_all_ver_cur_login_way.items():
#    print k,v
#print '最新版本--------',get_lastest_ver_no(pre_pre_day,init_path)
#for k,v in d_latest_ver_cur_login_way.items():
#    print k,v
#------------所有版本当日及昨日登陆次数统计
#今日动态密码登录次数及成功次数
all_ver_cur_day_dynamic_pass_cnt = d_all_ver_cur_login_way['动态密码登录次数']
all_ver_cur_day_dynamic_pass_succ_cnt = d_all_ver_cur_login_way['动态密码登录成功次数']
latest_ver_cur_day_dynamic_pass_cnt = get_latest_ver_type_login_stat('动态密码登录次数',d_latest_ver_cur_login_way)
latest_ver_cur_day_dynamic_pass_succ_cnt = get_latest_ver_type_login_stat('动态密码登录成功次数',d_latest_ver_cur_login_way)
#print 'latest_ver_cur_day_dynamic_pass_cnt=',latest_ver_cur_day_dynamic_pass_cnt
#print 'latest_ver_cur_day_dynamic_pass_succ_cnt=',latest_ver_cur_day_dynamic_pass_succ_cnt
#昨日动态密码登录次数及成功次数
all_ver_pre_day_dynamic_pass_cnt = d_all_ver_pre_login_way['动态密码登录次数']
all_ver_pre_day_dynamic_pass_succ_cnt = d_all_ver_pre_login_way['动态密码登录成功次数']
latest_ver_pre_day_dynamic_pass_cnt = get_latest_ver_type_login_stat('动态密码登录次数',d_latest_ver_pre_login_way)
latest_ver_pre_day_dynamic_pass_succ_cnt = get_latest_ver_type_login_stat('动态密码登录成功次数',d_latest_ver_pre_login_way)
#print 'latest_ver_pre_day_dynamic_pass_cnt=',latest_ver_pre_day_dynamic_pass_cnt
#print 'latest_ver_pre_day_dynamic_pass_succ_cnt=',latest_ver_pre_day_dynamic_pass_succ_cnt
#今日网站密码登录次数及成功次数
all_ver_cur_day_website_pass_cnt = d_all_ver_cur_login_way['网站密码登录次数']
all_ver_cur_day_website_pass_succ_cnt = d_all_ver_cur_login_way['网站密码登录成功次数']
latest_ver_cur_day_website_pass_cnt = get_latest_ver_type_login_stat('网站密码登录次数',d_latest_ver_cur_login_way)
latest_ver_cur_day_website_pass_succ_cnt = get_latest_ver_type_login_stat('网站密码登录成功次数',d_latest_ver_cur_login_way)
#print 'latest_ver_cur_day_website_pass_cnt=',latest_ver_cur_day_website_pass_cnt
#print 'latest_ver_cur_day_website_pass_succ_cnt=',latest_ver_cur_day_website_pass_succ_cnt

#昨日网站密码登录次数及成功次数
all_ver_pre_day_website_pass_cnt =  d_all_ver_pre_login_way['网站密码登录次数']
all_ver_pre_day_website_pass_succ_cnt = d_all_ver_pre_login_way['网站密码登录成功次数']
latest_ver_pre_day_website_pass_cnt =  get_latest_ver_type_login_stat('网站密码登录次数',d_latest_ver_pre_login_way)
latest_ver_pre_day_website_pass_succ_cnt = get_latest_ver_type_login_stat('网站密码登录成功次数',d_latest_ver_pre_login_way)
#print 'latest_ver_pre_day_website_pass_cnt=',latest_ver_pre_day_website_pass_cnt
#print 'latest_ver_pre_day_website_pass_succ_cnt=',latest_ver_pre_day_website_pass_succ_cnt

#今日服务密码登录次数及成功次数
all_ver_cur_day_service_pass_cnt = d_all_ver_cur_login_way['服务密码登录次数']
all_ver_cur_day_service_pass_succ_cnt  =d_all_ver_cur_login_way['服务密码登录成功次数']

#昨日服务密码登录次数及成功次数
all_ver_pre_day_service_pass_cnt = d_all_ver_pre_login_way['服务密码登录次数']
all_ver_pre_day_service_pass_succ_cnt = d_all_ver_pre_login_way['服务密码登录成功次数']

#今日静默登录次数及成功次数
all_ver_cur_day_slient_pass_cnt = d_all_ver_cur_login_way['静默登录次数']
all_ver_cur_day_slient_pass_succ_cnt = d_all_ver_cur_login_way['静默登录成功次数']

#昨日静默登录次数及成功次数
all_ver_pre_day_slient_pass_cnt = d_all_ver_pre_login_way['静默登录次数']
all_ver_pre_day_slient_pass_succ_cnt = d_all_ver_pre_login_way['静默登录成功次数']

#当日登录总次数
all_ver_cur_day_login_sum = all_ver_cur_day_dynamic_pass_cnt + all_ver_cur_day_website_pass_cnt + all_ver_cur_day_service_pass_cnt + all_ver_cur_day_slient_pass_cnt
latest_ver_cur_day_login_sum = latest_ver_cur_day_dynamic_pass_cnt + latest_ver_cur_day_website_pass_cnt

#当日登陆成功总次数
all_ver_cur_day_login_succ_sum = all_ver_cur_day_dynamic_pass_succ_cnt + all_ver_cur_day_website_pass_succ_cnt + all_ver_cur_day_service_pass_succ_cnt + all_ver_cur_day_slient_pass_succ_cnt
latest_ver_cur_day_login_succ_sum = latest_ver_cur_day_dynamic_pass_succ_cnt + latest_ver_cur_day_website_pass_succ_cnt

#昨日登录总次数
all_ver_pre_day_login_sum = all_ver_pre_day_dynamic_pass_cnt + all_ver_pre_day_website_pass_cnt + all_ver_pre_day_service_pass_cnt + all_ver_pre_day_slient_pass_cnt
latest_ver_pre_day_login_sum = latest_ver_pre_day_dynamic_pass_cnt + latest_ver_pre_day_website_pass_cnt

#昨日登陆成功总次数
all_ver_pre_day_login_succ_sum = all_ver_pre_day_dynamic_pass_succ_cnt + all_ver_pre_day_website_pass_succ_cnt + all_ver_pre_day_service_pass_succ_cnt + all_ver_pre_day_slient_pass_succ_cnt
latest_ver_pre_day_login_succ_sum = latest_ver_pre_day_dynamic_pass_succ_cnt + latest_ver_pre_day_website_pass_succ_cnt
#print 'all_ver_pre_day_slient_pass_cnt=',all_ver_pre_day_slient_pass_cnt
#print 'all_ver_pre_day_slient_pass_succ_cnt=',all_ver_pre_day_slient_pass_succ_cnt
#print 'all_ver_cur_day_login_sum=',all_ver_cur_day_login_sum
#print 'all_ver_pre_day_login_sum=',all_ver_pre_day_login_sum

#本月登录总次数
d_all_ver_cur_month_stat = get_all_ver_cur_month_stat(pre_day,init_path)
d_latest_ver_cur_month_stat = get_latest_ver_cur_month_stat(pre_day,cur_lastest_ver_no,init_path)
#print '本月所有版本登陆总次数------'
#for k,v in  d_all_ver_cur_month_stat.items():
#    print k,v

#print '本月最新版本登陆总次数------'
#for k,v in d_latest_ver_cur_month_stat.items():
#    print k,v

######################################开始生成结果数据并写入到文件#######################################################
l_result = []
#1.总体
###################################总体-----登录次数#########################################
#(1)所有版本
#今日和昨日登录次数
all_today,all_yestoday = all_ver_cur_day_login_sum,all_ver_pre_day_login_sum
#inc_pct增长率
if all_yestoday>0:
    all_inc_pct = round(float(all_today-all_yestoday)/float(all_yestoday)*100,2)
else:
    all_inc_pct = '--'
#本月累计
all_cur_month_sum = d_all_ver_cur_month_stat['本月累计登录次数']
#print all_today,all_yestoday,all_inc_pct,all_cur_month_sum
#(2)最新版本
#今日和昨日登录次数
latest_today,latest_yestoday = latest_ver_cur_day_login_sum,latest_ver_pre_day_login_sum
#增长率
if latest_yestoday>0:
    latest_inc_pct = round(float(latest_today-latest_yestoday)/float(latest_yestoday)*100,2)
else:
    latest_inc_pct = '--'
#本月累计
latest_cur_month_sum = d_latest_ver_cur_month_stat['本月累计登录次数']
#print latest_today,latest_yestoday,latest_inc_pct,latest_cur_month_sum
str1 = '\t'.join(['总体','登录次数',str(all_today),str(all_yestoday),str(all_inc_pct)+'%',str(all_cur_month_sum),str(latest_today),str(latest_yestoday),str(latest_inc_pct)+'%',str(latest_cur_month_sum)])
l_result.append(str1)
##################################总体----登录成功率#####################################
#(2)所有版本登录成功率
#今日和昨日登录成功率
if all_ver_cur_day_login_sum > 0:
    all_today_succ_pct = round(float(all_ver_cur_day_login_succ_sum)/float(all_ver_cur_day_login_sum)*100,2)
else:
    all_today_succ_pct = 0
if all_ver_pre_day_login_sum>0:
    all_yestoday_succ_pct = round(float(all_ver_pre_day_login_succ_sum)/float(all_ver_pre_day_login_sum)*100,2)
else:
    all_yestoday_succ_pct = 0
#增长率
if all_yestoday_succ_pct> 0:
    all_inc_pct = round((all_today_succ_pct-all_yestoday_succ_pct)*100/all_yestoday_succ_pct,2)
else:
    all_inc_pct = 0
#本月累计登录成功率
all_cur_month_succ_cnt = d_all_ver_cur_month_stat['本月累计登录成功次数']
all_cur_month_cnt = d_all_ver_cur_month_stat['本月累计登录次数']
if all_cur_month_cnt > 0:
    all_cur_month_succ_pct = round(float(all_cur_month_succ_cnt)*100/float(all_cur_month_cnt),2)
else:
    all_cur_month_succ_pct = 0
######################
#最新版本登录成功率
#今日和昨日登录成功率
if latest_ver_cur_day_login_sum>0:
    latest_today_succ_pct = round(float(latest_ver_cur_day_login_succ_sum)*100/float(latest_ver_cur_day_login_sum),2)
else:
    latest_today_succ_pct = 0
if latest_ver_pre_day_login_sum>0:
    latest_yestoday_succ_pct = round(float(latest_ver_pre_day_login_succ_sum)*100/float(latest_ver_pre_day_login_sum),2)
else:
    latest_yestoday_succ_pct = 0
#增长率:
if latest_yestoday_succ_pct>0:
    latest_inc_pct = round(float(latest_today_succ_pct - latest_yestoday_succ_pct)*100/float(latest_yestoday_succ_pct),2)
else:
    latest_inc_pct = 0
#本月累计登录成功率
latest_cur_month_succ_cnt = d_latest_ver_cur_month_stat['本月累计登录成功次数']
latest_cur_month_cnt = d_latest_ver_cur_month_stat['本月累计登录次数']
if latest_cur_month_cnt > 0:
    latest_cur_month_succ_pct = round(float(latest_cur_month_succ_cnt)*100/float(latest_cur_month_cnt),2)
else:
    latest_cur_month_succ_pct = 0
#print all_today_succ_pct,all_yestoday_succ_pct,all_inc_pct,all_cur_month_succ_pct,latest_today_succ_pct,latest_yestoday_succ_pct,latest_inc_pct,latest_cur_month_succ_pct
str2 = '\t'.join(['总体','登录成功率',str(all_today_succ_pct)+'%',str(all_yestoday_succ_pct)+'%',str(all_inc_pct)+'%',str(all_cur_month_succ_pct)+'%',str(latest_today_succ_pct)+'%',str(latest_yestoday_succ_pct)+'%',str(latest_inc_pct)+'%',str(latest_cur_month_succ_pct)+'%'])
l_result.append(str2)
###############################短信验证码(动态密码)-----次数占比#########################################
#所有版本次数占比
if all_ver_cur_day_login_sum>0:
    all_ver_cur_login_pct = round(float(all_ver_cur_day_dynamic_pass_cnt)*100/float(all_ver_cur_day_login_sum),2)
else:
    all_ver_cur_login_pct = 0
if all_ver_pre_day_login_sum>0:
    all_ver_pre_login_pct =round(float(all_ver_pre_day_dynamic_pass_cnt)*100/float(all_ver_pre_day_login_sum),2)
else:
    all_ver_pre_login_pct = 0
#增长率
if all_ver_pre_login_pct>0:
    all_ver_dynamic_pass_inc_pct = round((float(all_ver_cur_login_pct)-float(all_ver_pre_login_pct))*100/float(all_ver_pre_login_pct),2)
else:
    all_ver_dynamic_pass_inc_pct = 0
#本月累计短信登录次数占比
all_ver_cur_month_dynamic_pass_login_cnt = d_all_ver_cur_month_stat['动态密码登录次数']
all_ver_cur_month_login_cnt = d_all_ver_cur_month_stat['本月累计登录次数']
if all_ver_cur_month_login_cnt>0:
    all_ver_cur_month_dynamic_pass_login_pct = round(float(all_ver_cur_month_dynamic_pass_login_cnt)*100/float(all_ver_cur_month_login_cnt),2)
else:
    all_ver_cur_month_dynamic_pass_login_pct = 0
#最新版本次数占比
if latest_ver_cur_day_login_sum > 0:
    latest_ver_cur_login_pct = round(float(latest_ver_cur_day_dynamic_pass_cnt)*100/float(latest_ver_cur_day_login_sum),2)
else:
    latest_ver_cur_login_pct = 0
if latest_ver_pre_day_login_sum >0:
    latest_ver_pre_login_pct = round(float(latest_ver_pre_day_dynamic_pass_cnt)*100/float(latest_ver_pre_day_login_sum),2)
else:
    latest_ver_pre_login_pct = 0
#增长率
if latest_ver_pre_login_pct>0:
    latest_ver_dynamic_pass_inc_pct = round((float(latest_ver_cur_login_pct)-float(latest_ver_pre_login_pct))*100/float(latest_ver_pre_login_pct),2)
else:
    latest_ver_dynamic_pass_inc_pct = 0
#本月累计短信登录次数占比
latest_ver_cur_month_dynamic_pass_login_cnt = d_latest_ver_cur_month_stat['动态密码登录次数']
latest_ver_cur_month_login_cnt = d_latest_ver_cur_month_stat['本月累计登录次数']
if latest_ver_cur_month_login_cnt > 0:
    latest_ver_cur_month_dynamic_pass_login_pct = round(float(latest_ver_cur_month_dynamic_pass_login_cnt)*100/float(latest_ver_cur_month_login_cnt),2)
else:
    latest_ver_cur_month_dynamic_pass_login_pct = 0
#print all_ver_cur_login_pct,all_ver_pre_login_pct,all_ver_dynamic_pass_inc_pct,all_ver_cur_month_dynamic_pass_login_pct,latest_ver_cur_login_pct,latest_ver_pre_login_pct,latest_ver_dynamic_pass_inc_pct,latest_ver_cur_month_dynamic_pass_login_pct

str3 = '\t'.join(['短信验证码方式','次数占比',str(all_ver_cur_login_pct)+'%',str(all_ver_pre_login_pct)+'%',str(all_ver_dynamic_pass_inc_pct)+'%',str(all_ver_cur_month_dynamic_pass_login_pct)+'%',str(latest_ver_cur_login_pct)+'%',str(latest_ver_pre_login_pct)+'%',str(latest_ver_dynamic_pass_inc_pct)+'%',str(latest_ver_cur_month_dynamic_pass_login_pct)+'%'])

l_result.append(str3)

######################################短信验证码方式----登录成功率###################################################################
#所有版本登录成功率
all_ver_cur_dynamic_pass_login_succ_pct = int(d_all_ver_cur_login_way['动态密码登录成功率'].strip('%'))
all_ver_pre_dynamic_pass_login_succ_pct = int(d_all_ver_pre_login_way['动态密码登录成功率'].strip('%'))
if all_ver_pre_dynamic_pass_login_succ_pct>0:
    all_ver_dynamic_pass_login_inc_pct = round((float(all_ver_cur_dynamic_pass_login_succ_pct)-float(all_ver_pre_dynamic_pass_login_succ_pct))*100/float(all_ver_pre_dynamic_pass_login_succ_pct),2)
else:
    all_ver_dynamic_pass_login_inc_pct = 0
all_ver_dynamic_pass_cur_month_login_succ_cnt = d_all_ver_cur_month_stat['动态密码登录成功次数']
all_ver_dynamic_pass_cur_month_login_cnt = d_all_ver_cur_month_stat['动态密码登录次数']
if all_ver_dynamic_pass_cur_month_login_cnt>0:
    all_ver_dynamic_pass_cur_month_login_succ_pct = round(float(all_ver_dynamic_pass_cur_month_login_succ_cnt)*100/float(all_ver_dynamic_pass_cur_month_login_cnt),2)
else:
    all_ver_dynamic_pass_cur_month_login_succ_pct = 0
#最新版本登录成功率
latest_ver_cur_dynamic_pass_login_succ_pct = int(get_latest_ver_type_login_stat('动态密码登录成功率',d_latest_ver_cur_login_way).strip('%'))
latest_ver_pre_dynamic_pass_login_succ_pct = int(get_latest_ver_type_login_stat('动态密码登录成功率',d_latest_ver_pre_login_way).strip('%'))
if latest_ver_pre_dynamic_pass_login_succ_pct>0:
    latest_ver_dynamic_pass_login_inc_pct = round((float(latest_ver_cur_dynamic_pass_login_succ_pct)-float(latest_ver_pre_dynamic_pass_login_succ_pct))*100/float(latest_ver_pre_dynamic_pass_login_succ_pct),2)
else:
    latest_ver_dynamic_pass_login_inc_pct = 0
latest_ver_dynamic_pass_cur_month_login_succ_cnt =  d_latest_ver_cur_month_stat['动态密码登录成功次数']
latest_ver_dynamic_pass_cur_month_login_cnt = d_latest_ver_cur_month_stat['动态密码登录次数']
if latest_ver_dynamic_pass_cur_month_login_cnt>0:
    latest_ver_dynamic_pass_cur_month_login_succ_pct = round(float(latest_ver_dynamic_pass_cur_month_login_succ_cnt)*100/float(latest_ver_dynamic_pass_cur_month_login_cnt),2)
else:
    latest_ver_dynamic_pass_cur_month_login_succ_pct = 0
#print all_ver_cur_dynamic_pass_login_succ_pct,all_ver_pre_dynamic_pass_login_succ_pct,all_ver_dynamic_pass_login_inc_pct,all_ver_dynamic_pass_cur_month_login_succ_pct,latest_ver_cur_dynamic_pass_login_succ_pct,latest_ver_pre_dynamic_pass_login_succ_pct,latest_ver_dynamic_pass_login_inc_pct,latest_ver_dynamic_pass_cur_month_login_succ_pct
str4 = '\t'.join(['短信验证码方式','登录成功率',str(all_ver_cur_dynamic_pass_login_succ_pct)+'%',str(all_ver_pre_dynamic_pass_login_succ_pct)+'%',str(all_ver_dynamic_pass_login_inc_pct)+'%',str(all_ver_dynamic_pass_cur_month_login_succ_pct)+'%',str(latest_ver_cur_dynamic_pass_login_succ_pct)+'%',str(latest_ver_pre_dynamic_pass_login_succ_pct)+'%',str(latest_ver_dynamic_pass_login_inc_pct)+'%',str(latest_ver_dynamic_pass_cur_month_login_succ_pct)+'%'])
l_result.append(str4)

################################统一密码登陆方式(网站密码)------次数占比##########################################################
#所有版本次数占比
if all_ver_cur_day_login_sum>0:
    all_ver_cur_login_pct = round(float(all_ver_cur_day_website_pass_cnt)*100/float(all_ver_cur_day_login_sum),2)
else:
    all_ver_cur_login_pct = 0

if all_ver_pre_day_login_sum>0:
    all_ver_pre_login_pct =round(float(all_ver_pre_day_website_pass_cnt)*100/float(all_ver_pre_day_login_sum),2)
else:
    all_ver_pre_login_pct = 0
#增长率
if all_ver_pre_login_pct>0:
    all_ver_website_pass_inc_pct = round((float(all_ver_cur_login_pct)-float(all_ver_pre_login_pct))*100/float(all_ver_pre_login_pct),2)
else:
    all_ver_dynamic_pass_inc_pct = 0
#本月累计网站密码登录次数占比
all_ver_cur_month_website_pass_login_cnt = d_all_ver_cur_month_stat['网站密码登录次数']
all_ver_cur_month_login_cnt = d_all_ver_cur_month_stat['本月累计登录次数']
if all_ver_cur_month_login_cnt>0:
    all_ver_cur_month_website_pass_login_pct = round(float(all_ver_cur_month_website_pass_login_cnt)*100/float(all_ver_cur_month_login_cnt),2)
else:
    all_ver_cur_month_website_pass_login_pct = 0
#最新版本次数占比
if latest_ver_cur_day_login_sum > 0:
    latest_ver_cur_login_pct = round(float(latest_ver_cur_day_website_pass_cnt)*100/float(latest_ver_cur_day_login_sum),2)
else:
    latest_ver_cur_login_pct = 0

if latest_ver_pre_day_login_sum >0:
    latest_ver_pre_login_pct = round(float(latest_ver_pre_day_website_pass_cnt)*100/float(latest_ver_pre_day_login_sum),2)
else:
    latest_ver_pre_login_pct = 0
#增长率
if latest_ver_pre_login_pct>0:
    latest_ver_website_pass_inc_pct = round((float(latest_ver_cur_login_pct)-float(latest_ver_pre_login_pct))*100/float(latest_ver_pre_login_pct),2)
else:
    latest_ver_website_pass_inc_pct = 0
#本月累计网站密码登录次数占比
latest_ver_cur_month_website_pass_login_cnt = d_latest_ver_cur_month_stat['网站密码登录次数']
latest_ver_cur_month_login_cnt = d_latest_ver_cur_month_stat['本月累计登录次数']

if latest_ver_cur_month_login_cnt > 0:
    latest_ver_cur_month_website_pass_login_pct = round(float(latest_ver_cur_month_website_pass_login_cnt)*100/float(latest_ver_cur_month_login_cnt),2)
else:
    latest_ver_cur_month_website_pass_login_pct = 0
#print all_ver_cur_login_pct, all_ver_pre_login_pct,all_ver_website_pass_inc_pct,all_ver_cur_month_website_pass_login_pct,latest_ver_cur_login_pct,latest_ver_pre_login_pct,latest_ver_website_pass_inc_pct,latest_ver_cur_month_website_pass_login_pct
str5 = '\t'.join(['统一密码登陆方式','次数占比',str(all_ver_cur_login_pct)+'%',str(all_ver_pre_login_pct)+'%',str(all_ver_website_pass_inc_pct)+'%',str(all_ver_cur_month_website_pass_login_pct)+'%',str(latest_ver_cur_login_pct)+'%',str(latest_ver_pre_login_pct)+'%',str(latest_ver_website_pass_inc_pct)+'%',str(latest_ver_cur_month_website_pass_login_pct)+'%'])

l_result.append(str5)
################################统一密码登陆方式(网站密码)------登陆成功率##########################################################
#所有版本登录成功率
all_ver_cur_website_pass_login_succ_pct = int(d_all_ver_cur_login_way['网站密码登录成功率'].strip('%'))
all_ver_pre_website_pass_login_succ_pct = int(d_all_ver_pre_login_way['网站密码登录成功率'].strip('%'))
if all_ver_pre_website_pass_login_succ_pct>0:
    all_ver_website_pass_login_inc_pct = round((float(all_ver_cur_website_pass_login_succ_pct)-float(all_ver_pre_website_pass_login_succ_pct))*100/float(all_ver_pre_website_pass_login_succ_pct),2)
else:
   all_ver_pre_website_pass_login_succ_pct = 0

all_ver_website_pass_cur_month_login_succ_cnt = d_all_ver_cur_month_stat['网站密码登录成功次数']
all_ver_website_pass_cur_month_login_cnt = d_all_ver_cur_month_stat['网站密码登录次数']
if all_ver_website_pass_cur_month_login_cnt>0:
    all_ver_website_pass_cur_month_login_succ_pct = round(float(all_ver_website_pass_cur_month_login_succ_cnt)*100/float(all_ver_website_pass_cur_month_login_cnt),2)
else:
    all_ver_website_pass_cur_month_login_succ_pct = 0
#最新版本登录成功率
latest_ver_cur_website_pass_login_succ_pct = int(get_latest_ver_type_login_stat('网站密码登录成功率',d_latest_ver_cur_login_way).strip('%'))
latest_ver_pre_website_pass_login_succ_pct = int(get_latest_ver_type_login_stat('网站密码登录成功率',d_latest_ver_pre_login_way).strip('%'))

if latest_ver_pre_website_pass_login_succ_pct>0:
    latest_ver_website_pass_login_inc_pct = round((float(latest_ver_cur_website_pass_login_succ_pct)-float(latest_ver_pre_website_pass_login_succ_pct))*100/float(latest_ver_pre_website_pass_login_succ_pct),2)
else:
    latest_ver_website_pass_login_inc_pct = 0

latest_ver_website_pass_cur_month_login_succ_cnt =  d_latest_ver_cur_month_stat['网站密码登录成功次数']
latest_ver_website_pass_cur_month_login_cnt = d_latest_ver_cur_month_stat['网站密码登录次数']

if latest_ver_website_pass_cur_month_login_cnt>0:
    latest_ver_website_pass_cur_month_login_succ_pct = round(float(latest_ver_website_pass_cur_month_login_succ_cnt)*100/float(latest_ver_website_pass_cur_month_login_cnt),2)
else:
    latest_ver_website_pass_cur_month_login_succ_pct = 0

#print all_ver_cur_website_pass_login_succ_pct,all_ver_pre_website_pass_login_succ_pct,all_ver_website_pass_login_inc_pct,all_ver_website_pass_cur_month_login_succ_pct,latest_ver_cur_website_pass_login_succ_pct,latest_ver_pre_website_pass_login_succ_pct,latest_ver_website_pass_login_inc_pct,latest_ver_website_pass_cur_month_login_succ_pct

str6 = '\t'.join(['统一密码登陆方式','登陆成功率',str(all_ver_cur_website_pass_login_succ_pct)+'%',str(all_ver_pre_website_pass_login_succ_pct)+'%',str(all_ver_website_pass_login_inc_pct)+'%',str(all_ver_website_pass_cur_month_login_succ_pct)+'%',str(latest_ver_cur_website_pass_login_succ_pct)+'%',str(latest_ver_pre_website_pass_login_succ_pct)+'%',str(latest_ver_website_pass_login_inc_pct)+'%',str(latest_ver_website_pass_cur_month_login_succ_pct)+'%'])
l_result.append(str6)
#######################################客服密码方式(服务密码)----次数占比############################################################
#所有版本次数占比
if all_ver_cur_day_login_sum>0:
    all_ver_cur_login_pct = round(float(all_ver_cur_day_service_pass_cnt)*100/float(all_ver_cur_day_login_sum),2)
else:
    all_ver_cur_login_pct = 0

if all_ver_pre_day_login_sum>0:
    all_ver_pre_login_pct =round(float(all_ver_pre_day_service_pass_cnt)*100/float(all_ver_pre_day_login_sum),2)
else:
    all_ver_pre_login_pct = 0
#增长率
if all_ver_pre_login_pct>0:
    all_ver_service_pass_inc_pct = round((float(all_ver_cur_login_pct)-float(all_ver_pre_login_pct))*100/float(all_ver_pre_login_pct),2)
else:
    all_ver_dynamic_pass_inc_pct = 0
#本月累计客服密码登录次数占比
all_ver_cur_month_service_pass_login_cnt = d_all_ver_cur_month_stat['服务密码登录次数']
all_ver_cur_month_login_cnt = d_all_ver_cur_month_stat['本月累计登录次数']
if all_ver_cur_month_login_cnt>0:
    all_ver_cur_month_service_pass_login_pct = round(float(all_ver_cur_month_service_pass_login_cnt)*100/float(all_ver_cur_month_login_cnt),2)
else:
    all_ver_cur_month_service_pass_login_pct = 0

#print all_ver_cur_login_pct,all_ver_pre_login_pct,all_ver_service_pass_inc_pct,all_ver_cur_month_service_pass_login_pct
str7 = '\t'.join(['客服密码登陆方式','次数占比',str(all_ver_cur_login_pct)+'%',str(all_ver_pre_login_pct)+'%',str(all_ver_service_pass_inc_pct)+'%',str(all_ver_cur_month_service_pass_login_pct)+'%','-','-','-','-'])

l_result.append(str7)
######################################客服密码方式(服务密码)----登陆成功率#########################################################
#所有版本登录成功率
all_ver_cur_service_pass_login_succ_pct = int(d_all_ver_cur_login_way['服务密码登录成功率'].strip('%'))
all_ver_pre_service_pass_login_succ_pct = int(d_all_ver_pre_login_way['服务密码登录成功率'].strip('%'))
if all_ver_pre_service_pass_login_succ_pct>0:
    all_ver_service_pass_login_inc_pct = round((float(all_ver_cur_service_pass_login_succ_pct)-float(all_ver_pre_service_pass_login_succ_pct))*100/float(all_ver_pre_service_pass_login_succ_pct),2)
else:
   all_ver_pre_service_pass_login_succ_pct = 0

all_ver_service_pass_cur_month_login_succ_cnt = d_all_ver_cur_month_stat['服务密码登录成功次数']
all_ver_service_pass_cur_month_login_cnt = d_all_ver_cur_month_stat['服务密码登录次数']
if all_ver_service_pass_cur_month_login_cnt>0:
    all_ver_service_pass_cur_month_login_succ_pct = round(float(all_ver_service_pass_cur_month_login_succ_cnt)*100/float(all_ver_service_pass_cur_month_login_cnt),2)
else:
    all_ver_service_pass_cur_month_login_succ_pct = 0
#print all_ver_cur_service_pass_login_succ_pct,all_ver_pre_service_pass_login_succ_pct,all_ver_service_pass_login_inc_pct,all_ver_service_pass_cur_month_login_succ_pct

str8 = '\t'.join(['客服密码登陆方式','登陆成功率',str(all_ver_cur_service_pass_login_succ_pct)+'%',str(all_ver_pre_service_pass_login_succ_pct)+'%',str(all_ver_service_pass_login_inc_pct)+'%',str(all_ver_service_pass_cur_month_login_succ_pct)+'%','-','-','-','-'])

l_result.append(str8)
#######################################静默登陆方式(静默登陆)----次数占比############################################################
#所有版本次数占比
if all_ver_cur_day_login_sum>0:
    all_ver_cur_login_pct = round(float(all_ver_cur_day_slient_pass_cnt)*100/float(all_ver_cur_day_login_sum),2)
else:
    all_ver_cur_login_pct = 0

if all_ver_pre_day_login_sum>0:
    all_ver_pre_login_pct =round(float(all_ver_pre_day_slient_pass_cnt)*100/float(all_ver_pre_day_login_sum),2)
else:
    all_ver_pre_login_pct = 0
#增长率
if all_ver_pre_login_pct>0:
    all_ver_slient_pass_inc_pct = round((float(all_ver_cur_login_pct)-float(all_ver_pre_login_pct))*100/float(all_ver_pre_login_pct),2)
else:
    all_ver_dynamic_pass_inc_pct = 0
#本月累计客服密码登录次数占比
all_ver_cur_month_slient_pass_login_cnt = d_all_ver_cur_month_stat['静默登录次数']
all_ver_cur_month_login_cnt = d_all_ver_cur_month_stat['本月累计登录次数']
if all_ver_cur_month_login_cnt>0:
    all_ver_cur_month_slient_pass_login_pct = round(float(all_ver_cur_month_slient_pass_login_cnt)*100/float(all_ver_cur_month_login_cnt),2)
else:
    all_ver_cur_month_slient_pass_login_pct = 0

#print all_ver_cur_login_pct,all_ver_pre_login_pct,all_ver_slient_pass_inc_pct,all_ver_cur_month_slient_pass_login_pct
str9 = '\t'.join(['静默登陆方式','次数占比',str(all_ver_cur_login_pct)+'%',str(all_ver_pre_login_pct)+'%',str(all_ver_slient_pass_inc_pct)+'%',str(all_ver_cur_month_slient_pass_login_pct)+'%','-','-','-','-'])

l_result.append(str9)
#####################################静默登陆方式(静默登陆)----登陆成功率#####################################################    #
#所有版本登录成功率
all_ver_cur_slient_pass_login_succ_pct = int(d_all_ver_cur_login_way['静默登录成功率'].strip('%'))
all_ver_pre_slient_pass_login_succ_pct = int(d_all_ver_pre_login_way['静默登录成功率'].strip('%'))
if all_ver_pre_slient_pass_login_succ_pct>0:
    all_ver_slient_pass_login_inc_pct = round((float(all_ver_cur_slient_pass_login_succ_pct)-float(all_ver_pre_slient_pass_login_succ_pct))*100/float(all_ver_pre_slient_pass_login_succ_pct),2)
else:
   all_ver_pre_slient_pass_login_succ_pct = 0

all_ver_slient_pass_cur_month_login_succ_cnt = d_all_ver_cur_month_stat['静默登录成功次数']
all_ver_slient_pass_cur_month_login_cnt = d_all_ver_cur_month_stat['静默登录次数']
#print '静默登录成功次数',all_ver_slient_pass_cur_month_login_succ_cnt
#print '静默登录次数',all_ver_slient_pass_cur_month_login_cnt
if all_ver_slient_pass_cur_month_login_cnt>0:
    all_ver_slient_pass_cur_month_login_succ_pct = round(float(all_ver_slient_pass_cur_month_login_succ_cnt)*100/float(all_ver_slient_pass_cur_month_login_cnt),2)
else:
    all_ver_slient_pass_cur_month_login_succ_pct = 0
#print all_ver_cur_slient_pass_login_succ_pct,all_ver_pre_slient_pass_login_succ_pct,all_ver_slient_pass_login_inc_pct,all_ver_service_pass_cur_month_login_succ_pct

str10 = '\t'.join(['静默登陆方式','登陆成功率',str(all_ver_cur_slient_pass_login_succ_pct)+'%',str(all_ver_pre_slient_pass_login_succ_pct)+'%',str(all_ver_slient_pass_login_inc_pct)+'%',str(all_ver_slient_pass_cur_month_login_succ_pct)+'%','-','-','-','-'])

l_result.append(str10)
##写入结果到文件中
wrt_str_to_file(result_file,l_result)
