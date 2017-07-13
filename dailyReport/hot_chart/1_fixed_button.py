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
result_file = cf.get("resultfile","fixed_button")
#检查目录是否存在，如果不存在则创建
result_dir = '/'.join(result_file.split('/')[:-1])
if not os.path.exists(result_dir):
    os.makedirs(result_dir)
#获取今日源文件名称及路径
cur_short_day = get_day_short_fmt(pre_day)
cur_and_fname = cur_data_dir + cur_short_day + 'Android.csv'
cur_ios_fname = cur_data_dir + cur_short_day +'iOS.csv'
cur_h5_fname = cur_data_dir + cur_short_day + 'H5.csv'
print cur_and_fname,cur_ios_fname,cur_h5_fname

#获取昨日源文件名称及路径
pre_short_day = get_day_short_fmt(pre_pre_day)
pre_and_fname = pre_data_dir + pre_short_day + 'Android.csv'
pre_ios_fname = pre_data_dir + pre_short_day +'iOS.csv'
pre_h5_fname = pre_data_dir + pre_short_day + 'H5.csv'
print pre_and_fname,pre_ios_fname,pre_h5_fname

#开始计算六个按钮
#for line in open(and_fname):
#    pass
cf.read("../../../resource/hotchart_dict")
fixed_button = cf.get("fixed_button","fixed_button")
l_fixed_button = []
for x in fixed_button.split(','):
    btn_name = x.strip().split(':')[0]
    and_code = x.strip().split(':')[1]
    ios_code = x.strip().split(':')[2]
    cur_and_click_cnt,cur_and_visit_cnt,cur_ios_click_cnt,cur_ios_visit_cnt = 0,0,0,0
    pre_and_click_cnt,pre_and_visit_cnt,pre_ios_click_cnt,pre_ios_visit_cnt = 0,0,0,0
    #计算今日点击数及访问次数
    for line in open(cur_and_fname):
        l = line.strip().split(',')
        if len(l) == 5:
            if l[1].strip('"') == and_code:
                cur_and_click_cnt,cur_and_visit_cnt = l[2],l[3]
    #print and_code,cur_and_click_cnt,cur_and_visit_cnt
    for line in open(cur_ios_fname):
        l = line.strip().split(',')
        if len(l) == 5:
            if l[1].strip('"') == ios_code:
                cur_ios_click_cnt,cur_ios_visit_cnt = l[2],l[3]
    #print ios_code,cur_ios_click_cnt,cur_ios_visit_cnt
    #计算昨日点击数及访问次数
    for line in open(pre_and_fname):
        l = line.strip().split(',')
        if len(l) == 5:
            if l[1].strip('"') == and_code:
                pre_and_click_cnt,pre_and_visit_cnt = l[2],l[3]
    for line in open(pre_ios_fname):
        l = line.strip().split(',')
        if len(l) == 5:
            if l[1].strip('"') == ios_code:
                pre_ios_click_cnt,pre_ios_visit_cnt = l[2],l[3]
    #计算总点击次数、总访问次数、增长率
    cur_click_cnt = int(cur_and_click_cnt) + int(cur_ios_click_cnt)
    pre_click_cnt =  int(pre_and_click_cnt) + int(pre_ios_click_cnt)
    click_inc_pct = get_inc_pct(cur_click_cnt,pre_click_cnt)
    cur_visit_cnt = int(cur_and_visit_cnt) + int(cur_ios_visit_cnt)
    pre_visit_cnt = int(pre_and_visit_cnt) + int(pre_ios_visit_cnt)
    visit_inc_pct = get_inc_pct(cur_visit_cnt,pre_visit_cnt)
    s = '\t'.join(['6个固定按钮',btn_name,str(cur_click_cnt),str(pre_click_cnt),click_inc_pct,str(cur_visit_cnt),str(pre_visit_cnt),visit_inc_pct])
    l_fixed_button.append(s)
    #print btn_name,cur_click_cnt,pre_click_cnt,click_inc_pct,cur_visit_cnt,pre_visit_cnt,visit_inc_pct
wrt_str_to_file(result_file,l_fixed_button)


