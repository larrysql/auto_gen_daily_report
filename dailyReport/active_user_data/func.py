#coding:utf-8
import ConfigParser
import logging
import datetime,calendar
import re

def wr_log(lv,msg):
    cf = ConfigParser.ConfigParser()
    if os.path.exists('../config/init.conf'):
        confile = '../config/init.conf'
    elif os.path.exists('config/init.conf'):
        confile = 'config/init.conf'
    else:
        print '未找到配置文件!'
    cf.read(confile)
    logfile = cf.get("path", "log_path")
    logging.basicConfig(level=logging.DEBUG,
                    #format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=logfile,
                    filemode='a')
    if lv == 'info':
        logging.info(msg)
    elif lv == 'debug':
        logging.debug(msg)
    elif lv == 'warning':
        logging.warning(msg)
    else:
        pass

def get_date_fmt(date_format):
    now_date = datetime.datetime.now()
    pre_mon_date = datetime.date(datetime.date.today().year,datetime.date.today().month-1,1)
    if date_format == 'today':
        return datetime.date.today().strftime("%Y%m%d")
    elif date_format =='pre_day':
        return (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d")
    elif date_format == 'pre_mon_date':
        return datetime.date(datetime.date.today().year,datetime.date.today().month-1,1)
    elif date_format == 'cur_month':
        return datetime.date.today().strftime("%Y%m")
    elif date_format == 'prev_month':
        return datetime.date(datetime.date.today().year,datetime.date.today().month-1,1).strftime("%Y%m")
    elif date_format == 'cur_month_name':
        return datetime.date.today().strftime("%Y年%m月")
    elif date_format == 'prev_month_name':
        return datetime.date(datetime.date.today().year,datetime.date.today().month-1,1).strftime("%Y年%m月")
    elif date_format == 'cur_mon_days':
        return calendar.monthrange(now_date.year,now_date.month)[1]
    elif date_format == 'prev_mon_days':
        return  calendar.monthrange(pre_mon_date.year,pre_mon_date.month)[1]
    else:
        return None

#获取指定日期所在月份的第一天
def get_first_day_of_month(day):
    cur_day = datetime.datetime.strptime(day, "%Y%m%d").date()
    first_day = datetime.date(cur_day.year,cur_day.month,1).strftime("%Y%m%d")
    return first_day

#获取指定天数前的日期
def get_delta_day(day,delta):
    return (datetime.datetime.strptime(day, "%Y%m%d").date() - datetime.timedelta(delta)).strftime("%Y%m%d") 

#获取所有版本登录统计信息
def get_all_ver_login_stat(day):
    l_all_ver_login_way = ['一键登录次数','一键登录成功次数','一键登录率','服务密码登录次数','服务密码登录成功次数','服务密码登录成功率','动态密码登录次数','动态密码登录成功次数','动态密码登录成功率','静默登录次数','静默登录成功次数','静默登录成功率','网站密码登录次数','网站密码登录成功次数','网站密码登录成功率','修改网站密码次数','修改网站密码成功次数','修改网站密码成功率','重置网站密码次数','重置网站密码成功次数','重置网站密码成功率']
    d_all_ver_login_way = {}
    cf = ConfigParser.ConfigParser()
    cf.read("config/init.conf")
    cf.set('path','date',day)
    data_file = cf.get("path", "data_path") + 'RI' + day + '.txt'
    for line in open(data_file):
        l = line.strip().split(':')
        key = l[0]
        if key in l_all_ver_login_way and len(l) == 2:
             d_all_ver_login_way[key] = to_int(line.strip().split(':')[1])
    return d_all_ver_login_way 
#获取指定日期的最新版本信息
def get_lastest_ver_no(day):
    patt = r'^(\d+_\d+_\d+)\D'
    d_latest_ver_login_way = {}
    cf = ConfigParser.ConfigParser()
    cf.read("config/init.conf")
    cf.set('path','date',day)
    data_file = cf.get("path", "data_path") + 'RI' + day + '.txt'
    for line in open(data_file):
        l = line.strip().split(':')
        key = l[0]
        m = re.search(patt,key)
        if m is not None:
            lastet_version_no = m.group(1)
            break
        else:
            continue  
    return lastet_version_no
#获取最新版本登录统计信息
def get_latest_ver_login_stat(day):
    #l_latest_ver_login_way = ['5_0_1动态密码登录次数','5_0_1动态密码登录成功次数','5_0_1动态密码登录成功率','5_0_1网站密码登录次数','5_0_1网站密码登录成功次数','5_0_1网站密码登录成功率','5_0_1修改网站密码次数','5_0_1修改网站密码成功次数','5_0_1修改网站密码成功率','5_0_1重置网站密码次数','5_0_1重置网站密码成功次数','5_0_1重置网站密码成功率']
    patt = r'^\d+_\d+_\d+'
    d_latest_ver_login_way = {}
    cf = ConfigParser.ConfigParser()
    cf.read("config/init.conf")
    cf.set('path','date',day)
    data_file = cf.get("path", "data_path") + 'RI' + day + '.txt'
    for line in open(data_file):
        l = line.strip().split(':')
        key = l[0]
        if re.match(patt,key) and len(l) == 2:
             d_latest_ver_login_way[key] = to_int(line.strip().split(':')[1])
    return d_latest_ver_login_way 
#获取最新版本某种类型的登陆统计信息
def get_latest_ver_type_login_stat(login_type,d):
    for k,v in d.items():
        if login_type in k:
            val = v
            break
    return val

#获取所有版本本月累计登录统计信息
def get_all_ver_cur_month_stat(cur_day):
    first_day = get_first_day_of_month(cur_day) 
    last_day  = cur_day 
    l_dates = get_date_range(first_day,last_day)
    d_cur_month_all_ver_stat,d_tmp = {},{}
    all_ver_cur_month_dynamic_pass_cnt = 0
    all_ver_cur_month_dynamic_pass_succ_cnt = 0
    all_ver_cur_month_website_pass_cnt = 0
    all_ver_cur_month_website_pass_succ_cnt = 0
    all_ver_cur_month_service_pass_cnt = 0
    all_ver_cur_month_service_pass_succ_cnt = 0
    all_ver_cur_month_slient_pass_cnt = 0
    all_ver_cur_month_slient_pass_succ_cnt = 0
    for date in l_dates:
        d_tmp = get_all_ver_login_stat(date)
        all_ver_cur_month_dynamic_pass_cnt+=d_tmp['动态密码登录次数']
        all_ver_cur_month_dynamic_pass_succ_cnt+=d_tmp['动态密码登录成功次数']
        all_ver_cur_month_website_pass_cnt+=d_tmp['网站密码登录次数']
        all_ver_cur_month_website_pass_succ_cnt+=d_tmp['网站密码登录成功次数']
        all_ver_cur_month_service_pass_cnt+=d_tmp['服务密码登录次数']
        all_ver_cur_month_service_pass_succ_cnt+=d_tmp['服务密码登录成功次数']
        all_ver_cur_month_slient_pass_cnt+=d_tmp['静默登录次数']
        all_ver_cur_month_slient_pass_succ_cnt+=d_tmp['静默登录成功次数']

    all_ver_cur_month_login_cnt = all_ver_cur_month_dynamic_pass_cnt+all_ver_cur_month_website_pass_cnt+all_ver_cur_month_service_pass_cnt+all_ver_cur_month_slient_pass_cnt
    all_ver_cur_month_login_succ_cnt = all_ver_cur_month_dynamic_pass_succ_cnt+all_ver_cur_month_website_pass_succ_cnt+all_ver_cur_month_service_pass_succ_cnt+all_ver_cur_month_slient_pass_succ_cnt

    d_cur_month_all_ver_stat = {
     '动态密码登录次数':all_ver_cur_month_dynamic_pass_cnt,'动态密码登录成功次数':all_ver_cur_month_dynamic_pass_succ_cnt,
     '网站密码登录次数':all_ver_cur_month_website_pass_cnt,'网站密码登录成功次数':all_ver_cur_month_website_pass_succ_cnt,
     '服务密码登录次数':all_ver_cur_month_service_pass_cnt,'服务密码登录成功次数':all_ver_cur_month_service_pass_succ_cnt,
     '静默登录次数':all_ver_cur_month_slient_pass_cnt,'静默登录成功次数':all_ver_cur_month_slient_pass_succ_cnt,
     '本月累计登录次数':all_ver_cur_month_login_cnt,'本月累计登录成功次数':all_ver_cur_month_login_succ_cnt,
     }
    
    return d_cur_month_all_ver_stat
#获取本月最新版本累计统计信息
def get_latest_ver_cur_month_stat(cur_day,cur_lastest_ver_no):
    first_day = get_first_day_of_month(cur_day) 
    last_day  = cur_day 
    l_dates = get_date_range(first_day,last_day)
    d_cur_month_latest_ver_stat,d_tmp = {},{}
    latest_ver_cur_month_dynamic_pass_cnt = 0
    latest_ver_cur_month_dynamic_pass_succ_cnt = 0
    latest_ver_cur_month_website_pass_cnt = 0
    latest_ver_cur_month_website_pass_succ_cnt = 0
    for date in l_dates:
        lastest_ver_no = get_lastest_ver_no(date)
        if lastest_ver_no == cur_lastest_ver_no:
            d_tmp = get_latest_ver_login_stat(date)
            latest_ver_cur_month_dynamic_pass_cnt += get_latest_ver_type_login_stat('动态密码登录次数',d_tmp)
            latest_ver_cur_month_dynamic_pass_succ_cnt += get_latest_ver_type_login_stat('动态密码登录成功次数',d_tmp)
            latest_ver_cur_month_website_pass_cnt += get_latest_ver_type_login_stat('网站密码登录次数',d_tmp)
            latest_ver_cur_month_website_pass_succ_cnt += get_latest_ver_type_login_stat('网站密码登录成功次数',d_tmp)
        else:
            continue
    latest_ver_cur_month_login_cnt = latest_ver_cur_month_dynamic_pass_cnt + latest_ver_cur_month_website_pass_cnt
    latest_ver_cur_month_login_succ_cnt = latest_ver_cur_month_dynamic_pass_succ_cnt + latest_ver_cur_month_website_pass_succ_cnt
    d_cur_month_latest_ver_stat = {'动态密码登录次数':latest_ver_cur_month_dynamic_pass_cnt,
                                   '动态密码登录成功次数':latest_ver_cur_month_dynamic_pass_succ_cnt,
                                   '网站密码登录次数':latest_ver_cur_month_website_pass_cnt,
                                   '网站密码登录成功次数':latest_ver_cur_month_website_pass_succ_cnt,
                                   '本月累计登录次数':latest_ver_cur_month_login_cnt,
                                   '本月累计登录成功次数':latest_ver_cur_month_login_succ_cnt
                                  }
    return d_cur_month_latest_ver_stat

#字符串转换为数字
def to_int(s):
    try:
        i = int(s)
    except ValueError,e:
        i = s
    return i

#获取指定范围的连续日期
def get_date_range(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y%m%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y%m%d")
    return dates
#向文件中写入字符串
def wrt_str_to_file(file_name,l_str):
    with open(file_name,'w') as f:
        for str in l_str:
            f.write(str+'\n')

#获取两个版本列表中的最大版本号
def get_max_ver_no(l1,l2):
    l1_max = int(l1[-1].split('_')[-1].split('.')[0])
    l2_max = int(l2[-1].split('_')[-1].split('.')[0])
    return max(l1_max,l2_max)

#获取一个版本列表中的最小版本号
def get_min_ver_no(l):
    return int(l[0].split('_')[-1].split('.')[0])

#获取一个版本中的大版本号
def get_ver_no(version):
    return int(version.split('_')[-1].split('.')[0])

#计算安卓或ios的各版本活跃用户数
def get_act_user_cnt(min_ver_no,max_ver_no,l_ver,d_act_data):
    k = min_ver_no
    user_cnt = 0
    max_no_flag = 0
    d_active_user = {}
    for x in l_ver:
        ver_no = get_ver_no(x)
        if ver_no == k and ver_no < max_ver_no:
            user_cnt += d_act_data[x]
        elif ver_no > k and ver_no < max_ver_no:
            d_active_user[str(k) + '.x'] = user_cnt
            k = ver_no
            user_cnt = d_act_data[x]
        elif ver_no == max_ver_no:
            ver_no = x.strip().split('_')[-1]
            if max_no_flag == 0:
                d_active_user[str(k) + '.x'] = user_cnt
                max_no_flag = 1
                d_active_user[ver_no] = d_act_data[x]
            else:
                d_active_user[ver_no] = d_act_data[x]
        else:
            continue 
    if max_no_flag == 0:
        d_active_user[str(k) + '.x'] = user_cnt 
    return d_active_user

#获取给定变量的值，如果变量为--则返回0
def get_val_default(cnt):
    if isinstance(cnt,str):
        return 0
    else:
        return cnt
