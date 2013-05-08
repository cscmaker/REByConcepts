#!/usr/bin/python
#-*-coding:utf-8-*-
import nltk, os, string, urllib, math
import sys
if not '/home/csc/project' in sys.path:
  sys.path.append('/home/csc/project')

import FreqStatistics

def ChoosePredicateByX2(content_dir, keywords, predicatefile, limit, window, outputfile):
  return

def ChoosePredicateByPMI(content_dir, keywords, predicatefile, limit, window, outputfile):
  in_f = open(predicatefile, 'r')
  out_f = open(outputfile, 'w')
  c1c2 = FreqStatistics.SentExtractWithKeywordsHasWindow(content_dir, keywords, window)  
  while True:
    chunk = in_f.readline()
    if not chunk:
      break
    predicate = (chunk.split(':'))[0]
    print predicate
    c1pc2 = FreqStatistics.SentExtractWithKeywordsHasWindow(content_dir, keywords+'&'+predicate, window)
    p = FreqStatistics.SentExtractWithKeywordsHasWindow(content_dir, predicate, window)
    if c1c2*p == 0:
      continue
    pmi = math.log((c1pc2*1.0)/(c1c2*p))
    if pmi >= limit:
      out_f.write(predicate+':'+str(pmi))

  out_f.close()
  in_f.close()
  return 


def ChoosePredicateByCondition(content_dir, keywords, predicatefile, limit, window, outputfile):
  in_f = open(predicatefile, 'r')
  out_f = open(outputfile, 'w')
  while True:
    chunk = in_f.readline()
    if not chunk:
      break
    predicate = (chunk.split(':'))[0]
    print predicate
    c1pc2 = FreqStatistics.SentExtractWithKeywordsHasWindow(content_dir, keywords+'&'+predicate, window)
    p = FreqStatistics.SentExtractWithKeywordsHasWindow(content_dir, predicate, window)
    p_condition = 0
    if c1pc2 != 0:
      p_condition = (c1pc2*1.0)/p
    if p_condition >= limit:
      out_f.write(predicate+':'+str(p_condition))

  out_f.close()
  in_f.close()
  return 

if __name__ == '__main__':
  
   keywords = 'hypertension&cerebrovascular disease'
   ChoosePredicateByCondition('content_analysis_html_'+urllib.quote(keywords), keywords, 'freq/context_predicate_freq_'+urllib.quote(keywords), 0, 2, 'predicate_'+urllib.quote(keywords)+'_Bycondition')
   ChoosePredicateByPMI('content_analysis_html_'+urllib.quote(keywords), keywords, 'freq/context_predicate_freq_'+urllib.quote(keywords), -9999999, 2, 'predicate_'+urllib.quote(keywords)+'_ByPMI')
   
