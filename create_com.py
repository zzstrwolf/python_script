# -*- coding:utf-8 -*-

# -*- coding:utf-8 -*-

import os


file_name = os.listdir(os.getcwd())
folder_name=[]
for fn in file_name:
	if os.path.isdir(fn):
		folder_name.append(fn)
for folder in folder_name:
	#在每个文件夹下找到图片名的集合
	sub_dir = os.path.join(os.getcwd(),folder)
	img_name = os.listdir(sub_dir)
	#print img_name
	for img in img_name:
		com_dir = os.path.join(sub_dir,img)
		fw = open('com.txt','a')
		fw.write(com_dir + '\n')
		fw.close()