#!/usr/bin/env python
#coding:utf-8
#author:wangxingwei

#该方法传入版本配置文件，返回版本列表
def makeVersionList(version_list_conf): #根据配置文件生成版本列表
        versionlist = list()
        f = open(version_list_conf)
        for i in f:
                i = i.strip()
                if len(i) != 0:
                        versionlist.append(i)
        return versionlist





