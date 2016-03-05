# -*- coding:utf-8 -*-

import qiniu
import os
import cookielib
import json
from poster.encode import multipart_encode,MultipartParam
from poster.streaminghttp import register_openers
import requests
import poster
import time
from PIL import Image
import socket
import sys
import urllib
import urllib2
import re
import datetime

from qn_func import qn_up_img,post_article



#pub_date = datetime.date(2016,01,10)
rep = urllib2.urlopen("http://www.tudou.com/crp/plist.action?jsoncallback=page_play_model_pListModelList__findAll&lcode=8UJ5BsBRjqQ&app=2")
#print rep.read().decode('utf-8')
vlist = rep.read()
re_icode = re.compile(r'"icode":"(.+?)"')
icode_list = re.findall(re_icode,vlist)
#print icode_list,len(icode_list)
#构造API，获取视频缩略图
#这个API得到仍然是json，要去抓取bigpic的地址
for icode in icode_list[-1:]:
	req_thu = urllib2.urlopen('http://api.tudou.com/v3/gw?method=item.info.get&appKey=cb474a89091f33e1&format=json&itemCodes=%s' % icode)
	#每分钟只能调用100次API
	time.sleep(0.61)
	video_info = req_thu.read()
	#获取缩略大图
	re_bigpic = re.compile(r'"bigPicUrl":"(.+?)"')
	try:
		bigpic_url = re.search(re_bigpic,video_info).group(1)
	except:
		print 'Error',icode
		continue
	#获取title的期数
	re_inst = re.compile(r'No.(\d+?)\D')
	try:
		video_inst = re.search(re_inst,video_info).group(1)
	except:
		print 'Error',icode
		continue
	#构造图片name
	image_name = 'beautyleg_v_' + video_inst + '.jpg'
	#下载图片
	urllib.urlretrieve(bigpic_url,image_name)
	#上传封面缩略图到七牛云
	qn_up_img(image_name,image_name)
	#构造params的各个key值
	# 1.title
	re_title = re.compile(r'(No.+?)"')
	try:
		title_raw = re.search(re_title,video_info).group(1)
	except:
		print 'Error',icode
		continue
	title = title_raw.replace('-',' ')
	#print title
	# 2.en_title
	en_title = 'beautyleg_v_' + video_inst
	#print en_title
	# 3.img
	
	img = 'http://7xpgaf.com1.z0.glb.clouddn.com/' + en_title + '.jpg' + '?imageMogr2/thumbnail/685x685'
	#print img
	# 4.pub_time_0
	re_date = re.compile(r'\d{4}\.\d{2}\.\d{2}')
	pub_date = re.search(re_date,video_info).group()
	pub_time_0 = pub_date.replace('.','/')
	#print pub_time_0
	# 5.content
	content = '<div class="embed-responsive embed-responsive-4by3"><iframe class="embed-responsive-item" src="http://www.tudou.com/programs/view/html5embed.action?type=0&code=%s" allowtransparency="true" allowfullscreen="true" allowfullscreenInteractive="true" scrolling="no" border="0" frameborder="0" ></iframe></div>' % icode
	#print content
	_save = '保存'
	params = {
			'title':title, 
			'en_title':en_title,
			'img':img,
			'category':'2', 
			'tags':'',
			'author':'1',
			'rank':'0',
			'status':'0',
			'content':content,
			'summary':'',
			'pub_time_0':pub_time_0,
			'pub_time_1':'13:13',
			'_save':'保存'
	}
	#调用发文章接口
	post_article(params)
