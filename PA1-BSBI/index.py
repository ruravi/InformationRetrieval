#!/bin/env python
from collections import deque
import os, glob, os.path
import sys
import re
import bitstring

if len(sys.argv) != 3:
  print >> sys.stderr, 'usage: python index.py data_dir output_dir' 
  os._exit(-1)

total_file_count = 0
root = sys.argv[1]
out_dir = sys.argv[2]
if not os.path.exists(out_dir):
  os.makedirs(out_dir)

# this is the actual posting lists dictionary
posting_dict = {}
# this is a dict holding document name -> doc_id
doc_id_dict = {}
# this is a dict holding word -> word_id
word_dict = {}
# this is a queue holding block names, later used for merging blocks
block_q = deque([])

# function to count number of files in collection
def count_file():
  print >> sys.stderr, 'you must provide implementation'

# function for printing a line in a postings list to a given file
def print_posting(file, posting_line, termID):
  # a useful function is f.tell(), which gives you the offset from beginning of file
  # you may also want to consider storing the file position and doc frequency in posting_dict in this call
  posting_dict[termID] = (file.tell(), len(posting_line))
  file.write(termID + ' ')
  file.writelines(posting_line)
  file.write('\n')
  
# function for merging two lines of postings list to create a new line of merged results
def merge_posting (line1, line2):
  # don't forget to return the resulting line at the end
  result = []
  i = 0
  j = 0
  while i < len(line1) and j < len(line2):
      post1 = int(line1[i])
      post2 = int(line2[j])
      if post1 == post2:
          result.append(str(post1) + ' ')
          i += 1
          j += 1
      elif post1 < post2:
          result.append(str(post1) + ' ')
          i += 1
      else:
          result.append(str(post2) + ' ')
          j += 1
  while i < len(line1):
      result.append(line1[i] + ' ')
      i += 1
  while j < len(line2):
      result.append(line2[j] + ' ')  
      j += 1  
  return result


doc_id = -1
word_id = 0

for dir in sorted(os.listdir(root)):
  print >> sys.stderr, 'processing dir: ' + dir
  dir_name = os.path.join(root, dir)
  block_pl_name = out_dir+'/'+dir 
  # append block names to a queue, later used in merging
  block_q.append(dir)
  block_pl = open(block_pl_name, 'w')
  term_doc_list = set([])
  for f in sorted(os.listdir(dir_name)):
    #count_file()
    total_file_count += 1
    file_id = os.path.join(dir, f)
    doc_id += 1
    doc_id_dict[file_id] = doc_id
    fullpath = os.path.join(dir_name, f)
    file = open(fullpath, 'r')
    for line in file.readlines():
      tokens = line.strip().split()
      for token in tokens:
        if token not in word_dict:
          word_dict[token] = word_id
          word_id += 1
        term_doc_list.add( (word_dict[token], doc_id) )
  print >> sys.stderr, 'sorting term doc list for dir:' + dir
  #My Code here:
  term_doc_list = list(term_doc_list)
  term_doc_list.sort(key=lambda tuple:tuple[0])
  combined_term_doc_list = {}
  for termID,docID in term_doc_list:
      combined_term_doc_list.setdefault(termID,[]).append(docID)
  print >> sys.stderr, 'print posting list to disc for dir:' + dir
  for termID in sorted(combined_term_doc_list):
      block_pl.write(str(termID) + ' ')
      combined_term_doc_list[termID].sort()
      for each in combined_term_doc_list[termID]:
          block_pl.write(str(each) + ' ');
      block_pl.write("\n")
  # write the posting lists to block_pl for this current block
  #My code ends
  block_pl.close()


print >> sys.stderr, '######\nposting list construction finished!\n##########'

print >> sys.stderr, '\nMerging postings...'
while True:
  if len(block_q) <= 1:
    break
  b1 = block_q.popleft()
  b2 = block_q.popleft()
  print >> sys.stderr, 'merging %s and %s' % (b1, b2)
  b1_f = open(out_dir+'/'+b1, 'r')
  b2_f = open(out_dir+'/'+b2, 'r')
  comb = b1+'+'+b2
  comb_f = open(out_dir + '/'+comb, 'w')
  # (provide implementation merging the two blocks of posting lists)
  # write the new merged posting lists block to file 'comb_f'
  posting1 = b1_f.readline()
  posting2 = b2_f.readline()
  posting1 = posting1.strip().split()
  posting2 = posting2.strip().split()
  while True:   
      if posting1 == []:
          break
      if posting2 == []:
          break
      termID1 = int(posting1[0])
      termID2 = int(posting2[0])
      if termID1 == termID2:
          result = merge_posting(posting1[1:],posting2[1:])
          print_posting(comb_f,result,posting1[0])
          posting1 = b1_f.readline()
          posting2 = b2_f.readline()
          posting1 = posting1.strip().split()
          posting2 = posting2.strip().split()
      elif termID1 < termID2:
          posting1 =[each + ' ' for each in posting1]
          print_posting(comb_f,posting1[1:], posting1[0])
          posting1 = b1_f.readline().strip().split()
      else:
          posting2 = [each + ' ' for each in posting2]
          print_posting(comb_f, posting2[1:], posting2[0])
          posting2 = b2_f.readline().strip().split()
  while posting2 != []:
      posting2 = [each + ' ' for each in posting2]
      print_posting(comb_f, posting2[1:], posting2[0])
      posting2 = b2_f.readline()
      posting2 = posting2.strip().split()
  while posting1 != []:
      posting1 =[each + ' ' for each in posting1]
      print_posting(comb_f, posting1[1:], posting1[0])
      posting1 = b1_f.readline()
      posting1 = posting1.strip().split()
  b1_f.close()
  b2_f.close()
  comb_f.close()
  os.remove(out_dir+'/'+b1)
  os.remove(out_dir+'/'+b2)
  block_q.append(comb)
    
print >> sys.stderr, '\nPosting Lists Merging DONE!'

# rename the final merged block to corpus.index
final_name = block_q.popleft()
os.rename(out_dir+'/'+final_name, out_dir+'/corpus.index')

# print all the dictionary files
doc_dict_f = open(out_dir + '/doc.dict', 'w')
word_dict_f = open(out_dir + '/word.dict', 'w')
posting_dict_f = open(out_dir + '/posting.dict', 'w')
print >> doc_dict_f, '\n'.join( ['%s\t%d' % (k,v) for (k,v) in sorted(doc_id_dict.iteritems(), key=lambda(k,v):v)])
print >> word_dict_f, '\n'.join( ['%s\t%d' % (k,v) for (k,v) in sorted(word_dict.iteritems(), key=lambda(k,v):v)])
print >> posting_dict_f, '\n'.join(['%s\t%s' % (k,'\t'.join([str(elm) for elm in v])) for (k,v) in sorted(posting_dict.iteritems(), key=lambda(k,v):v)])
doc_dict_f.close()
word_dict_f.close()
posting_dict_f.close()

print total_file_count
