# -*- coding:utf-8 -*-
# from urllib.request import *
from bs4 import BeautifulSoup
import urllib
import urllib2
import scrapy
import re
from readability import Document
import glob
import math
import os

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

global agent
agent = {        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}

def gethttp(max):
    url = 'http://news.baidu.com/ns?'
    pagecount = 0
    while pagecount<(max-1):
        values = {
            'word':'特朗普',#关键字
            'rn':'10',#显示条数
            'cl':'2',#网页搜索
            'pn':str(pagecount)#从第pn项开始展示
        }
        data=urllib.urlencode(values)
        req = urllib2.Request(url+data, headers=agent)
        response = urllib2.urlopen(req)
        html = response.read()
        html = BeautifulSoup(html, "html.parser")
        html = html.findAll('h3', attrs={'class':'c-title'})
        html = str(html)
        findhttp_re = re.compile(r'(?<=href=")http://\S*(?=" )')
        httplist = []
        for m in findhttp_re.finditer(html):
            x = m.group()
            httplist.append(x)
        yield httplist
        pagecount += 20

def clearpath():
    rootpath = 'baidu_result\\*.txt'  # 'result' + '\\' + '*' + 'txt'
    pathlist = glob.glob(rootpath)  # 读取该路径下所有txt文件的路径
    for path in pathlist:
        os.remove(path)

def writefile(no, title, article, http): #no 是编号，文件名
    file = open('baidu_result\\' + str(no) + '.txt', 'w')
    file.write(title + '\n' + http + '\n' + article)

if __name__ == "__main__":
    httplist = list()
    clearpath()  # 清空文件夹
    i = 0
    for httplist_ in gethttp(5000):   #从百度新闻上爬取新闻链接
        for http in httplist_:
            print str(i), ': ', http
            article = '1'
            try:
                req = urllib2.Request(http, headers=agent)
                html = urllib2.urlopen(req)
                html = html.read()
                article = Document(html).summary()      #提取正文
                title = Document(html).short_title()    #提取标题
                html = str(BeautifulSoup(html, "html.parser"))
                dr = re.compile(r'<[^>]+>')             #定义正则
                article = dr.sub('', article)           #去除html标签
                article = article.replace(' ', '')      #去除空格
                article = article.replace('\n', '')     #去除换行
            except Exception,e:
                title = http
                article = 'HTTPError'

            print title    #标题打印到屏幕上
            writefile(i, title, article, http)      #创建txt，写入
            i += 1








