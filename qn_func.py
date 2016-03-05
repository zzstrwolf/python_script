# -*- coding:utf-8 -*-

import qiniu
import os
import re
import urllib
import urllib2
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

def qn_up_img(file_path,uped_name):
    qiniu_access_key = {{yours}}
    qiniu_secret_key = {{yours}}
    qiniu_bucket_name = {{yours}}

    q = qiniu.Auth(qiniu_access_key,qiniu_secret_key)
    key = uped_name
    mime_type = "image/jpeg"
    params = {'x:a': 'a'}
    localfile = file_path

    token = q.upload_token(qiniu_bucket_name, key)
    ret, info = qiniu.put_file(token, key, localfile, mime_type=mime_type, check_crc=True)
    #print info
    assert ret['key'] == key
    assert ret['hash'] == qiniu.etag(localfile)

def log_in(username,pwd,csrfmiddlewaretoken):
    paras = {'username':username,'password':pwd,'csrfmiddlewaretoken':csrfmiddlewaretoken,'next':'/admin/'}
    req = urllib2.Request('http://121.42.175.88/admin/login/?next=/admin/',urllib.urlencode(paras))
    req.add_header('Accept-Language','zh-CN,zh;q=0.8')
    req.add_header('Connection','keep-alive')
    req.add_header('Content-Type','application/x-www-form-urlencoded')
    req.add_header('Host','121.42.175.88')
    req.add_header('Origin','http://121.42.175.88')
    req.add_header('Referer','http://121.42.175.88/admin/login/?next=/admin/')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')
    ret = urllib2.urlopen(req)

#获取django管理后台的csrftoken
def get_csrf(url):
    rep = urllib2.urlopen(url)
    log_page = rep.read()
    re_csrf = re.compile(r"name='csrfmiddlewaretoken' value='(.+?)'")
    csrfmiddlewaretoken = re.search(re_csrf,log_page).group(1)
    return csrfmiddlewaretoken

def post_article(params): 
    #绑定cookie，自动处理cookie
    cj = cookielib.LWPCookieJar()
    #生成一个带cookie的opener，可以使用opener.open()打开URL
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    #安装opener，使得可以直接用urllib2.urlopen()带上cookie
    urllib2.install_opener(opener)
    #获取csrfmiddlewaretoken
    csrfmiddlewaretoken = get_csrf('http://121.42.175.88/admin/login/?next=/admin/')
    username = {{yours}}
    pwd = {{yours}}
    log_in(username,pwd,csrfmiddlewaretoken)

    #获取add页面的csrf
    csrfmiddlewaretoken = get_csrf('http://121.42.175.88/admin/blog/article/add/')

    params['csrfmiddlewaretoken'] = csrfmiddlewaretoken
    
    #print params

    items = []
    for key,value in params.items():
        items.append(MultipartParam(key,value))

    opener = poster.streaminghttp.register_openers()  
    opener.add_handler(urllib2.HTTPCookieProcessor(cj))
        
    #这里只有name-value对，直接用dict就可以成功
    #stackflow上提到如果上传键值对和文件，键值对先要封装成MultipartParam类
    #这里我持怀疑态度，官方说MultipartParam类处理独立的一对键值对
    #这里使用封装后的items也可以的
    datagen, headers = multipart_encode(params)


    additionalHeaders = {
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Host':'121.42.175.88',
        'Origin':'http://121.42.175.88',
        'Referer':'http://121.42.175.88/admin/blog/article/add/',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
    }

    for key,value in additionalHeaders.iteritems():
        headers[key] = value
     
    req = urllib2.Request('http://121.42.175.88/admin/blog/article/add/', datagen, headers)

    ret = urllib2.urlopen(req)