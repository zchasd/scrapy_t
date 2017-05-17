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

def get_film_info(top100_html, films_info, current_page_num):
    for line in top100_html.find_all(attrs={'id':'asyncRatingRegion'}):
        film_rank = current_page_num*10
        for film_info in line.children:
            # title = str(filminfo)
            film_info = str(film_info)
            if len(film_info)>10:
                title = re.search('title="[^"]+"', film_info).group()[7:-1]
                films_info[title] = list()
                film_url = re.search('a href="[^"]+"', film_info).group()[8:-1]
                films_info[title].append(film_url)

                director = re.search('导演[^<]+<[^<]+</a>', film_info).group()[0:-4]
                director = director.split('>')[1]
                films_info[title].append(director)
                for a in re.finditer('主演[^<]+<[^<]+<[^<]+<[^<]+</a>', film_info):
                    a = a.group().split('</a>')
                    actor1 = a[0]
                    actor2 = a[1]
                    actor1 = actor1.split('>')[1]
                    films_info[title].append(actor1)
                    actor2 = actor2.split('>')[1]
                    films_info[title].append(actor2)
                try:
                    introduction = re.search('<p class="mt3">[^<]*</p>', film_info).group()[15:-4]
                except AttributeError:
                    introduction = '暂无影评'
                films_info[title].append(introduction)
                point1 = re.search('<span class="total">\d</span>', film_info).group()[-8]
                point2 = re.search('<span class="total2">\.\d</span>', film_info).group()[-8]
                point = int(point1) + float(point2)/10
                films_info[title].append(point)
                films_info[title].append(film_rank)
                film_rank += 1
                post = {
                    '电影名':title,
                    '网址':film_url,
                    '导演':director,
                    '主演':actor1+','+actor2,
                    '评分':point,
                    '排名':film_rank,
                }
                coll_film_info.insert(post)

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
    global comments_count
    comments_count += 1
    if comments_count%100==0:
        print comments_count
    return para

def allocate_film_url(url_list):
    global current_url_count
    with get_film_page_url_lock:
        current_url_count += 1
        return url_list[current_url_count]

def get_film_comment(url_list):
    while True:
        try:
            films_url = allocate_film_url(url_list)
        except:
            break
        comment_dict = dict()
        r1 = requests.get(str(films_url + 'comment.html'), headers=comment_page_head);
        film_page_html = BeautifulSoup(r1.text, "html.parser")
        try:
            film_page_html = str(film_page_html.find_all(attrs={'id': 'PageNavigator'})[0])
        except IndexError:
            comment_dict['error'] = 'error'
            comment_dict['网址'] = films_url
            coll_film_comment.insert(comment_dict)
            return comment_dict
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
        try:
            coll_film_comment.insert(comment_dict)
        except:
            print 'write_____db____errrrrrrrrrrrrror: ',films_url,film_title
    return comment_dict

def get_films_urls(url,films_info):
    for i in range(10):
        url_suffix = 'index-' + str(i+1) + '.html'
        if (i+1) == 1:
            r = requests.get(url, headers=head);
            html = BeautifulSoup(r.text, "html.parser")
            get_film_info(html, films_info, i)
        else:
            r = requests.get(url+url_suffix, headers=head);
            html = BeautifulSoup(r.text, "html.parser")
            get_film_info(html, films_info, i)

if __name__ == "__main__":
    films_info = dict()
    films_comment = dict()
    threads = []
    url_list = []
    current_url_count = -1
    comments_count = 0
    get_films_urls(top100_chinese_url,films_info)
    for i in range(40):
        t = Thread(target=get_film_comment, args=([films_info[title][film_url] for title in films_info],))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    client.close()




