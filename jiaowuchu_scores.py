# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import os,sys
import urllib
import urllib2
import cookielib
import requests
import re
from readability import Document


global agent
head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    # 'Content-Length':'4803',
    'Connection': 'keep-alive',
    'Host': 'jwxt.shmtu.edu.cn',
    'Upgrade-Insecure-Requests': '1',
    # 'Content-Type': 'application/x-www-form-urlencoded',
    # 'Origin': 'https://cas.shmtu.edu.cn   ',
    'Referer':'http://jwc.shmtu.edu.cn/LinkText.aspx?id=b47acdbc-d1e4-41a5-a29b-e9c8d6437c31',
    'Cookie':'UM_distinctid=15be302509f4a8-0b6ff19d924031-871133d-1fa400-15be30250a05d2',
}
params = {
    'username': '201310311036',
    'password': '156010',
    '_eventId': 'submit',
    'signin': '登录',
    'lt': '',
    'execution': '',
}
r = requests.get("http://jwxt.shmtu.edu.cn/shmtu/home.action", headers=head)
# r = requests.post("https://cas.shmtu.edu.cn/cas/login", params, headers=head    )
print r.headers
rcookies = r.cookies
# print(r.text)
html = BeautifulSoup(r.text, "html.parser")
html = html.findAll(attrs = {'type': 'hidden'})
for h in html:
    print h
print '------------------------------------------'
findlt = re.compile(r'(?<=name="lt" type="hidden" value=")[^>]*(?="/>)')
params['lt'] = findlt.findall(str(html))[0]
findexecution = re.compile(r'(?<=name="execution" type="hidden" value=")[^>]*(?="/>)')
params['execution'] = findexecution.findall(str(html))[0]

# head['Cookie']=r.headers['Set-Cookie']
head['Cookie']='JSESSIONID=B4F9B45C3DB33B622C8C59A4E7951F6A'

r1 = requests.post("https://cas.shmtu.edu.cn/cas/login?service=http%3A%2F%2Fjwxt.shmtu.edu.cn%2Fshmtu%2Fhome.action", params, headers=head)
# print r1.text
head['Cookie']=r1.headers['Set-Cookie']
r2 = requests.get('http://jwxt.shmtu.edu.cn/shmtu/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR',headers=head)
print r.headers
print r1.headers
print '--------\n'
print r.cookies
print r1.cookies
print r2.text

print '----------------------------------------------'





