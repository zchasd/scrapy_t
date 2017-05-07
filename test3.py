# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import os,sys
import urllib
import urllib2
import cookielib
import requests
import re
from readability import Document

head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'jwxt.shmtu.edu.cn',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://cas.shmtu.edu.cn',
    'Referer':'http://jwxt.shmtu.edu.cn/shmtu/login.action',

}
params = {
    'username': '201310311036',
    'password': '156010',

    'lt': 'LT-AlwaysValidTicket',
    'encodedPassword': '',
}
r1 = requests.get('http://jwxt.shmtu.edu.cn/shmtu/login.action',headers=head)
print r1.headers
head['Cookie']='JSESSIONID=9C10A288886A3E583FF487E79208DF1B; SVRNAME=xk14'#r1.headers['Set-Cookie']

r2 = requests.post("http://jwxt.shmtu.edu.cn/shmtu/login.action", params, headers=head)
print r2.text