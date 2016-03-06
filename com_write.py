# -*- coding:utf-8 -*-
import os

file_name = os.listdir(os.getcwd())
folder_name=[]
fw = open('com.txt','a')
for fn in file_name:
	if os.path.isdir(fn):
		fw.write(fn + '\n')
fw.close()