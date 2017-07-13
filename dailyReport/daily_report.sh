#!/bin/bash
source ~/.bash_profile
#DAY=$1
if [ ! -n "$1" ];
then
    DAY=`date  +"%Y%m%d" -d  "-1 days"`
else
    DAY=$1
fi
#echo $DAY

#设置脚本路径及脚本名称
BASE_DIR="/home/aspire/apps/DailyReport/src/dailyReport/"
DIR_USER_ACTIVE="user_active"
DIR_NEW_USER="new_user"
DIR_ACTIVE_USER="active_user_data"
DIR_VERSION_DATA="version_data"
DIR_BUSS_RATE="sys_performence_monitor/buss_subscribe_success_rate"
DIR_LOG_SUCC_RATE="sys_performence_monitor/log_success_rate"
DIR_GEN_REPORT="gen_report"

USER_ACTIVE="gen_totalNum.py"
NEW_USER="qudao_add_user_today.py"
WEB_NEW_USER="web_qudao_add_user_today.py"
ACTIVE_USER_DATA="active_user_data.py"
OLD_TO_NEW="olduser_to_newversion.py"
VERSION_DATA="version_data.py"
VERSION_DESTRIBUTE="version_destribute.py"
BUSS_SUB_SUCC_RATE="service_oper_succ.py"
LOGIN_SUCC_PCT="login_succ_pct.py"
GEN_REPORT="gen_report.py"

#开始执行
cd $BASE_DIR$DIR_USER_ACTIVE
python $USER_ACTIVE $DAY

cd $BASE_DIR$DIR_NEW_USER
python $NEW_USER $DAY
python $WEB_NEW_USER $DAY

cd $BASE_DIR$DIR_ACTIVE_USER
python $ACTIVE_USER_DATA $DAY

cd $BASE_DIR$DIR_VERSION_DATA
python $OLD_TO_NEW $DAY
python $VERSION_DATA $DAY
python $VERSION_DESTRIBUTE $DAY

cd $BASE_DIR$DIR_BUSS_RATE
python $BUSS_SUB_SUCC_RATE $DAY

cd $BASE_DIR$DIR_LOG_SUCC_RATE
python $LOGIN_SUCC_PCT $DAY

cd $BASE_DIR$DIR_GEN_REPORT
python $GEN_REPORT $DAY
