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





icode = raw_input('icode: ').decode('GBK').encode('utf-8')
title = raw_input('title: ').decode('GBK').encode('utf-8')
tags = raw_input('tags: ').decode('GBK').encode('utf-8')
content = raw_input('content: ').decode('GBK').encode('utf-8')
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
#构造图片name
image_name = icode + '.jpg'
#下载图片
urllib.urlretrieve(bigpic_url,image_name)
#上传封面缩略图到七牛云
qn_up_img(image_name,image_name)
#构造params的各个key值
# 2.en_title
en_title = icode.replace('-','')
#print en_title
# 3.img

img = 'http://7xpgaf.com1.z0.glb.clouddn.com/' + icode + '.jpg' + '?imageMogr2/thumbnail/685x685'
#print img
# 4.pub_time_0,获取当前时间
pub_time_0 = time.strftime('%Y/%m/%d',time.localtime(time.time()))
pub_time_1 = time.strftime('%H:%M',time.localtime(time.time()))
#print pub_time_0
# 5.content
content = '<p>' + content + '</p>'
content += '<div class="embed-responsive embed-responsive-4by3"><iframe class="embed-responsive-item" src="http://www.tudou.com/programs/view/html5embed.action?type=0&code=%s" allowtransparency="true" allowfullscreen="true" allowfullscreenInteractive="true" scrolling="no" border="0" frameborder="0" ></iframe></div>' % icode
#print content
_save = '保存'
params = {
		'title':title, 
		'en_title':en_title,
		'img':img,
		'category':'3', 
		'tags':tags,
		'author':'1',
		'rank':'0',
		'status':'0',
		'content':content,
		'summary':'',
		'pub_time_0':pub_time_0,
		'pub_time_1':pub_time_1,
		'_save':'保存'
}
#调用发文章接口
post_article(params)
