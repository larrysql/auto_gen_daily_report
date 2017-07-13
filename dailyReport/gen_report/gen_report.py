#coding:utf-8
import xlsxwriter
import datetime,calendar
import ConfigParser
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('../../utils/')
from toolUtil import *

#######################################参数设置###################################################
#设置时间
if len(sys.argv) ==1:
    pre_day = get_date_fmt('pre_day')
    today =  get_date_fmt('today')
else:
    pre_day = sys.argv[1]
    pre_date = datetime.datetime.strptime(pre_day, '%Y%m%d')
    today_date = pre_date+datetime.timedelta(days=1)
    today =  today_date.strftime("%Y%m%d")

now_date = datetime.datetime.strptime(pre_day, "%Y%m%d")
pre_mon_date = get_date_fmt('pre_mon_date')

cur_month = get_date_fmt('cur_month',now_date)
prev_month = get_date_fmt('prev_month',now_date)
cur_month_name = get_date_fmt('cur_month_name',now_date)
prev_month_name = get_date_fmt('prev_month_name',now_date)

cur_mon_days = get_date_fmt('cur_mon_days',now_date)
prev_mon_days = get_date_fmt('prev_mon_days',now_date)

#定义日报名称
rpt_name = u'北京移动客户端日报_' + pre_day + '.xlsx'
char_set = 'GBK'
#获取数据文件及日志文件路径
cf = ConfigParser.ConfigParser()
cf.read("../../../resource/init.conf")

#取得计算结果文件名
cf.set('resultfile','date',pre_day)
cf.set('resultfile','cur_month',cur_month)
cf.set('resultfile','prev_month',prev_month)
guimohuoyue = cf.get("resultfile", "guimohuoyue")
new_users = cf.get("resultfile", "new_user")
web_new_users = cf.get("resultfile","web_new_user")
new_users_distr = cf.get("resultfile", "new_users_distr")
act_users_data = cf.get("resultfile","act_users_data")
latest_version_data = cf.get("resultfile","latest_version_data")
old_version_data = cf.get("resultfile","old_version_data")
version_distr_data = cf.get("resultfile","version_distr_data")
version_distr_his_data = cf.get("resultfile","month_version_proportion")
perf_mon_login_succ = cf.get("resultfile","perf_mon_login_succ")
perf_mon_trans_succ = cf.get("resultfile","perf_mon_trans_succ")
hot_chart = cf.get("resultfile","hot_chart")

#取得历史数据文件名
pre_mon_inc_perday = cf.get("resultfile", "pre_mon_inc_perday") #上月每日新增历史数据
cur_mon_inc_perday = cf.get("resultfile", "cur_mon_inc_perday") #本月每日新增历史数据
#print 'cur_mon_inc_perday=',cur_mon_inc_perday
#print 'pre_mon_inc_perday=',pre_mon_inc_perday
pre_mon_inc_act = cf.get("resultfile", "pre_mon_inc_act")    #新增月活目标差距(上月)
cur_mon_inc_act = cf.get("resultfile", "cur_mon_inc_act")     #新增月活目标差距(本月)
pre_mon_total_act = cf.get("resultfile", "pre_mon_total_act")     #累计月活目标差距(上月)
cur_mon_total_act = cf.get("resultfile", "cur_mon_total_act")     #累计月活目标差距(本月)

#assert (is_exist(pre_mon_inc_perday)),u"没有找到文件" + pre_mon_inc_perday
#取得最新版本号
latest_version = cf.get("version", "version")
#设置初始行列
row,col = 0,0

#新建excel及sheet
workbook = xlsxwriter.Workbook(rpt_name)
worksheet = workbook.add_worksheet()   #存放日报内容
workSheet2 = workbook.add_worksheet()  #存放画图所需数据

#创建图表样式
null_fmt1 = workbook.add_format(eval(cf.get("style", "null_fmt1")))
hd_fmt1 = workbook.add_format(eval(cf.get("style", "hd_fmt1")))
hd_fmt2 = workbook.add_format(eval(cf.get("style", "hd_fmt2")))
hd_fmt3 = workbook.add_format(eval(cf.get("style", "hd_fmt3")))
content_fmt1 = workbook.add_format(eval(cf.get("style", "content_fmt1")))
content_fmt2 = workbook.add_format(eval(cf.get("style", "content_fmt2")))

#设置列宽
worksheet.set_column('A:A', 35,null_fmt1)
# worksheet.set_column('B:H', 20,null_fmt1)
worksheet.set_column(1,100,20,null_fmt1)
#############################################开始处理excel##########################################################
###----------1.开始处理规模活跃类----------------
worksheet.set_row(row,None,null_fmt1)

row+=1
worksheet.write(row,col,u'1.规模活跃类',hd_fmt1)
worksheet.set_row(row,None,hd_fmt1)
#表头
l_hdr = [u'累计',u'完成',u'完成进度']
row+=1
for i in range(len(l_hdr)):
	worksheet.write_row(row,col,l_hdr,hd_fmt2)

#开始读取计算结果文件,并写入到excel
row+=1
for line in open(guimohuoyue):
	l = line.split()
	#l[0] = l[0].decode(char_set).encode('utf8')
	worksheet.write_row(row,col,l,content_fmt2)
	row+=1
#生成本月及上月趋势图
##(1)每日新增趋势图
max_days = max(cur_mon_days,prev_mon_days)
l_days = [[str(i),0,0] for i in range(1,max_days+1)]

# l_day_cur,l_val_cur,l_day_pre,l_val_pre = [],[],[],[]
l_cur,l_pre, = [],[]
if is_exist(cur_mon_inc_perday):
	for line in open(cur_mon_inc_perday):
		l = line.split()
		if len(l)<2:
			continue
		day = int(l[0][-2:])
		l_cur.append([str(day),l[1]])

if is_exist(pre_mon_inc_perday):
	for line in open(pre_mon_inc_perday):
		l = line.split()
		if len(l)<2:
			continue
		day = int(l[0][-2:])
		l_pre.append([str(day),l[1]])

cur_flag = 0
for x in l_days:
	for y in l_cur:
		if x[0] == y[0]:
			#print x[0],y[0],x[1],y[1]
			x[1] = int(y[1])
			cur_flag = 1
	if cur_flag == 0:
		x[1] = ''
	cur_flag = 0

pre_flag = 0
for x in l_days:
	for y in l_pre:
		if x[0] == y[0]:
			#print x[0],y[0],x[1],y[1]
			x[2] = int(y[1])
			pre_flag = 1
	if pre_flag == 0:
		x[2] = ''
	pre_flag = 0

l_days_z = zip(*l_days)  #将列表转换为三个子列表。

workSheet2.write_column('A1',l_days_z[0])  #所有日期列表
workSheet2.write_column('B1',l_days_z[1])  #本月数据
workSheet2.write_column('C1',l_days_z[2])  #上月数据
# workSheet2.write_column('D1',l_val_pre)
# workSheet2.write_column('E1',l_days)

# len_cur,len_pre,len_days = len(l_day_cur),len(l_day_pre),len(l_days)
len_days = len(l_days)
#print 'len_days====',len_days
chart1 = workbook.add_chart({'type': 'line'})
chart1.add_series({
'name': cur_month_name,
'categories': '=Sheet2!$A$1:$A$' + str(len_days),
'values': '=Sheet2!$B$1:$B$' + str(len_days),
})

chart1.add_series({
'name': prev_month_name,
'categories': '=Sheet2!$A$1:$A$' + str(len_days),
'values': '=Sheet2!$C$1:$C$' + str(len_days),
})

chart1.set_title ({
		'name': u'每日新增趋势图',
		'name_font':{
			'name': 'Calibri',
			'color':'black',
			'size':10,
			},
	})
chart1.set_size({'width': 500, 'height': 160})
worksheet.insert_chart('D2', chart1, {'x_offset': 50, 'y_offset': 20})

##(2)新增月活目标差距趋势图
l_cur,l_pre, = [],[]
l_days = [[str(i),0,0] for i in range(1,max_days+1)]

if is_exist(cur_mon_inc_act):
	for line in open(cur_mon_inc_act):
		l = line.split()
		if len(l)<2:
			continue
		day = int(l[0][-2:])
		l_cur.append([str(day),l[1]])

if is_exist(pre_mon_inc_act):
	for line in open(pre_mon_inc_act):
		l = line.split()
		if len(l)<2:
			continue
		day = int(l[0][-2:])
		l_pre.append([str(day),l[1]])

cur_flag = 0
for x in l_days:
	for y in l_cur:
		if x[0] == y[0]:
			#print x[0],y[0],x[1],y[1]
			x[1] = int(y[1])
			cur_flag = 1
	if cur_flag == 0:
		x[1] = ''
	cur_flag = 0

pre_flag = 0
for x in l_days:
	for y in l_pre:
		if x[0] == y[0]:
			#print x[0],y[0],x[1],y[1]
			x[2] = int(y[1])
			pre_flag = 1
	if pre_flag == 0:
		x[2] = ''
	pre_flag = 0

l_days_z = zip(*l_days)  #将列表转换为三个子列表。

workSheet2.write_column('D1',l_days_z[0])  #所有日期列表
workSheet2.write_column('E1',l_days_z[1])  #本月数据
workSheet2.write_column('F1',l_days_z[2])  #上月数据
# workSheet2.write_column('D1',l_val_pre)
# workSheet2.write_column('E1',l_days)

# len_cur,len_pre,len_days = len(l_day_cur),len(l_day_pre),len(l_days)
len_days = len(l_days)
#print len_days
chart2 = workbook.add_chart({'type': 'line'})
chart2.add_series({
'name': cur_month_name,
'categories': '=Sheet2!$D$1:$D$' + str(len_days),
'values': '=Sheet2!$E$1:$E$' + str(len_days),
})

chart2.add_series({
'name': prev_month_name,
'categories': '=Sheet2!$D$1:$D$' + str(len_days),
'values': '=Sheet2!$F$1:$F$' + str(len_days),
})

chart2.set_title ({
		'name': u'新增月活目标差距趋势图',
		'name_font':{
			'name': 'Calibri',
			'color':'black',
			'size':10,
			},
	})
chart2.set_size({'width': 500, 'height': 160})
worksheet.insert_chart('A12', chart2, {'x_offset': 20, 'y_offset': 0})

# ##(3)累计月活目标差距趋势
l_cur,l_pre, = [],[]
l_days = [[str(i),0,0] for i in range(1,max_days+1)]

if is_exist(cur_mon_total_act):
	for line in open(cur_mon_total_act):
		l = line.split()
		if len(l)<2:
			continue
		day = int(l[0][-2:])
		l_cur.append([str(day),l[1]])

if is_exist(pre_mon_total_act):
	for line in open(pre_mon_total_act):
		l = line.split()
		if len(l)<2:
			continue
		day = int(l[0][-2:])
		l_pre.append([str(day),l[1]])

cur_flag = 0
for x in l_days:
	for y in l_cur:
		if x[0] == y[0]:
			#print x[0],y[0],x[1],y[1]
			x[1] = int(y[1])
			cur_flag = 1
	if cur_flag == 0:
		x[1] = ''
	cur_flag = 0

pre_flag = 0
for x in l_days:
	for y in l_pre:
		if x[0] == y[0]:
			#print x[0],y[0],x[1],y[1]
			x[2] = int(y[1])
			pre_flag = 1
	if pre_flag == 0:
		x[2] = ''
	pre_flag = 0

l_days_z = zip(*l_days)  #将列表转换为三个子列表。

workSheet2.write_column('G1',l_days_z[0])  #所有日期列表
workSheet2.write_column('H1',l_days_z[1])  #本月数据
workSheet2.write_column('I1',l_days_z[2])  #上月数据

len_days = len(l_days)
#print len_days
chart3 = workbook.add_chart({'type': 'line'})
chart3.add_series({
'name': cur_month_name,
'categories': '=Sheet2!$G$1:$G$' + str(len_days),
'values': '=Sheet2!$H$1:$H$' + str(len_days),
})

chart3.add_series({
'name': prev_month_name,
'categories': '=Sheet2!$D$1:$D$' + str(len_days),
'values': '=Sheet2!$I$1:$I$' + str(len_days),
})

chart3.set_title ({
		'name': u'累计月活目标差距趋势图',
		'name_font':{
			'name': 'Calibri',
			'color':'black',
			'size':10,
			},
	})
chart3.set_size({'width': 500, 'height': 160})
worksheet.insert_chart('D12', chart3, {'x_offset': 50, 'y_offset': 0})

##############################----------2.开始处理新增用户----------------#####################
row+=12
worksheet.write(row,col,u'2.新增用户',hd_fmt1)
worksheet.set_row(row,None,hd_fmt1)

row+=1
worksheet.write(row,col,u'1）各渠道数据',null_fmt1)
worksheet.set_row(row,None,null_fmt1)

#表头
row+=1
l_hdr = [u'渠道',u'今日新增用户',u'昨日新增用户',u'增长率(%)']
worksheet.write_row(row,col,l_hdr,hd_fmt2)

#表内容
row+=1
for line in open(new_users):
	l = line.split()
	#l[0] = l[0].decode(char_set).encode('utf8')
	worksheet.write_row(row,col,l,content_fmt2)
	row+=1
#bmcc179-222渠道用户分布
#表头
row+=1
l_hdr = [u'渠道',u'今日新增用户',u'昨日新增用户',u'增长率(%)']
worksheet.write_row(row,col,l_hdr,hd_fmt2)
#表内容
row+=1
for line in open(web_new_users):
	l = line.split()
	#l[0] = l[0].decode(char_set).encode('utf8')
	worksheet.write_row(row,col,l,content_fmt2)
	row+=1

#########开始画新增用户分布图###
#写入用户分布数据
l_channel,l_cnt = [],[]
for line in open(new_users_distr):
	l = line.split()
	#s = l[0].decode(char_set).encode('utf8')
	s = l[0]
	l_channel.append(s)
	l_cnt.append(int(l[1]))
workSheet2.write_column('J1',l_channel)
workSheet2.write_column('K1',l_cnt)
#开始绘图
chart4 = workbook.add_chart({'type': 'pie'})
chart4.add_series({
	'name':u'新增用户渠道分布图',
	'categories': '=Sheet2!$J$1:$J$' + str(len(l_channel)),
	'values': '=Sheet2!$K$1:$K$' + str(len(l_cnt)),
})

chart4.set_title({'name':u'新增用户渠道分布图',
				  'name_font':{
								'name': 'Calibri',
								'color':'black',
								'size':10,
							},
				})
chart4.set_size({'width':450, 'height': 280})
worksheet.insert_chart('E25', chart4, {'x_offset': 10, 'y_offset': 0})

##############################----------3.开始处理活跃用户数据----------------#####################
#表头
worksheet.set_row(row,None,null_fmt1)
row+=1
worksheet.write(row,col,u'3.活跃用户数据',hd_fmt1)
worksheet.set_row(row,None,hd_fmt1)
row+=1
worksheet.merge_range(row,col+1,row,col+3,u'活跃用户数',hd_fmt2)
worksheet.merge_range(row,col,row+1,col,u'版本号',hd_fmt3)
row+=1
worksheet.write_row(row,col+1,[u'安卓','IOS',u'合计'],hd_fmt2)
row+=1
#print act_users_data
for line in open(act_users_data):
	l = line.split()
	#l[0] = l[0].decode(char_set).encode('utf8')
	worksheet.set_row(row,None,null_fmt1)
	worksheet.write_row(row,col,l,content_fmt1)
	row+=1

##############################----------4.开始版本数据-----------------------#####################
#表头
row+=1
worksheet.write(row,col,u'4.版本数据',hd_fmt1)
worksheet.set_row(row,None,hd_fmt1)
row+=1
#最新版本累计数据
worksheet.write(row,col,u'1）' + latest_version + u'版本累计数据',null_fmt1)
worksheet.set_row(row,None,null_fmt1)
row+=1
worksheet.write_row(row,col,[None,u'安卓','IOS',u'合计'],hd_fmt2)
row+=1
for line in open(latest_version_data):
	l = line.split()
	#l[0] = l[0].decode(char_set).encode('utf8')
	worksheet.write_row(row,col,l,content_fmt1)
	row+=1
#老用户更新来源
row+=1
worksheet.write(row,col,u'2）老用户更新来源',null_fmt1)
worksheet.set_row(row,None,null_fmt1)
row+=1
worksheet.write_row(row,col,[None,u'安卓','IOS',u'合计'],hd_fmt2)
row+=1
for line in open(old_version_data):
	l = line.split()
	#l[0] = l[0].decode(char_set).encode('utf8')
	worksheet.write_row(row,col,l,content_fmt1)
	row+=1

#今日各版本用户分布数据
row+=1
worksheet.write(row,col,u'3）今日各版本用户分布数据',null_fmt1)
worksheet.set_row(row,None,null_fmt1)
row+=1
worksheet.merge_range(row,col,row+1,col,None,hd_fmt2)
worksheet.merge_range(row,col+1,row,col+3,u'新增用户数',hd_fmt2)
worksheet.merge_range(row,col+4,row,col+7,u'总用户数',hd_fmt2)
row+=1
worksheet.write_row(row,col+1,[u'安卓','IOS',u'合计',u'安卓','IOS',u'合计',u'版本覆盖率'],hd_fmt2)
row+=1
for line in open(version_distr_data):
	l = line.split()
	#l[0] = l[0].decode(char_set).encode('utf8')
	if '|' in l[0]:
		l1 = l[0].split('|')
		l2 = l[-1].split('|')
		worksheet.write(row,col,l1[0],content_fmt2)
		worksheet.write(row+1,col,l1[1],content_fmt2)
		for i in range(1,len(l)-1):
			worksheet.merge_range(row,col+i,row+1,col+i,int(l[i]),content_fmt2)
		worksheet.write(row,col+len(l)-1,l2[0],content_fmt2)
		worksheet.write(row+1,col+len(l)-1,l2[1],content_fmt2)
		row+=2
	else:
		worksheet.write_row(row,col,l,content_fmt2)
		row+=1
#开始画全量用户版本分布图
l_ver,l_pct = [],[]
rn = 0
for line in open(version_distr_his_data):
	l = line.split()
	if rn>0:
		for i in range(1,len(l)):
			l[i] = float(l[i])
	if len(l) > 1:
		ver_cnt = len(l) - 1
	workSheet2.write_row(rn,12,l)
	rn+=1

#开始画图
chart5 = workbook.add_chart({'type': 'column', 'subtype': 'percent_stacked'})
for i in range(ver_cnt):
	chart5.add_series({
    		'name':  	['Sheet2',0,13+i],
    		'categories': '=Sheet2!$M$2:$M$' + str(rn),
    		'values':   ['Sheet2',1,13+i,rn,13+i],
    })

chart5.set_title ({'name': '全量用户版本分布情况',
					'name_font':{
								'name': 'Calibri',
								'color':'black',
								'size':10,
							},
				 })
chart5.set_x_axis({'name': '日期'})
chart5.set_y_axis({'name': '各版本分布'})
chart5.set_size({'width':800, 'height': 280})
worksheet.insert_chart(row,0, chart5, {'x_offset': 0, 'y_offset': 10})

row+=16
##############################----------5. 用户使用行为数据-------------#####################
##获取需要显示的项目列表
#cf.read("../../../resource/hotchart_dict")
#dict_name_display = cf.get('all_dict','dict_name_display')
#l_dict_name_display =  dict_name_display.strip().split(',')
#for x in l_dict_name_display:
#    print x
##开始写入数据到excel
#worksheet.write(row,col,u'5.用户使用行为数据',hd_fmt1)
#worksheet.set_row(row,None,hd_fmt1)
#row+=1
#worksheet.write(row,col,u'1）客户端各位置点击情况（热力图）',null_fmt1)
#row+=1
#l_hdr = [u'位置',u'  ',u'今日点击次数',u'昨日点击次数',u'增长率',u'今日访问次数',u'昨日访问次数',u'增长率']
#for x in l_dict_name_display:
#    worksheet.write_row(row,col,l_hdr,hd_fmt2)
#    row+=1
#    row_start = row
#    dict_name = x.strip("'").strip()
#    for line in open(hot_chart):
#        l = line.strip().split()
#        if len(l) == 0:
#            continue
#        if dict_name == l[0].strip():
#            worksheet.write_row(row,col,l,content_fmt2)
#            row+=1
#    row_end = row - 1
#    worksheet.merge_range(row_start,col,row_end,col,dict_name,content_fmt2)
#
##############################----------6.系统性能监控（登录成功率）-------------#####################
worksheet.write(row,col,u'6.系统性能监控（登录成功率）',hd_fmt1)
worksheet.set_row(row,None,hd_fmt1)
row+=1
worksheet.merge_range(row,col,row+1,col+1,None,hd_fmt2)
worksheet.merge_range(row,col+2,row,col+5,u'所有版本',hd_fmt2)
worksheet.merge_range(row,col+6,row,col+9,u'5.0.1版本',hd_fmt2)
row+=1
l_hdr = [u'今日',u'昨日',u'增长率',u'本月累计',u'今日',u'昨日',u'增长率',u'本月累计']
worksheet.write_row(row,col+2,l_hdr,hd_fmt2)
row+=1
i = 1
for line in open(perf_mon_login_succ):
	l = line.split()
	#l[0] = l[0].decode(char_set).encode('utf8')
	#l[1] = l[1].decode(char_set).encode('utf8')
	worksheet.write_row(row,col,l,content_fmt2)
	if (i % 2 == 0):
		worksheet.merge_range(row,col,row-1,col,l[0],content_fmt1)
	i+=1
	row+=1
worksheet.merge_range(row-4,col+6,row-1,col+9,None,content_fmt2)

##############################----------7. 系统性能监控（业务办理成功率）-------------#####################
row+=1
worksheet.write(row,col,u'7.系统性能监控（业务办理成功率）',hd_fmt1)
worksheet.set_row(row,None,hd_fmt1)
row+=1
worksheet.write(row,col,u'接口性能：（列出业务办理成功率低于50%的业务）',null_fmt1)
row+=1
l_hdr = [pre_day,u'成功率',u'订购次数']
worksheet.write_row(row,col,l_hdr,hd_fmt2)
row+=1
#print perf_mon_trans_succ
for  line in open(perf_mon_trans_succ):
        #print line
	l = line.split()
	l_tmp = [l[0],l[3]+'%',l[2]]
	if int(l[3])>=50:
		break
	# l[0] = l[0].decode(char_set).encode('utf8')
	# l[1] = l[1].decode(char_set).encode('utf8')
 	worksheet.write_row(row,col,l_tmp,content_fmt1)
	row+=1
workbook.close()
