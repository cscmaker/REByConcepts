#!/usr/bin/python
#-*-coding:utf-8-*-

import urllib2,urllib
import simplejson
import os, time,threading, textwrap, re, nltk, multiprocessing
from nltk.corpus import wordnet as wn
from goose import Goose
from readability.readability import Document
import sys
if not '/home/csc/project' in sys.path:
  sys.path.append('/home/csc/project')
import tools
                         
#定义线程函数
def thread_scratch(url, rnum_perpage, page, key,  content_dir):
 print '线程开启%s'%page
 url_set = [] 
 try:
   request = urllib2.Request(url, None, {'Referer': 'http://www.sina.com'})
   response = urllib2.urlopen(request)
   results = simplejson.load(response)
   info = results['items']
 except Exception,e:
   print 'get info error occured'
   print e
 else:
   for minfo in info:
      url_set.append(minfo['link'])
      print minfo['link']
 #处理链接
 i = 0
 for u in url_set:
   print '处理链接%s-------%s'%(page, i)
   content_data = ''
   response_data = ''
   isGoose = False
   try:
     try:
      g = Goose()
      article = g.extract(url = u)
      content_data = (article.cleaned_text).encode('utf-8')
      if len(content_data)<32:
        request_url = urllib2.Request(u, None, {'Referer': 'http://www.sina.com'})
        request_url.add_header('User-agent','CSC')
        response_data = urllib2.urlopen(request_url).read()
        content = response_data
      else:
        isGoose = True
     except Exception, e:
      print e
      request_url = urllib2.Request(u, None, {'Referer': 'http://www.sina.com'})
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
     print 'not Goose'
     content_data = nltk.clean_html(content)
   filenum = i+page
   file_content = content_dir+'/related_html_'+str(filenum)
   f_c = open(file_content, 'w')
   f_c.write(content_data)
   f_c.close()
   print '  write down: related_html_'+str(filenum)
   i = i+1
 print '线程退出%s'%page
 return 

#进程函数， 抓取网页
def process_work(pages, rnum_perpage, key,  content_dir):
 print '进程开启:'+key
 threads = []
 for x in range(pages):
   page = x * rnum_perpage+1
   search_key = key.replace('&', ' ')
   google_keywords = ''+search_key+''
   #url = ('https://www.googleapis.com/customsearch/v1?key=AIzaSyCLmWaw1UJwVhWvzcCelq8Jc609fHUnwRA&cx=013036536707430787589:_pqjad5hr1a&q=%s&start=%s&num=%s')%(urllib.quote(google_keywords), page, rnum_perpage)
   #url = ('https://www.googleapis.com/customsearch/v1?key=AIzaSyD6agcMbZmDa_zG4MkNokUJvTEQS5bWbZU&cx=013036536707430787589:_pqjad5hr1a&q=%s&start=%s&num=%s')%(urllib.quote(google_keywords), page, rnum_perpage)

   #url = ('https://www.googleapis.com/customsearch/v1?key=AIzaSyA_7rA8p0Ofia-8zYqFM-yBxicmr2S8M_E&cx=013036536707430787589:_pqjad5hr1a&q=%s&start=%s&num=%s')%(urllib.quote(google_keywords), page, rnum_perpage)

   url = ('https://www.googleapis.com/customsearch/v1?key=AIzaSyADVkbusXzwQWAT5or4Z-gan2xSsXZ72Gw&cx=013036536707430787589:_pqjad5hr1a&q=%s&start=%s&num=%s')%(urllib.quote(google_keywords), page, rnum_perpage)

   print 'url:  '+url
   print 'url:  '+url
   print 'url:  '+url
   t = threading.Thread(target=thread_scratch, args=(url,rnum_perpage, page, key,  content_dir))
   threads.append(t)
   t.start()
  #主线程等待子线程抓取完
 for t in threads:  
   t.join(300)
 print '进程结束，抓取完毕: '+key

#function
def GetGoogleCorpusByKeywords(keywords, pages=8, rnum_perpage=10):
 keywords_list = keywords.split('&')
 #synset_list1 = []
 #synset_list2 = []
 #synset_list1.append(keywords_list[0])
 #synset_list2.append(keywords_list[1])

 #for synset in wn.synsets(keywords_list[0], pos = wn.NOUN):
 #  for lemma in synset.lemmas:
 #    if (lemma.name).find('_') == -1:
 #      synset_list1.append(lemma.name)
 #for synset in wn.synsets(keywords_list[1], pos = wn.NOUN):
 #  for lemma in synset.lemmas:
 #    if (lemma.name).find('_') == -1:
 #     synset_list2.append(lemma.name)
 #all_keywords = []
 #构造同义关键字
 #for s1 in synset_list1:
 #  for s2 in synset_list2:
 #   all_keywords.append(s1+'&'+s2)
   
 #创建文件夹
 content_dir = 'content_analysis_html_'+urllib.quote(keywords)
 if os.path.exists(content_dir):
    tools.delete_file_folder(content_dir)
 os.makedirs(content_dir)
 
 #创建多个进程进行抓取
 #i = 0
 process_record = []
 #all_keywords_set = set()
 #for key in all_keywords:
 #  if key in all_keywords_set:
 #     continue
 #  if i==3:
 #    break
 #  i = i+1
 #  all_keywords_set.add(key)
 #  sub_dir_name = 'corpus_related_html_'+urllib.quote(keywords)+'/'+urllib.quote(key)
 #  if os.path.exists(sub_dir_name):
 #    print 'exists  file'
 #    tools.delete_file_folder(sub_dir_name)
 #  os.makedirs(sub_dir_name)
 #  sub_content_dir = 'content_analysis_html_'+urllib.quote(keywords)+'/'+urllib.quote(key)
 #  if os.path.exists(sub_content_dir):
 #    tools.delete_file_folder(sub_content_dir)
 #  os.makedirs(sub_content_dir)

 process = multiprocessing.Process(target = process_work, args = (pages, rnum_perpage, keywords,  content_dir))
 process.start()
 process_record.append(process)
 #主进程等待
 for process in process_record:
  process.join()
 return 



if __name__ == '__main__':
 #input the keywords
 keywords = raw_input('Enter the keywords: ')       
 get_corpus_of_keywords(keywords, 10, 10)
