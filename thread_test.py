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

# _*_ coding:utf8 _*_
import time
from threading import Thread, Lock


films_info = {
    'asd1':{'url':'http://1'},
    'asd2':{'url':'http://2'},
    'asd3':{'url':'http://3'},
    'asd4':{'url':'http://4'},
    'asd5':{'url':'http://5'},
    'asd6':{'url':'http://6'},
    'asd7':{'url':'http://7'},
    'asd8':{'url':'http://8'},
    'asd9':{'url':'http://9'},
    'asd10':{'url':'http://10'},
}
get_film_page_url_lock = Lock()
def get_film_page_url(url_list):
    global current_url_count
    with get_film_page_url_lock:
        current_url_count += 1
        return url_list[current_url_count]



def get_comment(url_list):
    while True:
        try:
            print get_film_page_url(url_list)
        except:
            return



threads = []
url_list = []
for title in films_info:
    url_list.append(films_info[title]['url'])
current_url_count = -1
for i in range(3):
    t = Thread(target=get_comment,args=(url_list,))
    t.start()
    threads.append(t)
for t in threads:
    t.join()


# value = 0
# lock = Lock()
# def getlock():
#     global value
#     with lock:
#         new = value + 1
#         time.sleep(0.001)
#         value = new
# threads = []
# for i in range(100):
#     t = Thread(target=getlock)
#     t.start()
#     threads.append(t)
# for t in threads:
#     t.join()
# print value