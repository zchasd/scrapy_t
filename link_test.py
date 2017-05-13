# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import os,sys
import urllib
import urllib2
import cookielib
import requests
import re
from time import sleep
from readability import Document
import HTMLParser

films_url = 'http://movie.mtime.com/10190/'
comment_page_head = {

    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
}


def get_comment_text(review_url):
    text = ''
    r2 = requests.get(review_url, headers=comment_page_head);
    film_page_html = BeautifulSoup(r2.text, "html.parser")
    film_page_html = str(film_page_html.find_all(attrs={'class': 'db_mediacont db_commentcont'})[0])
    delet_html_table_re = re.compile('(<[^>]*>)|[\s]+|(\n)')
    para = delet_html_table_re.sub(r'', film_page_html)
    return para


r1 = requests.get(str(films_url+'comment.html'), headers=comment_page_head);
film_page_html = BeautifulSoup(r1.text, "html.parser")
film_page_html = str(film_page_html.find_all(attrs={'id':'PageNavigator'})[0])
max_page = int(re.search('\d{1,2}(?=</a><a class="ml10 next")', film_page_html).group())
for i in range(max_page):
    if i+1 == 1:
        url_suffix = 'comment.html'
    else:
        print "===========asdfasdfasdf++++++++++++"
        sleep(0.5)

        url_suffix = 'comment-'+str(i+1)+'.html'
    films_url_ = films_url
    films_url_ += url_suffix
    print films_url_
    r1 = requests.get(films_url_, headers=comment_page_head);
    film_page_html = BeautifulSoup(r1.text, "html.parser")
    film_page_html = film_page_html.find_all(attrs={'id':'reviewRegion'})[0]
    for comments_div_html in film_page_html.children:
        comments_div_html = str(comments_div_html)
        if len(comments_div_html) > 10:
            print '-----------------------------------'
            review_title = re.search('(?<=<a href=")[^<]*(?=</a)', comments_div_html).group().split('">')[1]
            print review_title
            review_url = re.search('(?<=<a href=")[^"]*(?=" )', comments_div_html).group()
            print review_url
            review_text = get_comment_text(review_url)
            print review_text
            sleep(0.5)
    print '-----------------------------------------\n'