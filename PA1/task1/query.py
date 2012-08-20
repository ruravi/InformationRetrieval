#!/bin/env python
from collections import deque
import os, glob, os.path
import sys
import re
import common
from time import time

if len(sys.argv) != 2:
  print >> sys.stderr, 'usage: python query.py index_dir' 
  os._exit(-1)

# postings are lists of strings containing docIDs as strings
def intersectPosting (postings1, postings2):
  new_posting = []
  # provide implementation for merging two postings lists
  i = 0
  j = 0
  while i < len(postings1) and j < len(postings2):
      docID1 = postings1[i]
      docID2 = postings2[j]
      if docID1 == docID2:
          new_posting.append(docID1)
          i += 1
          j += 1
      elif int(docID1) < int(docID2):
          i += 1
      else:
          j += 1
  return new_posting

# file locate of all the index related files
index_dir = sys.argv[1]
index_f = open(index_dir+'/corpus.index', 'rb')
word_dict_f = open(index_dir+'/word.dict', 'r')
doc_dict_f = open(index_dir+'/doc.dict', 'r')
posting_dict_f = open(index_dir+'/posting.dict', 'rb')

word_dict = {}
doc_id_dict = {}
file_pos_dict = {}
doc_freq_dict = {}
posting_size_dict = {}

print >> sys.stderr, 'loading word dict'
for line in word_dict_f.readlines():
  parts = line.split('\t')
  word_dict[parts[0]] = int(parts[1])

print >> sys.stderr, 'loading doc dict'
for line in doc_dict_f.readlines():
  parts = line.split('\t')
  doc_id_dict[int(parts[1])] = parts[0]
print >> sys.stderr, 'loading posting mapping'
while True:
	dEntry = common.getPostingHeader( posting_dict_f )
	if dEntry is None:
		break
	else:
		term_id = int( dEntry[0] )
		file_pos = int( dEntry[1] )
		pos_size = int( dEntry[2] )
		file_pos_dict[term_id] = file_pos
		posting_size_dict[term_id] = pos_size
		doc_freq_dict[term_id] = pos_size


def read_posting(term_id):
  # provide implementation for posting list lookup for a given term
  # a useful function to use is index_f.seek(file_pos), which does a disc seek to 
  # a position offset 'file_pos' from the beginning of the file
  file_pos = file_pos_dict[term_id]
  index_f.seek(file_pos)
  posting_list = index_f.read( posting_size_dict[term_id] )
  posting_list = common.decode( posting_list )
  return posting_list
  
# read query from stdin
while True:
  input = sys.stdin.readline()
  start = time()
  input = input.strip()
  if len(input) == 0: # end of file reached
    break
  input_parts = input.split()
  # you need to translate words into word_ids
  input_parts = [word_dict.get(each,-1) for each in input_parts]
  if -1 in input_parts:
      print "no results found"
      continue
  input_parts = list(set(input_parts))
  # don't forget to handle the case where query contains unseen words
  # next retrieve the postings list of each query term, and merge the posting lists
  # to produce the final result
  input_parts.sort(key= lambda docID: doc_freq_dict[docID])
  merged_posting = read_posting(input_parts[0])
  for each_query in input_parts[1:]:
      posting = read_posting(each_query)
      merged_posting = intersectPosting(posting,merged_posting)
  # don't forget to convert doc_id back to doc_name, and sort in lexicographical order
  # before printing out to stdout
  merged_posting = [doc_id_dict[each] for each in merged_posting]
  merged_posting.sort()
  elapsed = time() - start
  print >> sys.stderr, "elapsed time =" + str(elapsed)
  if len(merged_posting) == 0:
      print "no results found"
  else:
      for each in merged_posting:
          print each
