# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import os,sys
import urllib
import urllib2
import cookielib
import requests
from readability import Document



data1 = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
    #'Referer':'http://jwxt.shmtu.edu.cn/shmtu/login.action',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie':   'JSESSIONID=7030C4152E5FFA3CA036074DA90DB331; Path=/shmtu/; HttpOnly;SVRNAME=xk13; path=/'  ,
    'Host': 'jwxt.shmtu.edu.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',

}



print '----------------------------------------------'
r2 = requests.get("http://jwxt.shmtu.edu.cn/shmtu/studentDetail.action", headers=data1)
print r2.text








# global agent
# agent = {        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
# params = {'username': 'Ryan', 'password': 'password'}
# r = requests.post("http://pythonscraping.com/pages/cookies/welcome.php", params)
# print("Cookie is set to:")
# print(r.cookies.get_dict())         #r.cookies.get_dict() 为cookies
# print("-----------")
# print("Going to profile page...")
# r = requests.get("http://pythonscraping.com/pages/cookies/profile.php",cookies=r.cookies)
# print(r.text)









