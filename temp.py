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
import pprint
import matplotlib.pyplot as plt

client = pymongo.MongoClient('localhost', 27017)
db = client['mtime_db']
coll_film_info = db['film_info']
coll_film_com = db['film_comment']
info = []
com = []
asd = []
# for x in coll_film_com.find({},{u'电影名':u'霸王别姬'}):
#      print x
print coll_film_com.find({u'电影名':u'霸王别姬'}).count()

