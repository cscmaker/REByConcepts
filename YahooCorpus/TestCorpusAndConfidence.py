#!/usr/bin/python
#-*-coding:utf-8-*-

import PreciateFreq, os
import multiprocessing

def process_work(content_dir, concepts, window, predicate_list):
  PreciateFreq.CountPredicateFreqByX2(content_dir, concepts, window, predicate_list)   
  return 

f = open('../choosenPredicateFile_0.01')
while True:
  processes = []
  for i in range(10):
   chunk = f.readline()
   chunk = chunk.replace('\n', '')
   if not chunk:
     break
   if chunk.find('#') != -1:
     continue
   concepts = (chunk.split(':'))[0]
   predicate_list = ((chunk.split(':'))[1]).split('&')
   print  predicate_list
   process = multiprocessing.Process(target = process_work, args = ('/home/csc/YahooCorpus/content_related_html_', concepts, 1,predicate_list))
   process.start()
   processes.append(process)
  #主进程等待
  for process in processes:
    process.join()

ChoosePredicate.ReadFreqX2File('freq_x2','combine_file_x2')
