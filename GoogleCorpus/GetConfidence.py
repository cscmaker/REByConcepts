#!/usr/bin/python
#-*-coding:utf-8-*-

import os, urllib

refile = 'ResultPre'

re_f = open(refile,'r')
out_f = open('ResultPreWithConfiden', 'w')

while True:
 chunk = re_f.readline()
 print chunk
 chunk = chunk.replace('\n','')
 if not chunk:
   break
 temp = chunk.split(':')
 in_f = open('freq/context_predicate_freq_'+urllib.quote(temp[0]), 'r')
 
 while True:
  chu = in_f.readline()
  print chu
  if not chu:
     break
  chu = chu.replace('\n','')
  print temp[1]
  if chu.find(temp[1]+':')!=-1:
    c_list = chu.split(':')
    print c_list
    out_f.write(temp[0]+' '+temp[1]+' '+c_list[1]+'\n')
    break 

 in_f.close()
out_f.close()
re_f.close

