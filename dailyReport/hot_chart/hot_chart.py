#coding:utf-8
#Author:梁世强

"""计算热力图数据，将结果输出到文件中"""

import datetime
import ConfigParser
import sys
sys.path.append('../../utils/')
from toolUtil import *
import os
import csv

if len(sys.argv) ==1:
    pre_day = get_date_fmt('pre_day')
else:
    pre_day = sys.argv[1]

#读取配置文件
cf = ConfigParser.ConfigParser()
cf.read("../../../resource/init.conf")

cf.set('path','date',pre_day)
cur_data_dir = cf.get("path", "data_path") #今日源数据目录

pre_pre_day = get_delta_day(pre_day,1)
cf.set('path','date',pre_pre_day)
pre_data_dir = cf.get("path", "data_path") #昨日源数据目录

#print cur_data_dir,pre_data_dir
cf.set('resultfile','date',pre_day)
result_file = cf.get("resultfile","hot_chart")
#检查目录是否存在，如果不存在则创建
result_dir = '/'.join(result_file.split('/')[:-1])
if not os.path.exists(result_dir):
    os.makedirs(result_dir)
#获取今日源文件名称及路径
#cur_short_day = get_day_short_fmt(pre_day)
cur_and_fname = cur_data_dir + pre_day + 'Android.csv'
cur_ios_fname = cur_data_dir + pre_day +'IOS.csv'
cur_h5_fname = cur_data_dir + pre_day + 'H5.csv'
#print cur_and_fname,cur_ios_fname,cur_h5_fname

#获取昨日源文件名称及路径
#pre_short_day = get_day_short_fmt(pre_pre_day)
pre_and_fname = pre_data_dir + pre_pre_day + 'Android.csv'
pre_ios_fname = pre_data_dir + pre_pre_day +'IOS.csv'
pre_h5_fname = pre_data_dir + pre_pre_day + 'H5.csv'
#print pre_and_fname,pre_ios_fname,pre_h5_fname

#开始计算六个按钮
#for line in open(and_fname):
#    pass
cf.read("../../../resource/hotchart_dict")
#fixed_button = cf.get("fixed_button","fixed_button")
dict_name = cf.get("all_dict","dict_name")
dict_detail = cf.get("all_dict","dict_detail")
l_dict_name =  dict_name.strip().split('||')
d = eval(dict_detail)

#统计固定项目的数量
def get_stat_fixed(data_file_name,code):
    click_cnt,visit_cnt = 0,0
    for line in open(data_file_name):
        l = line.strip().split(',')
        if len(l) == 5:
            if l[1].strip('"') == code and code <> '':
                #print data_file_name,'****',l[1],l[2],l[3]
                click_cnt,visit_cnt = int(l[2]),int(l[4])
                break
    return click_cnt,visit_cnt

#模糊匹配统计
def get_stat_like(data_file_name,code):
    click_cnt,visit_cnt = 0,0
    for line in open(data_file_name):
        l = line.strip().split(',')
        if len(l) == 5:
            if l[1].strip('"').startswith(code.strip('***')):
                click_cnt += int(l[2])
                visit_cnt += int(l[4])
    return click_cnt,visit_cnt



#开始计算
l_result = []
for dict_name in l_dict_name:
    dict_name = dict_name.strip("'")
    val = d.get(dict_name,None)
    if val == None:
        continue
    for x in val.split('||'):
        name = x.strip().split(':')[0]
        and_code = x.strip().split(':')[1]
        ios_code = x.strip().split(':')[2]
        if not and_code.endswith('***') and not and_code.startswith('-->'):
            #计算安卓今日点击数及访问次数
            cur_and_click_cnt,cur_and_visit_cnt = get_stat_fixed(cur_and_fname,and_code)
            #计算安卓昨日点击数及访问次数
            pre_and_click_cnt,pre_and_visit_cnt = get_stat_fixed(pre_and_fname,and_code)
        if not ios_code.endswith('***') and not ios_code.startswith('-->'):
            #计算ios今日点击数及访问次数
            cur_ios_click_cnt,cur_ios_visit_cnt = get_stat_fixed(cur_ios_fname,ios_code)
            #计算ios昨日点击数及访问次数
            pre_ios_click_cnt,pre_ios_visit_cnt = get_stat_fixed(pre_ios_fname,ios_code)
        if and_code.endswith('***') and not and_code.startswith('-->'):
            cur_and_click_cnt,cur_and_visit_cnt = get_stat_like(cur_and_fname,and_code)
            pre_and_click_cnt,pre_and_visit_cnt = get_stat_like(pre_and_fname,and_code)
        if ios_code.endswith('***') and not ios_code.startswith('-->'):
            cur_ios_click_cnt,cur_ios_visit_cnt = get_stat_like(cur_ios_fname,ios_code)
            pre_ios_click_cnt,pre_ios_visit_cnt = get_stat_like(pre_ios_fname,ios_code)
        if and_code.startswith('-->'): #当以-->开头时，代表此统计项需要从其他统计项的数据获取
            tmp_key = and_code.strip('-->')
            tmp_val = d.get(tmp_key,None)
            if tmp_val == None:
                continue
            #开始从-->指向的统计项数据中计算
            cur_and_click_cnt,pre_and_click_cnt,cur_and_visit_cnt,pre_and_visit_cnt = 0,0,0,0
            cur_ios_click_cnt,pre_ios_click_cnt,cur_ios_visit_cnt,pre_ios_visit_cnt = 0,0,0,0
            print tmp_val
            for y in tmp_val.split('||'):
                tmp_name = y.strip().split(':')[0]
                and_code = y.strip().split(':')[1]
                ios_code = y.strip().split(':')[2]
                if not and_code.endswith('***') and not and_code.startswith('-->'):
                    cnt1,cnt2 = get_stat_fixed(cur_and_fname,and_code)
                    cnt3,cnt4 = get_stat_fixed(pre_and_fname,and_code)
                    cur_and_click_cnt += cnt1
                    cur_and_visit_cnt += cnt2
                    pre_and_click_cnt += cnt3
                    pre_and_visit_cnt += cnt4
                if not ios_code.endswith('***') and not ios_code.startswith('-->'):
                    cnt5,cnt6 = get_stat_fixed(cur_ios_fname,ios_code)
                    cnt7,cnt8 = get_stat_fixed(pre_ios_fname,ios_code)
                    cur_ios_click_cnt += cnt5
                    cur_ios_visit_cnt += cnt6
                    pre_ios_click_cnt += cnt7
                    pre_ios_visit_cnt += cnt8
            print 'name,cur_and_click_cnt,cur_and_visit_cnt=',name,int(cur_and_click_cnt+cur_ios_click_cnt)
        #计算总点击次数、总访问次数、增长率
        cur_click_cnt = int(cur_and_click_cnt) + int(cur_ios_click_cnt)
        pre_click_cnt =  int(pre_and_click_cnt) + int(pre_ios_click_cnt)
        click_inc_pct = get_inc_pct(cur_click_cnt,pre_click_cnt)
        cur_visit_cnt = int(cur_and_visit_cnt) + int(cur_ios_visit_cnt)
        pre_visit_cnt = int(pre_and_visit_cnt) + int(pre_ios_visit_cnt)
        visit_inc_pct = get_inc_pct(cur_visit_cnt,pre_visit_cnt)
        s = '\t'.join([dict_name,name,str(cur_click_cnt),str(pre_click_cnt),click_inc_pct,str(cur_visit_cnt),str(pre_visit_cnt),visit_inc_pct])
        l_result.append(s)
    l_result.append('\t')
#for x in l_result:
#    print x
        #print btn_name,cur_click_cnt,pre_click_cnt,click_inc_pct,cur_visit_cnt,pre_visit_cnt,visit_inc_pct
wrt_str_to_file(result_file,l_result)


