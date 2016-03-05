# -*- coding: utf8 -*-

import os 
import urllib2
import urllib
import cookielib
import re
import json
import time
from email.mime.text import MIMEText
from email.header import Header
import smtplib

f = open(u'D:\\QQ群营销\\魅力高跟街拍.txt')
info = f.read()
re_qq = re.compile(r'\((.+?)\)')
f.close()
qq_list = re.findall(re_qq,info)
qqmail_list = map(lambda x:x + '@qq.com',qq_list)

f = open('qqmail_list.txt','a')
for qqmail in qqmail_list:
	f.write(qqmail + '\n')
f.close()




msg = MIMEText(u'<html><body>百度【秀色驿站】，Vx公众号【秀色驿站】</body></html>', 'html', 'utf-8')
msg['Subject'] = Header(u'秀色驿站', 'utf-8').encode()
from_addr = {{yours}}
password = {{yours}}
smtp_server = 'smtp.163.com'


server = smtplib.SMTP(smtp_server, 25)
#server.set_debuglevel(1)
server.login(from_addr, password)
for qqmail in qqmail_list:
	i = 0
	while True:
		try:
			if i == 5:
				break
			server.sendmail(from_addr, [qqmail], msg.as_string())
			print '%s sussess!' % qqmail
			break
		except:
			i += 1
			time.sleep(61)
server.quit()

