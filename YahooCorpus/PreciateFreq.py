#!/usr/bin/python
#!-*-coding:utf-8-*-

import math, urllib, os, sys
if not '/home/csc/project' in sys.path:
  sys.path.append('/home/csc/project')
from nltk.corpus import wordnet as wn
import FreqStatistics

def CountPredicateFreqBySplitConcept(content_dir, keywords, window,predicateList):
  out_f = open('freq_'+urllib.quote(keywords)+'_bySplitConcept', 'w')
  print '计算以概念分开的文件夹'
  c1c2_0 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(urllib.quote(keywords.split('&')[0])), keywords, 1, '')
  c1c2_1 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[1]), keywords, 1, '')
  print c1c2_0
  print c1c2_1
  print 'c1c2_0   c1c2_1'
  for predicate in predicateList:
    out_f.write(predicate+': ')
    c1c2_p_0 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[0]), keywords+'&'+predicate, 1, '')
    c1c2_p_1 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[1]), keywords+'&'+predicate, 1, '')
    #计算条件概率
    p_0 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[0]), predicate, 1, '')
    p_1 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[1]), predicate, 1, '')
    print c1c2_p_0
    print c1c2_p_1
    print p_0
    print p_1
    print '-------------------------------------'
    p_condition = 0
    if p_0+p_1 != 0:
      p_condition = (c1c2_p_0+c1c2_p_1)*1.0/(p_0+p_1)
    #计算互信息
    pmi = -9999999999
    temp1 = (c1c2_0+c1c2_1)*1.0*(p_1+p_0)
    temp2 = c1c2_p_1+c1c2_p_0
    if temp1 != 0 and temp2 != 0:
      pmi = math.log(temp2*1.0/temp1)
    #计算x2检验
    c1c2_not_p_0 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[0]), keywords, 1, predicate)
    c1c2_not_p_1 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[1]), keywords, 1, predicate)
    p_not_c1c2_0 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[0]), predicate, 1, keywords)
    p_not_c1c2_1 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[1]), predicate, 1, keywords)
    all_0 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[0]), '', 1, '')
    all_1 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[1]), '', 1, '')
    o11 = (c1c2_p_0+c1c2_p_1)
    o22 = (all_0+all_1-c1c2_p_0-c1c2_p_1)
    o12 = (p_not_c1c2_0+p_not_c1c2_1)
    o21 = (c1c2_not_p_0+c1c2_not_p_1)
    x2 = 0
    print o11
    print o22
    print o12
    print o21
    print 'end-----------------------------'
    temp_1 = (o11*1.0*o22-o12*1.0*o21) 
    temp_2 = 1.0*(o11+o12)*(o11+o21)*(o12+o22)*(o21+o22)
    if temp_1 !=0 and temp_2 != 0:
      x2 = (temp_1*1.0*temp_1)/temp_2
    out_f.write(str(p_condition)+'  '+str(pmi)+'  '+str(x2)+'\n')
  out_f.close()


def CountPredicateFreqByConceptPredicate(content_dir, keywords, window,predicateList):
  out_f = open('freq_'+urllib.quote(keywords)+'_byConceptPredicate', 'w')
  print '计算以概念谓词的文件夹'

  for predicate in predicateList:
    out_f.write(predicate+': ')
    c1c2_0 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[0]+'&'+predicate), keywords, 1, '')
    c1c2_1 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[1]+'&'+predicate), keywords, 1, '')
    print c1c2_0
    print c1c2_1
    print 'c1c2_0   c1c2_1'
    c1c2_p_0 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[0]+'&'+predicate), keywords+'&'+predicate, 1, '')
    c1c2_p_1 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[1]+'&'+predicate), keywords+'&'+predicate, 1, '')
    #计算条件概率
    p_0 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[0]+'&'+predicate), predicate, 1, '')
    p_1 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[1]+'&'+predicate), predicate, 1, '')
    print c1c2_p_0
    print c1c2_p_1
    print p_0
    print p_1
    print '-------------------------------------'
    p_condition = 0
    if p_0+p_1 != 0:
      p_condition = (c1c2_p_0+c1c2_p_1)*1.0/(p_0+p_1)
    #计算互信息
    pmi = -9999999999
    temp1 = (c1c2_0+c1c2_1)*1.0*(p_1+p_0)
    temp2 = c1c2_p_1+c1c2_p_0
    if temp1 != 0 and temp2 != 0:
      pmi = math.log(temp2*1.0/temp1)
    #计算x2检验
    c1c2_not_p_0 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[0]+'&'+predicate), keywords, 1, predicate)
    c1c2_not_p_1 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[1]+'&'+predicate), keywords, 1, predicate)
    p_not_c1c2_0 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[0]+'&'+predicate), predicate, 1, keywords)
    p_not_c1c2_1 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[1]+'&'+predicate), predicate, 1, keywords)
    all_0 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[0]+'&'+predicate), '', 1, '')
    all_1 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords.split('&')[1]+'&'+predicate), '', 1, '')
    o11 = (c1c2_p_0+c1c2_p_1)
    o22 = (all_0+all_1-c1c2_p_0-c1c2_p_1)
    o12 = (p_not_c1c2_0+p_not_c1c2_1)
    o21 = (c1c2_not_p_0+c1c2_not_p_1)
    x2 = 0
    print o11
    print o22
    print o12
    print o21
    print 'end-----------------------------'
    temp_1 = (o11*1.0*o22-o12*1.0*o21) 
    temp_2 = 1.0*(o11+o12)*(o11+o21)*(o12+o22)*(o21+o22)
    if temp_1 !=0 and temp_2 != 0:
      x2 = (temp_1*1.0*temp_1)/temp_2
    out_f.write(str(p_condition)+'  '+str(pmi)+'  '+str(x2)+'\n')
  out_f.close()


def CountPredicateFreqByConcepts(content_dir, keywords, window,predicateList):
  out_f = open('freq_'+urllib.quote(keywords)+'_byConcepts', 'w')
  print '计算以概念集合的文件夹'
  c1c2 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords), keywords, 1, '')
  print c1c2
  print 'c1c2'
  for predicate in predicateList:
    out_f.write(predicate+': ')
    c1c2_p = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords), keywords+'&'+predicate, 1, '')
    #计算条件概率
    p = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords), predicate, 1, '')
    print c1c2_p
    print p
    print '-------------------------------------'
    p_condition = 0
    if p != 0:
      p_condition = c1c2_p*1.0/p
    #计算互信息
    pmi = -9999999999
    temp1 = c1c2*1.0*p
    temp2 = c1c2_p
    if temp1 != 0 and temp2 != 0:
      pmi = math.log(temp2*1.0/temp1)
    #计算x2检验
    c1c2_not_p = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords), keywords, 1, predicate)
    p_not_c1c2 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords), predicate, 1, keywords)
    all_0 = FreqStatistics.ContextExtractWithKeywords(content_dir+urllib.quote(keywords), '', 1, '')
    o11 = c1c2_p
    o22 = all_0-c1c2_p
    o12 = p_not_c1c2
    o21 = c1c2_not_p
    x2 = 0
    print o11
    print o22
    print o12
    print o21
    print 'end-----------------------------'
    temp_1 = (o11*1.0*o22-o12*1.0*o21) 
    temp_2 = 1.0*(o11+o12)*(o11+o21)*(o12+o22)*(o21+o22)
    if temp_1 !=0 and temp_2 != 0:
      x2 = (temp_1*1.0*temp_1)/temp_2
    out_f.write(str(p_condition)+'  '+str(pmi)+'  '+str(x2)+'\n')
  out_f.close()

if __name__ == '__main__':
   f = open('choosedPredicateList')
   while True:
     chunk = f.readline()
     chunk = chunk.replace('\n', '')
     if not chunk:
       break
     if chunk.find('#') != -1:
       continue
     concepts = (chunk.split(':'))[0]
     predicate_list = ((chunk.split(':'))[1]).split('&')
     print  predicate_list
     CountPredicateFreqByConcepts('content_related_html_', concepts, 1, predicate_list)      
