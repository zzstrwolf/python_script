# -*- coding:utf-8 -*-

import os

image_dir = 'D:\\BaiduYunDownload\\[Be]2016.02.24 No.1258\\[Be]2016.02.24 No.1258 Alice[56P383M]'
images = os.listdir(image_dir)
i = 1
for img in images:
	os.rename(os.path.join(image_dir,img),os.path.join(image_dir,'%s.jpg' % i))
	i += 1