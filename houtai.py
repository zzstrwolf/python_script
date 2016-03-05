# -*- coding: utf-8 -*-
import os
import re
from django.utils import timezone
import django
import sys
#把web项目根目录加入到sys.path
sys.path.append('D:/vmaig_blog')
django.setup()
from blog.models import Article,Category
from vmaig_auth.models import VmaigUser

#begin
#获得用户strwolf
author = VmaigUser.objects.get(pk=1)
category = Category.objects.get(pk=1)
#cat.name可以取得value
title = u'[Beautyleg] 美腿寫真 No.663 Jill 2012.04.09 [62P]'
num = re.search(ur'No\.(\d+?)[^\d]',title).group(1)
en_title = 'beautylg_photo_%s' % num
tags = ''
summary = ''
pub_time = timezone.now()
#构造content
#原始图片文件夹
raw_pic_dir = u'/static/img/[Beautyleg] 美腿寫真 No.663 Jill 2012.04.09 [62P]/'
#缩略图片文件夹
thub_pic_dir = u'/static/img/thub2/'
#该期图片总数
pic_num = len(os.listdir('D:\\vmaig_blog\\blog\\static\\img\\thub2'))
i = 1
content = ''
while i <= pic_num:
    if i == 1:
        content += u'<p><a class="lightview" href="%s%d.jpg" data-lightview-group-options="controls: { close: false , slider: false },spacing: {relative: { horizontal: 60, vertical: 0 },thumbnails: { horizontal: 60, vertical: 0 },top: { horizontal: 60, vertical: 0 }}," data-lightview-group="example"> <img src="%s%d.jpg" alt="" /></a> ' % (raw_pic_dir,i,thub_pic_dir,i)
        i += 1
        continue
    if i > 1 and i % 3 == 1:
        content += u'<p><a class="lightview" href="%s%d.jpg" data-lightview-group="example"><img src="%s%d.jpg" alt="" /></a> ' % (raw_pic_dir,i,thub_pic_dir,i)
        i += 1
        continue
    if i % 3 == 2:
        content += u'<a class="lightview" href="%s%d.jpg" data-lightview-group="example"><img src="%s%d.jpg" alt="" /></a> ' % (raw_pic_dir,i,thub_pic_dir,i)
        i += 1
        continue
    if i % 3 == 0:
        content += u'<a class="lightview" href="%s%d.jpg" data-lightview-group="example"><img src="%s%d.jpg" alt="" /></a></p>' % (raw_pic_dir,i,thub_pic_dir,i)
        i += 1
        continue
if pic_num % 3 == 0:
    pass
else:
    content += u'</p>'
#print content
#构造Article类写入数据库
a = Article(author = author,category = category,title = title,en_title = en_title,tags = tags, summary = summary,content = content, pub_time = pub_time)
a.save()

#print Article.objects.all()

