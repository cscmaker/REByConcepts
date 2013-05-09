#!/usr/bin/python
#-*-coding:utf-8-*-
import os, threading, re, time
import urllib2, urllib, sgmllib
import nltk
from goose import Goose

from readability.readability import Document
import sys
if not '/home/csc/project' in sys.path:
  sys.path.append('/home/csc/project')
import tools

from BeautifulSoup import BeautifulSoup
def grabHref(url):
  urls = []
  print url
  html = urllib.urlopen(url).read()
  #html = unicode(html,'gb2312','ignore').encode('utf-8','ignore')
  content = BeautifulSoup(html).findAll('a')
  pat = re.compile(r'href="([^"]*)"')
  pat2 = re.compile(r'http')
  for item in content:
   h = pat.search(str(item))
   if h:
     href = h.group(1)
     if pat2.search(href):
       if href.find('http://')!=-1:
         urls.append(href)
  return urls

#继承sgmlibParser,重写do_a方法
class LinksParser(sgmllib.SGMLParser):  
 urls = []  
 def do_a(self, attrs):  #定义当遇到标签<a>时，应做的处理
  for name, value in attrs:  
   if name == 'href' and value not in self.urls:  
    if value.startswith('http'):  
      self.urls.append(value)  
    else:  
     continue  
    return  
#获取相关链接
def GetRelatedURL(search_url, page):
  urls = []
  urls = grabHref(search_url)
  stopYahoo_f = open('StopYahooLinks', 'r')
  stop_link_list = (stopYahoo_f.read()).split('\n')
  stopYahoo_f.close()
  #过滤无用链接
  for stop_link in stop_link_list:
    if stop_link == '':
       break
    for url in urls:
     if url.find(stop_link) != -1:
       #print url
       urls.remove(url)
  return urls

#抓取lianjie
def thread_scratch_work(keywords, page, content_dir):
  search_key = keywords.replace('&', '+')
  search_key = search_key.replace(' ', '+')
 
  for i in range(10):
     #search_url = 'http://cn.bing.com/search?q='+search_key+'+&go=&qs=HS&pq=&sc=8-0&sp=1&sk=&intlF=1&first='+str(page)+'&FORM=TIPEN1'
     search_url = 'http://search.yahoo.com/search;_ylt=A0oGdSlBfX9RF2AAJ3pXNyoA?p='+search_key+'&ei=UTF-8&fr=yfp-t-101&pstart=1&b='+str(page+1)
     urls = GetRelatedURL(search_url, page)
     j = 0
     print 'len(urls): '+str(len(urls))+'     '+search_url
     for url in urls:
       print url
       if url.find('.pdf')!=-1 or url.find('.ppt')!=-1:
         continue
       content_data = ''
       response_data = ''
       isGoose = False
       try:
         try:
           if url.count('/') <= 3 and url[len(url)-1:] == '/':
            request_url = urllib2.Request(url, None, {'Referer': 'http://www.sina.com'})
            request_url.add_header('User-agent','CSC')
            response_data = urllib2.urlopen(request_url).read()
            content = (Document(response_data).summary()).encode('utf-8')
            if len(content) <= 32:
              content = response_data
           else:
            g = Goose()
            article = g.extract(url = url)
            content_data = (article.cleaned_text).encode('utf-8')
            if len(content_data)<32:
              request_url = urllib2.Request(url, None, {'Referer': 'http://www.sina.com'})
              request_url.add_header('User-agent','CSC')
              response_data = urllib2.urlopen(request_url).read()
              content = response_data
            else:
             isGoose = True
         except Exception, e:
           print e
           request_url = urllib2.Request(url, None, {'Referer': 'http://www.sina.com'})
           request_url.add_header('User-agent','CSC')
           response_data = urllib2.urlopen(request_url).read()
           content = (Document(response_data).summary()).encode('utf-8')
           if len(content) <= 32:
            content = response_data
       except Exception, e:
         print 'error occured 2'
         print e
         content = response_data
       #过滤文件
       if isGoose:
          print 'Goose'
       else:
          content_data = nltk.clean_html(content)
       filenum = str(page)+'_'+str(j)
       file_content = content_dir+'/related_html_'+filenum
       print 'write_file_content_'+content_dir+'_'+filenum
       f_c = open(file_content, 'w')
       f_c.write(content_data)
       f_c.close()
       j = j+1
     page = page+ 10
  print '线程退出%s'%page

def GetCorpusFromBing(keywords, pages = 1000):
  content_dir = 'content_related_html_'+urllib.quote(keywords)
  if os.path.exists(content_dir):
     print 'exists file'
     tools.delete_file_folder(content_dir)
  os.makedirs(content_dir)
  threads = []
  page = 0
  num = pages/100
  for x in range(num):
    page = x*100
    thread_scratch_work(keywords, page, content_dir)
    #page = x*100
    #t = threading.Thread(target = thread_scratch_work, args=(keywords, page, content_dir))
    #threads.append(t)
    #t.start()
 # for t in threads:
  #  t.join()

if __name__ == '__main__':
    
  #GetCorpusFromBing('titanic')
  urls = GetRelatedURL('http://cn.bing.com/search?q=titanic+&go=&qs=HS&pq=&sc=9-0&sp=1&sk=&intlF=1&first=100&FORM=TIPEN1' ,0)
  print urls
