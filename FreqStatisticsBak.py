#!/usr/bin/python
#-*-coding:utf-8-*-

import nltk, os, string, urllib, math, re
from nltk.corpus import wordnet as wn
#抽取指定文件夹的句子，并且统计个数
def SentExtractWithKeywords(content_dir, keywords):
  total_num = 0
  keywords_list = keywords.split('&')
  #outputfile = 'sentences_with_'+keywords
  #out_f = open(outputfile, 'w')
  for filename in os.listdir(content_dir):
    full_filename = content_dir+'/'+filename
    in_f = open(full_filename, 'r')
    chunk = in_f.read()
    #split sent
    sents = nltk.tokenize.sent_tokenize(chunk)
    for sent in sents:
      sent = sent.lower()
      isHas = False
      for key in keywords_list:
        temp = wn.morphy(key, pos=wn.VERB)
        if temp != None:
           isHas = False
           res = re.findall(key.lower(), sent)
           if res != None:
             for r in res:
                tem = wn.morphy(key, pos=wn.VERB)
                if tem == key:
                  isHas = True
                  break
             if isHas == False:
                break
        else:
          if sent.find(key.lower()) != -1:
            isHas = True
          else:
            isHas = False
            break
      if isHas:
   #     out_f.write(sent.replace('\n', ' ')+'\n')
        total_num += 1
    in_f.close()
  #out_f.close()
  return total_num
def ContextExtractWithKeywords(content_dir, keywords, window, notkeywords, size):
  total_num = 0
  keywords_list = keywords.split('&')
  notkeywords_list = notkeywords.split('&')
  #outputfile = 'sentences_with_'+keywords
  #out_f = open(outputfile, 'w')
  i = 0
  for filename in os.listdir(content_dir):
    i += 1
    if i>size:
       break
    full_filename = content_dir+'/'+filename
    in_f = open(full_filename, 'r')
    chunk = in_f.read()
    #split sent
    sents = nltk.tokenize.sent_tokenize(chunk)
    for i in range(len(sents)):
      combine_sent = ''
      for j in range(window):
        pre = i-j
        nex = i+j+1
        if pre >= 0:
          combine_sent += sents[pre]
        if nex < len(sents):
          combine_sent += sents[nex]
      combine_sent = combine_sent.lower()
      isHas = False
      for key in keywords_list:
        temp = wn.morphy(key, pos=wn.VERB)
        if temp != None:
           isHas = False
           res = re.findall(key.lower(), combine_sent)
           if res != None:
             for r in res:
                tem = wn.morphy(key, pos=wn.VERB)
                if tem == key:
                  isHas = True
                  break
             if isHas == False:
                break
        else:
          if combine_sent.find(key.lower()) != -1:
           isHas = True
          else:
           isHas = False
           break
      if isHas:
        if notkeywords == '':
           total_num += 1
        else:
          for nkey in notkeywords_list:
            temp = wn.morphy(nkey, pos=wn.VERB)
            if temp != None:
              isHas = False
              res = re.findall(nkey.lower(), combine_sent)
              if res != None:
               for r in res:
                tem = wn.morphy(nkey, pos=wn.VERB)
                if tem == nkey:
                  isHas = False
                  break
               if isHas == True:
                  break
            else:
              if combine_sent.find(nkey.lower()) != -1:
                 isHas = False
              else:
                 isHas = True
                 break
          if isHas == False:
            total_num += 1
  return total_num



#抽取指定文件夹，并且统计个数
def ContentExtractWithKeywords(content_dir, keywords):
  keywords_list = keywords.split('&')
  keydict = {}
  for key in keywords_list:
    keydict[key] = 0
  #outputfile = 'sentences_with_'+keywords
  #out_f = open(outputfile, 'w')
  for filename in os.listdir(content_dir):
    full_filename = content_dir+'/'+filename
    in_f = open(full_filename, 'r')
    chunk = (in_f.read()).lower()
    for key in keywords_list:
      keydict[key] += chunk.count(key.lower())
    in_f.close()
  #out_f.close()
  for key in keywords_list:
     print key+': %s'%keydict[key]


if __name__ == '__main__':
  
  content_dir = 'content_related_html_'
  f = open('choosedPredicateList', 'r')
  f1 = open('resultsWithWindow1', 'w')
  f2 = open('resultsWithWindow2', 'w')
  while True:
    chunk = f.readline()
    chunk.replace('\n', '')
    if not chunk:
     break
    #格式为：概念：谓语集
    temp_list = chunk.split(':')
    concept_list = (temp_list[0]).split('&')
    predicate_list = (temp_list[1]).split('&')
    f1.write(temp_list[0]+'\n')
    f2.write(temp_list[0]+'\n')
    print concept_list
    cons_count_win1 = SentExtractWithKeywordsHasWindow(content_dir+urllib.quote(temp_list[0]), '&'.join(concept_list), 1)
    for predicate in predicate_list:
      print predicate
     #window 1
      cons_predi_count_win1 = SentExtractWithKeywordsHasWindow(content_dir+urllib.quote(temp_list[0]), '&'.join(concept_list)+'&'+predicate, 1)
      predi_count_win1 = SentExtractWithKeywordsHasWindow(content_dir+urllib.quote(temp_list[0]), predicate, 1)
      #计算条件概率
      print str(cons_predi_count_win1)+'/'+str(predi_count_win1)
      if predi_count_win1 == 0:
        p_condition = 0
      else:
        p_condition = cons_predi_count_win1*1.0/predi_count_win1
      print 'p_condition: %s'%p_condition
      f1.write(predicate+': '+str(p_condition)+'\n')
    #window 2
    #  cons_predi_count_win2 = ContextExtractWithKeywordsHasWindow(content_dir+urllib.quote(temp_list[0]), '&'.join(concept_list)+'&'+predicate, 1, '')
    #  predi_count_win2 = ContextExtractWithKeywordsHasWindow(content_dir+urllib.quote(temp_list[0]), predicate, 1, '')
      #计算条件概率
    #  print str(cons_predi_count_win2)+'/'+str(predi_count_win2)
    #  if predi_count_win2 == 0:
    #    p_condition = 0
    #  else:
    #    p_condition = cons_predi_count_win2*1.0/predi_count_win2
    #  print 'p_condition: %s'%p_condition
    #  f2.write(predicate+': '+str(p_condition)+'\n')
  f1.close()
  #f2.close()
