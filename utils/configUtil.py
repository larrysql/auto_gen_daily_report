#!/usr/bin/env python
# -*- coding: utf-8 -*-

'获取文件根目录'
import ConfigParser

__author__ = '秦欢'
from dateUtil import getYesterday
yesterdayDate = getYesterday()

# 加载配置文件
def loadConfig():
    cf = ConfigParser.ConfigParser()
    cf.read("../../../resource/init.conf")
    return cf

# 源数据路径
def getDataPath(date = yesterdayDate):
    cf = loadConfig()
    cf.set("path","date", date)
    return cf.get("path", "data_path")

# 待写入文件路径
def getResultPath(date = yesterdayDate):
    cf = loadConfig()
    cf.set("resultfile","date", date)
    return cf.get("resultfile", "result_dir")

# 根据 section 和 option 获取配置文件中的参数   
def getConfigProperty(section, option):
    cf = loadConfig()
    return cf.get(section, option)
