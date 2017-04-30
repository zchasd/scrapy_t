# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import os,sys
import urllib
import urllib2
import cookielib
import requests
from readability import Document


global agent
agent = {        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
params = {'username': 'Ryan', 'password': 'password'}
r = requests.post("http://pythonscraping.com/pages/cookies/welcome.php", params)
print("Cookie is set to:")
print(r.cookies.get_dict())         #r.cookies.get_dict() 为cookies
print("-----------")
print("Going to profile page...")
r = requests.get("http://pythonscraping.com/pages/cookies/profile.php",cookies=r.cookies)
print(r.text)




13.17.16




