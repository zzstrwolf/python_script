# -*- coding:utf-8 -*-

import os
import re

re_user = re.compile(r'(.+?)@')
re_pw = re.compile(r'----(.+)$')
re_domain = re.compile(r'@(.+?)-')
fr = open(u'D:\\QQ群营销\\600email.txt')
fw = open(u'D:\\QQ群营销\\600email_record.txt','a')
for raw_email in fr:
	user = re.search(re_user,raw_email).group(1)
	pw = re.search(re_pw,raw_email).group(1)
	domain = re.search(re_domain,raw_email).group(1)
	smtp_addr = 'smtp.' + domain
	email = user + '@' + domain
	recode = ','.join(['Y',email,user,pw,smtp_addr,'25','N'])
	fw.write(recode + '\n')
fr.close()
fw.close()

