#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = '秦欢'
'增、删、改、查文件'
import os

# 将字符串 str1 写入到给定的文件中
# 参数：path：'a/b/c/d/e.txt' str1:'hello world' 
# append 默认为 'a', 另外可选如下参数值：
# w: 覆写，文件不存在则创建
# w+: 覆写可读，文件不存在则创建
# r+: 读写，文件不存在报错
# a: 追加，文件不存在则创建
# a+: 追加可读，文件不存在则创建
# ...
# 还有很多种，欢迎添加完善
def writeStr2File(path,str1,append = 'a'):
    # 去掉文件，保留路径。比如 'a/b/c/d.txt' 经过下面代码会变成 'a/b/c'
    subPath = path[:path.rfind('/')]
    # 如果给定的路径中，文件夹不存在，则创建
    if not os.path.exists(subPath):
        os.makedirs(subPath)
    # 打开文件并将 str 内容写入给定的文件
    with open(path, append) as f:
        f.write(str1)

#检测文件是否存在，如果不存在就创建，存在则清空
def cleanFile(path):
    subPath = path[:path.rfind('/')]
    if not os.path.exists(subPath):
        os.makedirs(subPath)
    f = open(path, 'w')
    f.close()

#将测文件是否存在，不存在就创建
def mkFile(path):
    subPath = path[:path.rfind('/')]
    if not os.path.exists(subPath):
        os.makedirs(subPath)
        f = open(path, 'w')
        f.close()
