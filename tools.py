#!/usr/bin/python

import os, string
def delete_file_folder(src):
  if os.path.isfile(src):
    try:
      os.remove(src)
    except:
      pass
  elif os.path.isdir(src):
    for item in os.listdir(src):
      itemsrc = os.path.join(src, item)
      delete_file_folder(itemsrc)
    try:
      os.rmdir(src)
    except:
      pass

def combine_file(filelist, outputfile):
  word_dict = {}
  output_f = open(outputfile, 'w+')
  for inputfile in filelist:
    input_f = open(inputfile, 'r+')
    while True:
      chunk = input_f.read(2048)
      if not chunk:
        break
      output_f.write(chunk)
    input_f.close()
  output_f.close()

def combine_file_version2(filelist, outputfile):
   word_dict = {}
   total_num = 0
   output_f = open(outputfile, 'w+')
   for inputfile in filelist:
      input_f = open(inputfile, 'r+')
      try:
        chunk = input_f.readline()
        if not chunk:
           continue
        total_num += string.atoi(chunk)
        while True:
          chunk = input_f.readline()
          if not chunk:
            break
          tag = chunk.split(':')
          if tag[0] not in word_dict:
             word_dict[tag[0]] = 1
          else:
             word_dict[tag[0]] = word_dict[tag[0]]+string.atoi(tag[1])
      finally:
        input_f.close()

   wordlist =  sort_dict_by_value(word_dict)

   for word in wordlist:
      output_f.write(word[0]+':'+str(word[1])+'\n')
   output_f.close()
   return total_num

def sort_dict_by_value(d):
  return sorted(d.items(), key = lambda d:d[1])


def find_item_in_list(my_list, item):
  i = 0
  flag = False
  for l in my_list:
    if l == item:
      flag = True
      break
    i += 1
  if flag:
    return i
  else:
    return -1

def find_keys_in_list(my_list, key):
  pos_list = []
  key_list = key.split('&')
  len1 = len(key_list[0])
  len2 = len(key_list[1])
  for i in range(len(my_list)):
   if (i+len1)<=len(my_list):
     if my_list[i:i+len1] == key_list[0]:
        pos_list.append(i)
        pos_list.append(i+len1)
   if (i+len2)<=len(my_list):
     if my_list[i:i+len2] == key_list[1]:
        pos_list.append(i)
        pos_list.append(i+len2)
  return pos_list
  
    
if __name__ == '__main__':
  
   f = open('stopwordsList', 'r')
   l = f.readline()
