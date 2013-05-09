#!/usr/bin/python
#-*-coding:utf-8-*-

def ReadRelationConcepts(filename):
 relation_dict = {}
 f = open(filename, 'r')
 while True:
   chunk = f.readline()
   if not chunk:
     break
   chunk = chunk.replace('\n', '')
   relation_dict[chunk] = chunk
 return relation_dict

def ReadNoRelationConcepts(filename):
 no_dict = {}
 f = open(filename, 'r')
 while True:
   chunk = f.readline()
   if not chunk:
     break
   chunk = chunk.replace('\n', '')
   no_dict[chunk] = chunk
 return no_dict

def CountPRAndFMeasure(relationFile, noRelationFile, judgeFile, support):
 f = open(judgeFile, 'r')
 A = 0
 B = 0
 C = 0
 D = 0
 r_dict = ReadRelationConcepts(relationFile)
 n_dict = ReadNoRelationConcepts(noRelationFile)
 while True:
   chunk = f.readline()
   if not chunk:
     break
   chunk = chunk.replace('\n','')
   temp = chunk.split(':')
   if cmp(temp[1], ' '+str(support))>=0:
      if (temp[0][:len(temp[0])-1]) in r_dict:
         A += 1
      else:
         B += 1
   else:
      if (temp[0][:len(temp[0])-1]) in r_dict:
        C+=1
      else:
        D+=1
 print 'A:%s B:%s C:%s D:%s '%(A,B,C,D)
 P=0
 R=0
 F=0
 if (A+B) != 0:
   P = A*1.0/(A+B)
 if (A+C)!=0:
   R = A*1.0/(A+C)
 if (P+R)!=0:
   F = 2*P*R*1.0/(P+R)
 print 'P:%s  R:%s  F:%s  support:%s'%(P,R,F, support)

if __name__ == '__main__':
  CountPRAndFMeasure('RelationConceptSupport', 'NoRelationConceptSupport', 'concepts_support', 0.35)
  print '---------------------------'
  CountPRAndFMeasure('RelationConceptSupport', 'NoRelationConceptSupport', 'concepts_support', 0.325)
  print '---------------------------'
  CountPRAndFMeasure('RelationConceptSupport', 'NoRelationConceptSupport', 'concepts_support', 0.30)
  print '---------------------------'
  CountPRAndFMeasure('RelationConceptSupport', 'NoRelationConceptSupport', 'concepts_support', 0.275)
  print '---------------------------'
  CountPRAndFMeasure('RelationConceptSupport', 'NoRelationConceptSupport', 'concepts_support', 0.250)
  print '---------------------------'
  CountPRAndFMeasure('RelationConceptSupport', 'NoRelationConceptSupport', 'concepts_support', 0.225)
  print '---------------------------'
  CountPRAndFMeasure('RelationConceptSupport', 'NoRelationConceptSupport', 'concepts_support', 0.200)
  print '---------------------------'
  CountPRAndFMeasure('RelationConceptSupport', 'NoRelationConceptSupport', 'concepts_support', 0.175)
  print '---------------------------'
  CountPRAndFMeasure('RelationConceptSupport', 'NoRelationConceptSupport', 'concepts_support', 0.150)
  print '---------------------------'
  CountPRAndFMeasure('RelationConceptSupport', 'NoRelationConceptSupport', 'concepts_support', 0.125)
  print '---------------------------'
  CountPRAndFMeasure('RelationConceptSupport', 'NoRelationConceptSupport', 'concepts_support', 0.100)
  print '---------------------------'
  CountPRAndFMeasure('RelationConceptSupport', 'NoRelationConceptSupport', 'concepts_support', 0.085)
  print '---------------------------'
  CountPRAndFMeasure('RelationConceptSupport', 'NoRelationConceptSupport', 'concepts_support', 0.065)
  print '---------------------------'
  CountPRAndFMeasure('RelationConceptSupport', 'NoRelationConceptSupport', 'concepts_support', 0.045)
  print '---------------------------'
  CountPRAndFMeasure('RelationConceptSupport', 'NoRelationConceptSupport', 'concepts_support', 0.025)
  print '---------------------------'
  CountPRAndFMeasure('RelationConceptSupport', 'NoRelationConceptSupport', 'concepts_support', 0.01)
