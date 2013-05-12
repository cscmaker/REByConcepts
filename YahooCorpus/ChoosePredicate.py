#!/usr/bin/python
#-*-coding:utf-8-*-
import os, urllib

def ChooseFitPredicate(filename, keywords, outputfile):
  in_f = open(filename, 'r')
  out_f = open(outputfile, 'a')
  chunk = in_f.read()
  if not chunk:
    return
  value_list = chunk.split('\n')
  condition = ''
  PMI = ''
  x2 = ''
  fit_condition = ''
  fit_PMI = ''
  fit_x2 = ''
  for value in value_list:
   if value == '':
     break
   value = value.replace('\n','')
   temp_list = value.split(':')
   v_list = (temp_list[1]).split('  ')
   if fit_condition == '':
     condition = v_list[0]
     PMI = v_list[1]
     if v_list[2].find('#')==-1:
       x2 = v_list[2]
     else:
       x2 = 0
     fit_condition = temp_list[0]
     fit_PMI = temp_list[0]
     fit_x2 = temp_list[0]
   else:
     if cmp(v_list[0], condition)>0:
        condition = v_list[0]
        fit_condition = temp_list[0]
     if cmp(v_list[1], PMI)<0:
        PMI = v_list[1]
        fit_PMI = temp_list[0]
     if v_list[2].find('e')!=-1:
        continue 
     if cmp(v_list[2], x2)>0:
        x2 = v_list[2]
        fit_x2 = temp_list[0]
  out_f.write(keywords+'          '+fit_condition+'          '+fit_PMI+'          '+fit_x2+'\n')  
  out_f.close()
  in_f.close()

def ChooseFitPredicateByX2(filename, keywords, outputfile):
  in_f = open(filename, 'r')
  out_f = open(outputfile, 'a')
  chunk = in_f.read()
  if not chunk:
    return
  value_list = chunk.split('\n')
  x2 = ''
  fit_x2 = ''
  for value in value_list:
   if value == '':
     break
   value = value.replace('\n','')
   temp_list = value.split(':')
   if fit_x2 == '':
     if temp_list[1].find('#')==-1:
       x2 = temp_list[1]
     else:
       x2 = 0
     fit_x2 = temp_list[0]
   else:
     if temp_list[1].find('e')!=-1:
        continue 
     if cmp(temp_list[1], x2)>0:
        x2 = temp_list[1]
        fit_x2 = temp_list[0]
  out_f.write(keywords+': '+fit_x2+'\n')  
  out_f.close()
  in_f.close()

def ReadFreqFile(inputdir, outputfile):
  for filename in os.listdir(inputdir):
   full_filename = inputdir+'/'+filename
   keywords = urllib.unquote(filename[5:len(filename)-11])
   ChooseFitPredicate(full_filename, keywords, outputfile)
  return 'freq over'
def ReadFreqX2File(inputdir, outputfile):
  for filename in os.listdir(inputdir):
   full_filename = inputdir+'/'+filename
   keywords = urllib.unquote(filename[5:len(filename)-11])
   ChooseFitPredicateByX2(full_filename, keywords, outputfile)
  return 'freq over'

if __name__ == '__main__':
  ReadFreqX2File('freq_500','combine_file')
