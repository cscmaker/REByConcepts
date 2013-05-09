#!/usr/bin/python
#!-*-coding:utf-8-*-
import YahooCorpus
import multiprocessing
def process_work(keywords, pages):
  YahooCorpus.GetCorpusFromBing(chunk, pages)
  return 
f = open('/home/csc/project/ConceptList', 'r')
#f = open('ConceptList', 'r')
process_record = []

while True:
  chunk = f.readline()
  if not chunk:
    break
  chunk = chunk.replace('\n', '')
  process_work(chunk, 1000)
  #process = multiprocessing.Process(target = process_work, args = (chunk,800))
  #process.start()
  #process_record.append(process)
#主进程等待
#for process in process_record:
 # process.join()

print '抓取完毕'
