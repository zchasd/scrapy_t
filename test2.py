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


L = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print L[-2::-2]
print L[-2:2:-2]