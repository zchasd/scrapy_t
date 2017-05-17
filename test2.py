# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import os,sys
import urllib
import urllib2
import cookielib
import requests
import re
from readability import Document
import time
from threading import Thread, Lock
import copy
import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client['mtime_db']
coll_film_info = db['film_info']
coll_film_comment = db['film_comment']


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
def get_comment_text(review_url):
    r2 = requests.get(review_url, headers=comment_page_head);
    try:
        film_page_html = BeautifulSoup(r2.text, "html.parser")
        film_page_html = str(film_page_html.find_all(attrs={'class': 'db_mediacont db_commentcont'})[0])
        delet_html_table_re = re.compile('(<[^>]*>)|[\s]+|(\n)')
        para = delet_html_table_re.sub(r'', film_page_html)
    except:
        para = 'empty review or url access error'
        print review_url + para

    return para




films_url = 'http://movie.mtime.com/10190/'
comment_dict = dict()
r1 = requests.get(str(films_url + 'comment.html'), headers=comment_page_head);
film_page_html = BeautifulSoup(r1.text, "html.parser")
try:
    film_page_html = str(film_page_html.find_all(attrs={'id': 'PageNavigator'})[0])
except IndexError:
    print  'error'
try:
    max_page = int(re.search('\d{1,2}(?=</a><a class="ml10 next")', str(film_page_html)).group())
except AttributeError:
    max_page = 1
for i in range(max_page):
    if i + 1 == 1:
        url_suffix = 'comment.html'
    else:
        url_suffix = 'comment-' + str(i + 1) + '.html'
    films_url_ = films_url
    films_url_ += url_suffix
    r1 = requests.get(films_url_, headers=comment_page_head);
    film_page_html = BeautifulSoup(r1.text, "html.parser")
    try:
        film_title = \
    re.search('(?<=<h1 property="v:itemreviewed"><a href="http://movie.mtime.com/)[^>]*>[^<]*(?=</a>)',
              str(film_page_html)).group().split('>')[1]
    except:
        print '____errrrrrrrrrrrrror: ', films_url, film_title

    comment_dict['电影名'] = film_title
    comment_dict['网址'] = films_url
    film_page_html = film_page_html.find_all(attrs={'id': 'reviewRegion'})[0]
    for comments_div_html in film_page_html.children:
        comments_div_html = str(comments_div_html)
        if len(comments_div_html) > 10:
            review_title = re.search('(?<=<a href=")[^<]*(?=</a)', comments_div_html).group().split('">')[1]
            review_title = re.sub('\s|\.|_', '', review_title)
            review_url = re.search('(?<=<a href=")[^"]*(?=" )', comments_div_html).group()
            review_text = get_comment_text(review_url)
            comment_dict[review_title] = review_text


# coll_film_comment.insert(comment_dict)

