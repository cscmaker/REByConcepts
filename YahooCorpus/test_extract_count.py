#!/usr/bin/python
#-*-coding:utf-8-*-
import urllib
import CountPredicate, ExtractPredicate
import sys
if not '/home/csc/project' in sys.path:
  sys.path.append('/home/csc/project')
import tools


def CombineExtractAndCountPredicate(keywords, window):
  content_dir = 'content_related_html_'+urllib.quote(keywords)
  context_dir = 'context_html_'+urllib.quote(keywords)
  predicate_dir = 'predicate_'+urllib.quote(keywords)
  predicate_freq_file_context = 'freq/context_predicate_freq_'+urllib.quote(keywords)
  predicate_freq_file_sent = 'freq/sent_predicate_freq_'+urllib.quote(keywords)

  print '基于context抽取相关的谓语词'
  ExtractPredicate.ExtractContextFromContent(content_dir, context_dir, keywords, window)
  ExtractPredicate.ExtractPredicateFromContext(context_dir, predicate_dir, keywords)
  CountPredicate.CombineFreq(predicate_dir, predicate_freq_file_context)

  print '基于sent抽取相关的谓语词'
  ExtractPredicate.ExtractPredicateFromSent(content_dir, predicate_dir, keywords)
  CountPredicate.CombineFreq(predicate_dir, predicate_freq_file_sent)

def ChoosePredicate(predicate_dir, keywords, limit):
  f = open(predicate_dir+'/sent_predicate_freq_'+urllib.quote(keywords), 'r')


if __name__ == '__main__':

  f = open('/home/csc/project/TheatreConceptList', 'r')
  chunk = f.read()
  keylist = chunk.split('\n')
  for key in keylist:
   if key != '':
     CombineExtractAndCountPredicate(key, 1)
