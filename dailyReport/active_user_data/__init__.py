# -*- coding: utf-8 -*-
file_and_property = open("D:\\and.txt")
file_ios_property = open("D:\\ios.txt")
#and版本配置文件
list_and_property = []
list_and_propertyb = []
while 1:
   line = file_and_property.readline().decode("UTF-8")
   file_and_property.close
   if not line:
       break
   list_and_propertyb[0:0]=[line]
for i in list_and_propertyb:
    str1 = i.strip()
    if len(str1)<19:
        continue
    list_and_property[0:0] = [str1]
   
#for  i in list_and_property:
#    print i
#print list_and_property[0]
#print len(list_and_property)
#print list_and_property[len(list_and_property)-1]

#ios版本配置文件   
list_ios_propertyb = []
list_ios_property = []
while 1:
   line = file_ios_property.readline().decode("UTF-8")
   file_ios_property.close
   if not line:
       break
   list_ios_propertyb[0:0]=[line]
for i in list_ios_propertyb:
   str3 = i.strip()
   if len(str3)<19:
       continue
   list_ios_property[0:0]=[str3]
#for  i in list_ios_property:
 #  print i 
#print list_ios_property[len(list_ios_property)-1]
#print len(list_ios_property[len(list_ios_property)-1])
#print len(list_ios_property)
#获取给定文件数据

file_act_groupver = open("D:\\act_groupver20160822.txt")
list_act_groupver = []
list_act_groupver_p = []
while 1:
   line = file_act_groupver.readline()
   file_act_groupver.close
   if not line:
       break
   list_act_groupver[0:0]=[line]
#for i in list_act_groupver:
#  print i 
#排序
for i in list_act_groupver:
    str1 = i.strip()
    list_act_groupver_p[0:0] = [str1]
	
#print list_act_groupver_p[0]
#print len(list_act_groupver_p[0])
del list_act_groupver_p[0]
#print list_act_groupver_p[17]
#print len(list_act_groupver_p[17])
#for i in list_act_groupver_p:
#    print i 
#截取活跃版本字符串及数据
list_huo1 = []
for i in list_act_groupver_p:
    if (len(i)< 20 and len(i)!=1 and len(i)!=0):
	      break
    list_huo1[0:0]=[i]
#for i in list_huo1:
#    print i 
#print list_huo1[17]
#print len(list_huo1[17])
#排序
list_huo2 = []
for i in  list_huo1:
	if len(i)==0:
	 continue
	list_huo2[0:0]=[i]
#for i in  list_huo2:
#	print i
#print len(list_huo2)

#截取活跃各版本数据----------------
list_s1 = []
for i in list_huo2:
	str1 = i[-15:]
	str2 = str1.strip()
	list_s1[0:0] = [str2]
#排序
list_s2 = []
for i in list_s1:
  list_s2[0:0] = [i]
#print len(list_s2)
#for i in list_s2:
#	print i

#截取活跃各版本号-----------------------------
list_b1 = []
list_b2 = []
for i in list_huo2:
	str1 = i[0:20]
	str2 = str1.strip()
	list_b1[0:0] = [str2]
#排序
for i in list_b1:
	list_b2[0:0] = [i]
#for i in list_b2:
#	print i 
#print len(list_b2[0])
#print list_b2[0]

#将获取的版本号及数据放入map中-----------------
count = 0
dict ={};
while (count<len(list_b2)):
	dict.setdefault(list_b2[count],list_s2[count])
	count = count+1
#print len(dict)
#for i in list_and_property:
#		print dict.get(i)
#大版本更新及数据显示--------------------------------------------------------------------
#and更新大版本：
#print len(list_ios_property)
if int((list_and_property[len(list_and_property)-1])[14:15])>int((list_ios_property[len(list_ios_property)-1])[14:15]):
		strd = "and 大版本更新"
		print strd.decode("utf-8")
		a = int((list_and_property[len(list_and_property)-1])[14:15])
		count1 = len(list_and_property)-1
		f=file("D:\\Active user data.txt","w+")
		#输出最新版本的内容
		#print a
		total_z = 0
		while count1>0:
			str1 =list_and_property[count1]
			str2 =int(str1[14:15])
			str3 = str1[14:19]
			if a!=str2:
			    break
			total_z = total_z + int(dict.get(list_and_property[count1]))
			str4 = [str3+" "+dict.get(list_and_property[count1])+" "+"---"+ " "+dict.get(str1)+"\n"]
			count1 = count1 - 1
			f.writelines(str4)
#		print total_z

		#输出历史版本统计数据 
		#andX数据
		total_and_z = 0
		total_ios_z = 0
		count2 = a-1
		while count2>2:
			total_andX=0
			str6 = str(count2)
			for i in list_and_property:
				if count2==int(i[14:15]):
					#print int(dict.get(i))
					total_andX = total_andX + int(dict.get(i))
			str3 = str(total_andX)
			total_and_z = total_and_z + total_andX
			str5=[str6+"X"+" "+str3]
			f.writelines(str5)
		#iosX数据
			total_iosX=0
			str7 = str(count2)
			for i in list_ios_property:
				if count2==int(i[14:15]):
					total_iosX = total_iosX + int(dict.get(i))
			str8 = str(total_iosX)
			total_X = total_andX + total_iosX
			total_ios_z = total_iosX + total_ios_z
			str9 = str(total_X)
			str10=[" "+str8+" "+str(total_X)+"\n"]
			f.writelines(str10)
			count2 = count2- 1
		str11 = ["合计"+"  "+str(total_z+total_and_z)+" "+str(total_ios_z)+"  "+str(total_z+total_and_z+total_ios_z)]
		f.writelines(str11)
#ios大版本更新:
if int((list_ios_property[len(list_ios_property)-1])[14:15])>int((list_and_property[len(list_and_property)-1])[14:15]):
		stri = "ios 大版本更新"
		print stri.decode("utf-8")
		a = int((list_ios_property[len(list_ios_property)-1])[14:15])
		count1 = len(list_ios_property)-1
		f=file("D:\\Active user data.txt","w+")
		#输出最新版本的内容
		while count1>0:
			str1 =list_ios_property[count1]
			str2 =int(str1[14:15])
			str3 = str1[14:19]
			if a!=str2:
			    break
			str4 = [str3+" "+"---"+" "+dict.get(list_ios_property[count1])+" "+dict.get(str1)+"\n"]
			count1 = count1 - 1
			f.writelines(str4)

		#输出历史版本统计数据 
		#andX数据
		count2 = a-1
		while count2>2:
			total_andX=0
			str6 = str(count2)
			for i in list_and_property:
				if count2==int(i[14:15]):
					#print int(dict.get(i))
					total_andX = total_andX + int(dict.get(i))
			str3 = str(total_andX)
			str5=str6+"X"+" "+str3
#			f.writelines(str5)
#			print total_andX
#			print str5
			#iosX数据
			total_iosX=0
			str7 = str(count2)
			for i in list_ios_property:
				if count2==int(i[14:15]):
					total_iosX = total_iosX + int(dict.get(i))
			str8 = str(total_iosX)
			total_X = total_andX + total_iosX
			str9 = str(total_X)
			str10=[str5+"  "+str8+"  "+str9+"\n"]
			f.writelines(str10)
			count2 = count2- 1
#			print total_iosX
#			print total_X
		total_andht = 0
		total_iosht = 0
		for i in list_and_property:
			total_andht = total_andht + int(dict.get(i))
#		print total_andht
		for i in list_ios_property:
			total_iosht = total_iosht + int(dict.get(i))
#		print total_iosht
		total_and_ios_h = 0
		total_and_ios_h = total_andht + total_iosht
		str_tatol = ["合计"+"     "+str(total_andht)+"    "+str(total_iosht)+"    "+str(total_and_ios_h)]
		f.writelines(str_tatol)
#小版本更新及数据显示--------------------------------------------------------------------
if int((list_and_property[len(list_and_property)-1])[14:15])==int((list_ios_property[len(list_ios_property)-1])[14:15]):
	strx = "小版本更新"
	print strx.decode("utf-8")
	f=file("D:\\Active user data.txt","w+")
	a = int((list_and_property[len(list_and_property)-1])[14:15])
#	print a
	list_andxp = []
	list_iosxp = []
#	for i in list_and_property:
#		print i 
	for i in list_and_property:
		str1 = int(i[14:15])
		if str1==a:
			list_andxp[0:0] = [i]
			#print "rfrfg"
	#print len(list_andxp)
#	for i in list_andxp:
#		print i 
#		print list_andxp[1]
	for i in list_ios_property:
		str1 = int(i[14:15])
		if str1==a:
			list_iosxp[0:0]=[i]
#	for i in list_iosxp:
#		print i
	str1 = list_andxp[0]
	str2 = list_iosxp[0]
#	print str1
#	print str2
	
#	print str1[16:17]
#	print str1[18:19]
	
#	print and_f
#	print ios_f
	count1 = len(list_andxp)-1
#	print count1
	count2 = len(list_iosxp)-1
#	print count1
	count1_1 = 0
	count2_2 = 0
#	print count1
#	print count2
	while count1_1<=count1 or count2_2<=count2:
		if count1_1<count1 and count2_2<count2:
			and_f = int(list_andxp[count1_1][16:17] + list_andxp[count1_1][18:19])
			ios_f = int(list_iosxp[count2_2][16:17] + list_iosxp[count2_2][18:19])
#			print and_f
#			print ios_f
			if and_f==ios_f:
#				print "====="
				str_w = [list_andxp[count1_1][14:19]+"      "+str(dict.get(list_andxp[count1_1]))+"      "+str(dict.get(list_iosxp[count2_2]))+"      "+str(int(dict.get(list_andxp[count1_1]))+int(dict.get(list_andxp[count1_1])))+"\n"]
				f.writelines(str_w)
				count2_2 = count2_2 + 1
				count1_1 = count1_1 + 1
				continue
			if and_f>ios_f:
#				print ">>>>>"
				str_w = [list_andxp[count1_1][14:19]+"      "+str(dict.get(list_andxp[count1_1]))+"      "+"---"+"      "+str(dict.get(list_andxp[count1_1]))+"\n"]
				f.writelines(str_w)
				count1_1 = count1_1 + 1
				count2_2 = count2_2
				continue
			if and_f<ios_f:
#				print "<<<<<"
				str_w = [list_iosxp[count1_1][14:19]+"      "+"---"+str(dict.get(list_iosxp[count2_2]))+"      "+str(dict.get(list_iosxp[count2_2]))+"\n"]
				f.writelines(str_w)
				count2_2 = count2_2 + 1
				count1_1 = count1_1 
				continue
		if count1_1==count1 and count2_2<count2:
			and_f = int(list_andxp[count1_1][16:17] + list_andxp[count1_1][18:19])
			ios_f = int(list_iosxp[count2_2][16:17] + list_iosxp[count2_2][18:19])
			if and_f>ios_f:
				str_w = [list_andxp[count1_1][14:19]+"      "+str(dict.get(list_andxp[count1_1]))+"      "+"---"+str(dict.get(list_andxp[count1_1]))+"\n"]
				f.writelines(str_w)
				count1_1 = count1_1 + 1
				count2_2 = count2_2
				continue
			if and_f==ios_f:
				str_w = [list_andxp[count1_1][14:19]+"      "+str(dict.get(list_andxp[count1_1]))+"      "+str(dict.get(list_iosxp[count2_2]))+"      "+str(int(dict.get(list_andxp[count1_1]))+int(dict.get(list_andxp[count1_1])))+"\n"]
				f.writelines(str_w)
				count1_1 = count1_1 + 1
				count2_2 = count2_2 + 1
				continue
			if and_f<ios_f:
				str_w = [list_iosxp[count1_1][14:19]+"      "+"---"+"      "+str(dict.get(list_iosxp[count2_2]))+"      "+str(dict.get(list_iosxp[count2_2]))+"\n"]
				f.writelines(str_w)
				count2_2 = count2_2 + 1
				count1_1 = count1_1 
				continue
		if count1_1==count1 and count2_2==count2:
			and_f = int(list_andxp[count1_1][16:17] + list_andxp[count1_1][18:19])
			ios_f = int(list_iosxp[count2_2][16:17] + list_iosxp[count2_2][18:19])
			if and_f>ios_f:
				str_w = [list_andxp[count1_1][14:19]+"      "+str(dict.get(list_andxp[count1_1]))+"      "+"---"+str(dict.get(list_andxp[count1_1]))+"\n"]
				f.writelines(str_w)
				count1_1 = count1_1 + 1
				count2_2 = count2_2
				continue
			if and_f==ios_f:
				str_w = [list_andxp[count1_1][14:19]+"      "+str(dict.get(list_andxp[count1_1]))+"      "+str(dict.get(list_iosxp[count2_2]))+"      "+str(int(dict.get(list_andxp[count1_1]))+int(dict.get(list_andxp[count1_1])))+"\n"]
				f.writelines(str_w)
				count1_1 = count1_1 + 1
				count2_2 = count2_2 + 1
				break
			if and_f<ios_f:
				str_w = [list_iosxp[count1_1][14:19]+"      "+"---"+str(dict.get(list_iosxp[count2_2]))+"      "+str(dict.get(list_iosxp[count2_2]))+"\n"]
				f.writelines(str_w)
				count2_2 = count2_2 + 1
				count1_1 = count1_1 
				continue
		if count1_1>count1 and count2_2==count2:
			str_w = [list_iosxp[count2_2][14:19]+"      "+"---"+str(dict.get(list_iosxp[count2_2]))+"      "+str(dict.get(list_iosxp[count2_2]))+"\n"]
			f.writelines(str_w)
			count2_2 = count2_2 
			break
			
		if count1_1>count1 and count2_2<count2:
			str_w = [list_iosxp[count2_2][14:19]+"      "+"---"+str(dict.get(list_iosxp[count2_2]))+"      "+str(dict.get(list_iosxp[count2_2]))+"\n"]
			f.writelines(str_w)
			count2_2 = count2_2 + 1
			continue

		if count1_1<count1 and count2_2==count2:
			and_f = int(list_andxp[count1_1][16:17] + list_andxp[count1_1][18:19])
			ios_f = int(list_iosxp[count2_2][16:17] + list_iosxp[count2_2][18:19])
			if and_f>ios_f:
				str_w = [list_andxp[count1_1][14:19]+"      "+str(dict.get(list_andxp[count1_1]))+"      "+"---"+"     "+str(dict.get(list_andxp[count1_1]))+"\n"]
				f.writelines(str_w)
				count1_1 = count1_1 + 1
				count2_2 = count2_2
				continue
			if and_f==ios_f:
				str_w = [list_andxp[count1_1][14:19]+"      "+str(dict.get(list_andxp[count1_1]))+"      "+str(dict.get(list_iosxp[count2_2]))+"      "+str(int(dict.get(list_andxp[count1_1]))+int(dict.get(list_andxp[count1_1])))+"\n"]
				f.writelines(str_w)
				count1_1 = count1_1 + 1
				count2_2 = count2_2 + 1
				continue
			if and_f<ios_f:
				str_w = [list_iosxp[count1_1][14:19]+"      "+"---"+"      "+str(dict.get(list_iosxp[count2_2]))+"      "+str(dict.get(list_iosxp[count2_2]))+"\n"]
				f.writelines(str_w)
				count2_2 = count2_2 + 1
				count1_1 = count1_1 
				continue
		if  count1_1<=count1 and count2_2>count2:
			str_w = [list_andxp[count1_1][14:19]+"     "+str(dict.get(list_andxp[count1_1]))+"     "+"---"+"      "+str(dict.get(list_andxp[count1_1]))+"\n"]
			f.writelines(str_w)
			count1_1 = count1_1 + 1
			continue
	#输出历史版本统计数据：
	list_andls = []
	list_iosls = []
	for i in list_and_property:
		str1 = int(i[14:15])
		if a==str1:
			continue
		list_andls[0:0] = [i]
#	for i in list_andls:
#		print i 
	for i in list_ios_property:
		str1 = int(i[14:15])
		if a==str1:
			continue
		list_iosls[0:0]=[i]
#	for i in list_iosls:
#		print i
	countX = a-1
	while countX>2:
		#andX数据
		total_andX=0
		str6 = str(countX)
		for i in list_andls:
			if countX==int(i[14:15]):
				total_andX = total_andX + int(dict.get(i))
		str3 = str(total_andX)
#		print str3
		str5=str6+"X"+"       "+str3
#		print str5
		#iosX数据
		total_iosX=0
		str7 = str(countX)
		for i in list_iosls:
			if countX==int(i[14:15]):
				total_iosX = total_iosX + int(dict.get(i))
			str8 = str(total_iosX)
			total_X = total_andX + total_iosX
			str9 = str(total_X)
			str10=[str5+"   "+str8+"  "+str9+"\n"]
		f.writelines(str10)
		countX = countX-1
	#输出合计数据
	total_andht = 0
	total_iosht = 0
	for i in list_and_property:
		total_andht = total_andht + int(dict.get(i))
	print total_andht
	for i in list_ios_property:
		total_iosht = total_iosht + int(dict.get(i))
	print total_iosht
	total_and_ios_h = 0
	total_and_ios_h = total_andht + total_iosht
	str_tatol = ["合计"+"     "+str(total_andht)+"    "+str(total_iosht)+"    "+str(total_and_ios_h)]
	f.writelines(str_tatol)
	














