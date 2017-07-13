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
#print pre_day
#读取配置文件
cf = ConfigParser.ConfigParser()
cf.read("../../../../resource/init.conf")

cf.set('path','date',pre_day)
data_file = cf.get("path", "data_path") + '/' + 'RI' + pre_day + '.txt'

cf.set('resultfile','date',pre_day)
result_file = cf.get("resultfile","perf_mon_trans_succ")
#print result_file
data_dir = cf.get("path", "data_path")
result_dir = '/'.join(result_file.split('/')[:-1])
#print data_file
#检查目录是否存在，如果不存在则创建
# if not os.path.exists(data_dir):
#     os.makedirs(data_dir)
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

#开始处理数据
l_service_deal = []
s_service_name = set()

#f = file(result_file,"w+")
assert (os.path.isfile(data_file)),"error,datafile not found!"

for line in open(data_file):
    l = line.split(':')
    if '订购' in l[0] and '成功率' not in l[0]:
        loc = l[0].find('订购')
        service_name = l[0][:loc]
        service_key = l[0][loc:]
        service_value = l[1]
        s_service_name.add(service_name)
        l_service_deal.append([service_name,service_key,service_value])

l_result = []

for x in s_service_name:
    l_tmp = []
    succ_cnt = 0
    total_cnt = 0
    pct_succ = 0
    for y in l_service_deal:
        if x == y[0]:
            if y[1] =='订购成功次数':
                succ_cnt = succ_cnt + int(y[2])
            elif y[1] == '订购次数':
                total_cnt = total_cnt + int(y[2])
    if total_cnt != 0:
        pct_succ = int(float(succ_cnt)/float(total_cnt)*100)
    else:
        pct_succ = 0
    if pct_succ == 0 or total_cnt <= 10:
        continue
    l_tmp = [x.replace(' ',''),succ_cnt,total_cnt,pct_succ]
    l_result.append(l_tmp)

l_result = sorted(l_result,key=lambda l:l[3],reverse=False)

#for x in l_result:
#    print x[0],x[3]
# for x in s_service_name:
#     f.writelines(x+'\n')

# for x in l_service_deal:
#     s = x[0] + ':' + x[1] + ':' + x[2]
#     f.writelines(s)
# f.writelines('************************************************************\n')
for x in l_result:
    s = str(x[0]) + '\t' + str(x[1]) + '\t' + str(x[2]) + '\t' + str(x[3]) + '\n'
    #print s
#    f.writelines(s)
#f.close()
with open(result_file, 'w') as f:
    for x in l_result:
        s = str(x[0]) + '\t' + str(x[1]) + '\t' + str(x[2]) + '\t' + str(x[3]) + '\n'
        f.write(s)


# for x in l_service_name:
#     print x
# print s_service_name
# for x in s_service_name:
#     print x




