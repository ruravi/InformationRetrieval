#!/bin/env python
from collections import deque
import os, glob, os.path
import sys
import re
import struct

from array import array
import common

if len(sys.argv) != 3:
  print >> sys.stderr, 'usage: python index.py data_dir output_dir' 
  os._exit(-1)

total_file_count = 0
root = sys.argv[1]
out_dir = sys.argv[2]
if not os.path.exists(out_dir):
  os.makedirs(out_dir)


# this is a dict holding document name -> doc_id
doc_id_dict = {}
# this is a dict holding word -> word_id
word_dict = {}
# this is a queue holding block names, later used for merging blocks
block_q = deque([])


# function to count number of files in collection
def count_file():
  print >> sys.stderr, 'you must provide implementation'

doc_id = 1
word_id = 1

sortedDirList = sorted(os.listdir(root))
#for dir in sortedDirList:
#    block_q.append(dir)
#if False:
for dir in sortedDirList:
  common.termsWritten = {}
  print >> sys.stderr, 'processing dir: ' + dir
  dir_name = os.path.join(root, dir)
  block_pl_name = out_dir+'/'+dir 
  # append block names to a queue, later used in merging
  block_q.append(dir)
  block_pl = open(block_pl_name + '.postings', 'wb')
  block_dict = open(block_pl_name + '.dict', 'wb')
  # term-doc-list is made a set so we don't have duplicate term-docID listings for multiple occurrences of a word
  term_doc_list = set([])
  sortedFileList = sorted(os.listdir(dir_name))
  for f in sortedFileList:
    total_file_count += 1
    file_id = os.path.join(dir, f)
    doc_id += 1
    doc_id_dict[file_id] = doc_id
    fullpath = os.path.join(dir_name, f)
    file = open(fullpath, 'r')
    for line in file.readlines():
      tokens = line.strip().split()
      for token in tokens:
        if word_dict.setdefault(token,word_id) == word_id:
            word_id += 1
        #if token not in word_dict:
        #  word_dict[token] = word_id
        #  word_id += 1
        term_doc_list.add( (word_dict[token], doc_id) )
  print >> sys.stderr, 'sorting term doc list for dir:' + dir
  term_doc_list = list(term_doc_list)
  # Sort the termID-docID pairs by termID
  term_doc_list.sort(key=lambda tuple:tuple[0])
  combined_term_doc_list = {}
  for termID,docID in term_doc_list:
      combined_term_doc_list.setdefault(termID,[]).append(docID)
  print >> sys.stderr, 'print posting list to disc for dir:' + dir
  terms = combined_term_doc_list.keys()
  # Since sorted() takes much longer  than .sort()
  terms.sort()
  for termID in terms:
    # write the posting lists to block_pl for this current block
    combined_term_doc_list[termID].sort()
    numPostings  = len(combined_term_doc_list[termID])
    common.writePostingsList( block_dict, block_pl, termID, common.compress(combined_term_doc_list[termID]), numPostings)
  block_pl.close()
  block_dict.close()

 


print >> sys.stderr, '######\nposting list construction finished!\n##########'

print >> sys.stderr, '\nMerging postings...'
while True:
  if len(block_q) <= 1:
    break
  b1 = block_q.popleft()
  b2 = block_q.popleft()
  print >> sys.stderr, 'merging %s and %s' % (b1, b2)
  b1_f = open(out_dir+'/'+b1+'.postings', 'rb')
  b2_f = open(out_dir+'/'+b2+'.postings', 'rb')
  b1_dict_file = open(out_dir+'/'+b1+'.dict', 'rb')
  b2_dict_file = open(out_dir+'/'+b2+'.dict', 'rb')
  comb = b1+'+'+b2
  comb_f = open(out_dir + '/'+comb+'.postings', 'wb')
  comb_dict_file = open(out_dir + '/'+comb+'.dict', 'wb')
  common.termsWritten = {}
  # write the new merged posting lists block to file 'comb_f'
  x = common.getNextPostingsList( b1_dict_file, b1_f )
  y = common.getNextPostingsList( b2_dict_file, b2_f )
  while True:
      if x is None or y is None:
          break
      termID1 = x[0]
      termID2 = y[0]
      if termID1 == termID2:
          common.mergeAndWritePostings(comb_dict_file, comb_f, termID1, x[1], y[1])
          x = common.getNextPostingsList( b1_dict_file, b1_f )
          y = common.getNextPostingsList( b2_dict_file, b2_f )
      elif termID1 < termID2:
          common.writePostingsList( comb_dict_file, comb_f, termID1, common.compress(x[1]), len(x[1]) )
          x = common.getNextPostingsList( b1_dict_file, b1_f )
      else:
          common.writePostingsList( comb_dict_file, comb_f, termID2, common.compress(y[1]), len(y[1]) )
          y = common.getNextPostingsList( b2_dict_file, b2_f )
  while x is not None:
      termID1 = x[0]
      common.writePostingsList( comb_dict_file, comb_f, termID1, common.compress(x[1]), len(x[1]) )
      x = common.getNextPostingsList( b1_dict_file, b1_f )
  while y is not None:
      termID2 = y[0]
      common.writePostingsList( comb_dict_file, comb_f, termID2, common.compress(y[1]), len(y[1]) )
      y = common.getNextPostingsList( b2_dict_file, b2_f )
  b1_f.close()
  b2_f.close()
  comb_f.close()
  b1_dict_file.close()
  b2_dict_file.close()
  comb_dict_file.close()
  os.remove(out_dir+'/'+b1+'.postings')
  os.remove(out_dir+'/'+b2+'.postings')
  os.remove(out_dir+'/'+b1+'.dict')
  os.remove(out_dir+'/'+b2+'.dict')
  block_q.append(comb)
    
print >> sys.stderr, '\nPosting Lists Merging DONE!'

# rename the final merged block to corpus.postings
final_name = block_q.popleft()
os.rename(out_dir+'/'+final_name+'.postings', out_dir+'/corpus.index')
os.rename(out_dir+'/'+final_name+'.dict', out_dir+'/posting.dict')

# print all the dictionary files
doc_dict_f = open(out_dir + '/doc.dict', 'w')
word_dict_f = open(out_dir + '/word.dict', 'w')
#posting_dict_f = open(out_dir + '/posting.dict', 'w')
print >> doc_dict_f, '\n'.join( ['%s\t%d' % (k,v) for (k,v) in sorted(doc_id_dict.iteritems(), key=lambda(k,v):v)])
print >> word_dict_f, '\n'.join( ['%s\t%d' % (k,v) for (k,v) in sorted(word_dict.iteritems(), key=lambda(k,v):v)])
#print >> posting_dict_f, '\n'.join(['%s\t%s' % (k,'\t'.join([str(elm) for elm in v])) for (k,v) in sorted(posting_dict.iteritems(), key=lambda(k,v):v)])
doc_dict_f.close()
word_dict_f.close()
#posting_dict_f.close()

print total_file_count
