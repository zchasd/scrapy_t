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
    'Content-Length':'4803',
    'Connection': 'keep-alive',
    'Host': 'cas.shmtu.edu.cn',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://cas.shmtu.edu.cn',
    'Referer':'https://cas.shmtu.edu.cn/cas/login?service=http%3A%2F%2Fjwxt.shmtu.edu.cn%2Fshmtu%2Fhome.action',
    # 'Cookie':'UM_distinctid=15be302509f4a8-0b6ff19d924031-871133d-1fa400-15be30250a05d2',
}
params = {
    'username': '201310311036',
    'password': '156010',
    '_eventId': 'submit',
    'signin': '登录',
    'lt': '',
    'execution': '',
}
r = requests.get("https://cas.shmtu.edu.cn/cas/login", headers=head)
# r = requests.post("https://cas.shmtu.edu.cn/cas/login", params, headers=head    )
print r.text
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

head['Cookie']=r.headers['Set-Cookie']

r1 = requests.post("https://cas.shmtu.edu.cn/cas/login", params, headers=head)
print r1.text


print r.headers
print r1.headers
print '--------\n'
print r.cookies
print r1.cookies

dictMerged=dict(r.cookies.get_dict(), **r1.cookies.get_dict())
Cookie = 'TGC='+ dictMerged['TGC'] + '; JSESSIONID=' + dictMerged['JSESSIONID']
print Cookie
print '------r2:------'
head['Cookie']=Cookie
# data1 = {
#     'Accept':'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'Connection': 'keep-alive',
#     #'Referer':'http://jwxt.shmtu.edu.cn/shmtu/login.action',
#     'Accept-Encoding': 'gzip, deflate, sdch, br',
#     'Accept-Language': 'zh-CN,zh;q=0.8',
#     'Connection': 'keep-alive',
#     'Host': 'jwxt.shmtu.edu.cn',
#     'Upgrade-Insecure-Requests':'1',
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
#
# }
r2 = requests.get("https://cas.shmtu.edu.cn/cas/login?service=http%3A%2F%2Fjwxt.shmtu.edu.cn%2Fshmtu%2FstudentDetail.action%3Bjsessionid%3D81BA4A3FAF8B53F5F5B9",headers=head)
print r2.headers
# data1 = {
#     'Accept':'Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'Connection': 'keep-alive',
#     #'Referer':'http://jwxt.shmtu.edu.cn/shmtu/login.action',
#     'Accept-Encoding': 'gzip, deflate, sdch, br',
#     'Accept-Language': 'zh-CN,zh;q=0.8',
#     'Cache-Control': 'max-age=0',
#     'Connection': 'keep-alive',
#     'Cookie':  'JSESSIONID=DFD94859B18780E778C76F00AEE8CCAB; UM_distinctid=15b100b29433dc-0bcecbd86dc29a-396b4c0b-1fa400-15b100b29447ab; _gscu_1865196914=90682755qfvb4486; SVRNAME=xk11',
#     'Host': 'jwxt.shmtu.edu.cn',
#     'Upgrade-Insecure-Requests':'1',
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
#
# }
data1 = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
    #'Referer':'http://jwxt.shmtu.edu.cn/shmtu/login.action',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie':   'JSESSIONID=AFE4BE6423C6E5A64A9310A29B98C242; Path=/shmtu/; HttpOnly;SVRNAME=xk13; path=/'  ,
    'Host': 'jwxt.shmtu.edu.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',

}
print '----------------------------------------------'
# r2 = requests.get("http://jwxt.shmtu.edu.cn/shmtu/studentDetail.action", headers=data1)
# print r2.text

# print 'cookies: ', r.cookies
# print 'cookies: ', r1.cookies
# print 'cookies: ', r2.cookies





