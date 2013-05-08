#/usr/bin/python
import GoogleCorpus
import os

f = open('ConceptList', 'r')
while True:
  chunk = f.readline()
  chunk = chunk.replace('\n', '')
  print chunk
  if not chunk:
    break
  GoogleCorpus.GetGoogleCorpusByKeywords(chunk)

print 'end'
