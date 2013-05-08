#!/usr/bin/python
#-*-coding:utf-8-*-

import os, time,threading, textwrap, re, nltk, string, urllib, urllib2
from nltk.corpus import wordnet as wn

import sys
if not '/home/csc/project' in sys.path:
  sys.path.append('/home/csc/project')

import tools

def ExtractContextFromContent(inputdir, outputdir, keywords, window):
   #创建文件夹
   keywords_list = keywords.split('&')
   dir_name = outputdir
   if os.path.exists(dir_name):
     print 'exists  file'
     tools.delete_file_folder(dir_name)
   os.makedirs(dir_name)
   for filename in os.listdir(inputdir):
     full_filename = inputdir+'/'+filename
     output_filename = outputdir+'/'+filename+'_context'
     in_f = open(full_filename, 'r')
     out_f = open(output_filename, 'w')
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
       out_f.write(combine_sent.replace(r'[^a-zA-Z]?', ' ')+'\n#####\n')
     in_f.close()
     out_f.close()
   return  
def ExtractPredicateFromSent(inputdir, outputdir, key):
   #创建文件夹
   dir_name = outputdir
   if os.path.exists(dir_name):
     print 'exists  file'
     tools.delete_file_folder(dir_name)
   os.makedirs(dir_name)

   lancaster = nltk.LancasterStemmer()
   wnl = nltk.WordNetLemmatizer()
   porter = nltk.PorterStemmer()
   #stopwords
   stopwords_f = open('stopwordsList', 'r')
   chunk = stopwords_f.read()
   stopword_list = chunk.split('\n')
   stopwords_f.close()
   pattern = key.replace('&', '|')
   pattern = pattern.lower()
   regex = re.compile(r'\b'+pattern+'\b')
   for filename in os.listdir(inputdir):
     full_filename = inputdir+'/'+filename
     output_filename = outputdir+'/'+filename+'_predicate'
     in_f = open(full_filename, 'r')
     out_f = open(output_filename, 'w')
     chunk = in_f.read()
     sents = nltk.tokenize.sent_tokenize(chunk)
     predicate_dict = {}
     for sent in sents: 
       sent = sent.lower()
       first_pos = 0
       last_pos = 0
       for match in regex.finditer(sent):
         first_pos = match.start()
         break
       for match in regex.finditer(sent):
         last_pos = match.start()
       if last_pos == 0:
          continue
       if first_pos>20:
          move = first_pos-20
          while sent[move:move] !=' 'and move > 0:
             move = move-1
          fist_pos = move
       last = last_pos+20
       while last < len(sent) and sent[last:last]!=' ':
          last = last+1
       sent = sent[first_pos:last_pos]
       #对句子进行分词，然后进行词性标注
       words = nltk.word_tokenize(sent)
       words_tag = nltk.pos_tag(words)
       #保留关键字周围的动词和名词
       for word_tag in words_tag:
         if tools.find_item_in_list(stopword_list, (word_tag[0]).lower()) != -1:
            continue
         temp_str = ''
         if word_tag[1][0] =='V':
            if word_tag[0] == 'amp':
              continue
            temp_str = wn.morphy(word_tag[0], pos=wn.VERB)
            if temp_str == None:
               continue
         #elif word_tag[1][0] == 'N':
          #规则判断
          #if word_tag[0].find('or')==-1 or word_tag[0].find('er') == -1:
          #   continue
          #   temp_str = lancaster.stem(word_tag[0])
          #   if len(wn.synsets(temp_str, pos=wn.VERB)) == 0:#名词进行动词还原后具有动词性
          #      continue
         else:
            continue
         if temp_str not in predicate_dict:
            predicate_dict[temp_str] = 1
         else:
            predicate_dict[temp_str] += 1
     for k in predicate_dict:
       out_f.write(k+":"+str(predicate_dict[k])+'\n')  
     out_f.close()
     in_f.close()
   print '取谓词完成'

def ExtractPredicateFromContext(inputdir, outputdir, key):
   #创建文件夹
   dir_name = outputdir
   if os.path.exists(dir_name):
     print 'exists  file'
     tools.delete_file_folder(dir_name)
   os.makedirs(dir_name)

   lancaster = nltk.LancasterStemmer()
   wnl = nltk.WordNetLemmatizer()
   porter = nltk.PorterStemmer()
   #stopwords
   stopwords_f = open('stopwordsList', 'r')
   chunk = stopwords_f.read()
   stopword_list = chunk.split('\n')
   stopwords_f.close()
   pattern = key.replace('&', '|')
   pattern = pattern.lower()
   regex = re.compile(r'\b'+pattern+'\b')
   for filename in os.listdir(inputdir):
     full_filename = inputdir+'/'+filename
     output_filename = outputdir+'/'+filename+'_predicate'
     in_f = open(full_filename, 'r')
     out_f = open(output_filename, 'w')
     chunk = in_f.read()
     predicate_dict = {}
     context_list = chunk.split('\n#####\n')
     for context in context_list:
       context = context.lower()
       first_pos = 0
       last_pos = 0
       for match in regex.finditer(context):
         first_pos = match.start()
         break
       for match in regex.finditer(context):
         last_pos = match.start()
       if last_pos == 0:
          continue
       if first_pos>20:
          move = first_pos-20
          while context[move:move] !=' 'and move > 0:
             move = move-1
          fist_pos = move
       last = last_pos+20
       while last < len(context) and context[last:last]!=' ':
          last = last+1
       context = context[first_pos:last_pos]
       #对句子进行分词，然后进行词性标注
       words = nltk.word_tokenize(context)
       words_tag = nltk.pos_tag(words)
              #保留关键字周围的动词和名词
       for word_tag in words_tag:
         if tools.find_item_in_list(stopword_list, (word_tag[0]).lower()) != -1:
            continue
         temp_str = ''
         if word_tag[1][0] =='V':
            if word_tag[0] == 'amp':
              continue
            temp_str = wn.morphy(word_tag[0], pos=wn.VERB)
            if temp_str == None:
              continue
            if temp_str == 'include':
              print temp_str
         #elif word_tag[1][0] == 'N':
          #规则判断
          #if word_tag[0].find('or')==-1 or word_tag[0].find('er') == -1:
          #   continue
          #   temp_str = lancaster.stem(word_tag[0])
          #   if len(wn.synsets(temp_str, pos=wn.VERB)) == 0:#名词进行动词还原后具有动词性
          #      continue
         else:
            continue
         if temp_str not in predicate_dict:
            predicate_dict[temp_str] = 1
         else:
            predicate_dict[temp_str] += 1
     for k in predicate_dict:
       out_f.write(k+":"+str(predicate_dict[k])+'\n')  
     out_f.close()
     in_f.close()
   if os.path.exists(inputdir):
     print 'exists  file'
     tools.delete_file_folder(inputdir)
   print '取谓词完成'


if __name__ == '__main__':
   
   dir_in_out = raw_input('Enter in dir and out dir:\n')
   dirlist = dir_in_out.split(' ')

