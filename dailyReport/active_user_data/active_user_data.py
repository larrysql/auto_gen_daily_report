#coding:utf-8
#Author:梁世强

"""计算活跃用户，按版本排序,将结果输出到文件中"""

import datetime
import ConfigParser
import sys
sys.path.append('../../utils/')
from toolUtil import *
import os

if len(sys.argv) ==1:
    pre_day = get_date_fmt('pre_day')
else:
    pre_day = sys.argv[1]

#读取配置文件
cf = ConfigParser.ConfigParser()
cf.read("../../../resource/init.conf")

cf.set('path','date',pre_day)
data_file = cf.get("path", "data_path") + '/'  + 'act_groupver' + pre_day + '.txt'

cf.set('resultfile','date',pre_day)
result_file = cf.get("resultfile","act_users_data")
guimohuoyue = cf.get("resultfile", "guimohuoyue")  #规模活跃类结果文件
print result_file
data_dir = cf.get("path", "data_path")
result_dir = '/'.join(result_file.split('/')[:-1])
#版本配置文件
and_ver_file = cf.get('datafile','and_version')
ios_ver_file = cf.get('datafile','ios_version')

#检查目录是否存在，如果不存在则创建
if not os.path.exists(result_dir):
    os.makedirs(result_dir)
print data_file

#将源文件数据转换为dict
d_act_data = {}
begin_flag = 0
assert (os.path.isfile(data_file)),"error,datafile not found!"
for line in open(data_file):
    if '活跃' in line:
        begin_flag = 1
        continue
    elif 'bjservice' in line and begin_flag == 1:
        key = line.strip().split()[0]
        val = int(line.strip().split()[1])
        d_act_data[key] = val
    elif 'bjservice' not in line and begin_flag == 1:
        break
    else:
        continue

#生成版本列表
l_ver_and = [x.strip() for x in open(and_ver_file)]
l_ver_ios = [x.strip() for x in open(ios_ver_file)]

#获取最大版本号和最小版本号
max_ver_no = get_max_ver_no(l_ver_and,l_ver_ios)
and_min_ver_no = get_min_ver_no(l_ver_and)
ios_min_ver_no = get_min_ver_no(l_ver_ios)
print 'max_ver_no=',max_ver_no,'and_min_ver_no=',and_min_ver_no,'ios_min_ver_no=',ios_min_ver_no

#开始分布计算安卓和ios的各版本活跃用户数
d_and_active_user = get_act_user_cnt(and_min_ver_no,max_ver_no,l_ver_and,d_act_data)
d_ios_active_user = get_act_user_cnt(ios_min_ver_no,max_ver_no,l_ver_ios,d_act_data)
print '安卓',d_and_active_user
print 'ios',d_ios_active_user

#将所有版本合并、去重、排序
l_ver = list(set([k for k in d_and_active_user.keys()] + [k for k in d_ios_active_user.keys()]))

l_pre_ver = sorted([x for x in l_ver if 'x' in x],reverse=True)
l_cur_ver = [x for x in l_ver if 'x' not in x]

l_cur_ver_int = [[int(y) for y in x] for x in [x.split('.') for x in l_cur_ver]]
l_cur_ver_int.sort(key = lambda l:(l[0],l[1],l[2]),reverse=True)
#l_cur_ver = [[str(y) for y in x] for x in l_cur_ver_int]
l_cur_ver = ['.'.join(x) for x in [[str(y) for y in x] for x in l_cur_ver_int]]
l_all_ver = l_cur_ver + l_pre_ver
print l_all_ver

#开始输出结果到列表中
l_result = []
for x in l_all_ver:
    and_act_cnt = d_and_active_user.get(x,'--')
    ios_act_cnt = d_ios_active_user.get(x,'--')
    sum_act_cnt = get_val_default(and_act_cnt) + get_val_default(ios_act_cnt)
    if x == '4.x':
        and_4x_cnt = and_act_cnt
    print x,and_act_cnt,ios_act_cnt,sum_act_cnt
    l = [x,str(and_act_cnt),str(ios_act_cnt),str(sum_act_cnt)]
    l_result.append(l)

#计算安卓和ios的总和
l_and = [x[1] for x in l_result]
l_ios = [x[2] for x in l_result]
and_cnt = sum([int(x) for x in l_and if x.isdigit()])
ios_cnt = sum([int(x) for x in l_ios if x.isdigit()])
all_cnt = and_cnt + ios_cnt
l_result.append(['合计',and_cnt,ios_cnt,all_cnt])
other_cnt =  all_cnt - and_4x_cnt
print 'other_cnt=',other_cnt
all_cnt_final =  get_cur_active_user(guimohuoyue)#从规模活跃类中取得的总活跃用户数据
and_4x_cnt_final = all_cnt_final - other_cnt
#修正and 4.x数据和总用户合计
for x in  l_result:
    if x[0] == '4.x':
        x[1] = str(and_4x_cnt_final)
        x[3] = str(int(x[1]) + int(x[2]))
    if x[0] =='合计':
        x[3] = str(all_cnt_final)
        x[1] = str(all_cnt_final - x[2])
        x[2] = str(x[2])
    print x
l_str = ['\t'.join(x) for x in l_result]
print l_str

#将结果写入到文件
wrt_str_to_file(result_file,l_str)
