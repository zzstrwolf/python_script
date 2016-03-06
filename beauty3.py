# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import time
import sys
import os
import socket


def getHtml(url):
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }
	i = 0
	while i < 1:
		try:
			request = urllib2.Request(url,headers = headers)
			response = urllib2.urlopen(request)
			html = response.read()
			response.close()
			#page = urllib.urlopen(url)
			#html = page.read()
			#page.close()
			i += 1 
		except:
			print u'打开网页失败，请检查网络'
			time.sleep(2)
	return html
		
	


def getImg(html,name,x):
	reg = r'border=0 src=(.+?\.jpg) alt='
	imgre = re.compile(reg)
	imglist = re.findall(imgre,html)
	if imglist!=[]:
		#print imglist
		i = 0
		n = len(imglist)
		path = name + '\\' + '%s.jpg'
		flag = 0                                                     #用于提示语的控制
		while i < n:
			try:
				urllib.urlretrieve(imglist[i],path % x)
				i += 1
				time.sleep(1)
				x += 1
				flag = 0
			except:
				if flag == 0:
					print u'请等待...'
				if flag == 20:
					print u'下载出错，仍然尝试下载中，可继续等待或稍后再试'
				flag += 1
				time.sleep(5)
	return x
	
#重新写一种下载图片的方式，感觉urlretrieve这个函数有问题
def getImg2(html,name,x):
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
	headers = { 'User-Agent' : user_agent }
	reg = r'border=0 src=(.+?\.jpg) alt='
	imgre = re.compile(reg)
	imglist = re.findall(imgre,html)
	if imglist!=[]:
		#print imglist
		i = 0
		n = len(imglist)
		
		flag = 0                                                     #用于提示语的控制
		while i < n:
			try:
				request = urllib2.Request(imglist[i],headers = headers)
				response = urllib2.urlopen(request)
				print 'test0'
				data = response.read()
				response.close()
				print 'test1'
				path = name + '\\' + str(x) + '.jpg'
				f = open(path,'wb')
				f.write(data)
				f.close()
				i += 1
				time.sleep(1)
				x += 1
				flag = 0
			except:
				print flag
				if flag == 0:
					print u'请等待...'
				if flag == 200:
					print u'下载出错，仍然尝试下载中，可继续等待或稍后再试'
				flag += 1
				time.sleep(5)
	return x
	




#主函数	

#socket.setdefaulttimeout(20)
html = getHtml('http://www.umei.cc/tags/BeautyLeg.htm')
#print html
re1 = r'href=(.+?\.htm)\starget=_blank><SPAN>.+?\n.+?title=\"(.+?)\"'
girl_html_re = re.compile(re1)
girl_html_list = re.findall(girl_html_re,html)
print girl_html_list
for girl_html in girl_html_list:
	name = girl_html[1].strip()
	isExists = os.path.exists(name)
	if not isExists:
		x = 1
		print u'正在下载',name
		os.makedirs(name)
		html_every_girl = getHtml(girl_html[0])
		x = getImg2(html_every_girl,name,x)
		re2 = r'href=\'(.+?\.htm)\'\s'
		page_girl_html_re = re.compile(re2)
		page_list = re.findall(page_girl_html_re,html_every_girl)
		for page in page_list:
			final_html = getHtml('http://www.umei.cc/p/gaoqing/gangtai/%s' % page)
			x = getImg2(final_html,name,x)
	else:
		print name,u'已存在'

raw_input('全部下载完成！请按回车退出'.decode('utf-8').encode('GBK'))
	
	