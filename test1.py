# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import os,sys
import urllib
import urllib2
import cookielib
import requests
import re
import pymongo
from threading import Thread, Lock
from time import sleep
from readability import Document

film_url,director,actor1,actor2,introduction,point,rank = 0,1,2,3,4,5,6     #define
top100_chinese_url = 'http://www.mtime.com/top/movie/top100_chinese/'
head = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'www.mtime.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
}
comment_page_head = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
}
get_film_page_url_lock = Lock()
client = pymongo.MongoClient('localhost', 27017)
db = client['mtime_db']
coll_film_info = db['film_info']
coll_film_comment = db['film_comment']

r2 = requests.get('http://movie.mtime.com/12142/reviews/3820558.htmlempty', headers=comment_page_head);

film_page_html = BeautifulSoup(r2.text, "html.parser")
film_page_html = str(film_page_html.find_all(attrs={'class': 'db_mediacont db_commentcont'})[0])
delet_html_table_re = re.compile('(<[^>]*>)|[\s]+|(\n)')
para = delet_html_table_re.sub(r'', film_page_html)




