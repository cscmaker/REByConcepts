#!/usr/bin/python
#-*-coding:utf-8-*-

import os, time,threading, textwrap, re, nltk, string, urllib, urllib2
from nltk.corpus import wordnet as wn

import sys
if not '/home/csc/project' in sys.path:
  sys.path.append('/home/csc/project')
import tools

def CountFreq(inputdir, outputdir):
  if os.path.exists(outputdir):
    print 'exists  file'
    tools.delete_file_folder(outputdir)
  os.makedirs(outputdir)
  transaction_num = 0
  for filename in os.listdir(inputdir):
    full_filename = inputdir+'/'+filename
    output_filename = outputdir+'/'+filename+'_freq'
    in_f = open(full_filename, 'r')
    transaction_num += len(in_f.readlines())
    in_f.seek(0)
    out_f = open(output_filename, 'w')
    chunk = in_f.read()
    print 'read'+filename
    if not chunk:
      continue
    in_f.close()
    words = nltk.word_tokenize(chunk)
    word_dict = {}
    for word in words:
       if word not in word_dict:
          word_dict[word] = 1
       else:
          word_dict[word] += 1  
    for key in word_dict:
      out_f.write(key+':'+str(word_dict[key])+'\n')
    out_f.close()
  if os.path.exists(inputdir):
    print 'exists  file'
    tools.delete_file_folder(inputdir)
  return transaction_num

def CombineFreq(inputdir, outfreqfile):
  if os.path.exists(outfreqfile):
    tools.delete_file_folder(outfreqfile)
  out_f = open(outfreqfile, 'w')
  word_dict = {}
  for filename in os.listdir(inputdir):
    full_filename = inputdir+'/'+filename
    in_f = open(full_filename, 'r')
    while True:
       chunk = in_f.readline()
       if not chunk:
         break
       temp_list = chunk.split(':')
       if temp_list[0] not in word_dict:
         word_dict[temp_list[0]] = string.atoi(temp_list[1])
       else:
         word_dict[temp_list[0]] += string.atoi(temp_list[1])
    in_f.close()
   
  word_freq_list = tools.sort_dict_by_value(word_dict)
  for word_freq in word_freq_list:
    out_f.write(word_freq[0]+':'+str(word_freq[1])+'\n')
  out_f.close()
 
  if os.path.exists(inputdir):
    tools.delete_file_folder(inputdir)
  return 


if __name__ == '__main__':
   
   d = raw_input('Input in out outfile: \n')
   d_list = d.split('&')
