#coding=utf-8
import urllib
import urllib2
import httplib
import cookielib
url = 'http://www.xxx.net/'
cookie = cookielib.CookieJar()
cj=urllib2.HTTPCookieProcessor(cookie)
#设置登录参数，使用浏览器的调试器等抓包工具得到
postdata=urllib.urlencode({'JSESSIONID':'1F616774D9548C1E8AF12A65B470B663', 'username':'admin','password':'admin'})
#生成请求
request=urllib2.Request(url, postdata)
#设置代理
request.set_proxy('xx.xx.xx.xx:xx','http')
#登录
opener=urllib2.build_opener(cj)
urllib2.install_opener(opener)

html=opener.open(request)
print html.read()

#打开数据页面开始采集数据
s = urllib2.urlopen('http://www.xx.net').read()

request = urllib2.Request(url)
set_cookie = urllib2.urlopen(request).info()['Set-Cookie']
json_id = set_cookie.split(';')[0]#JSESSIONID=3037DCDF69A6454FC525E38C41E6B611
json_id = json_id.split('=')[-1]
print json_id
