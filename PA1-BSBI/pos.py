#!/bin/env python
from collections import deque
import sys,os

# A deque is like a list but with efficient adding and consuming at both ends.  But we'll only consume from the front
# d = deque([])
# d.append("foo")
# d.appendleft("foo")
# el = d.pop()
# el = d.popleft()


DBG = False

testCases = [ 
    [ "1:7,18,33,72,86,231; 2:1,17,74,222,255; 4:8,16,190,429,433; 5:363,367; 7:13,23,191; 13:28",
      "1:17,25; 4:17,191,291,430,434; 5:14,19,101; 6:19; 8:42; 10:11; 13:24",
      "[(1,18,17), (4,16,17), (4,190,191), (4,429,430), (4,429,434), (4,433,430), (4,433,434), (13,28,24)]" ],
    [ "1:11,35,77,98,104; 5:100",
      "1:21,92,93,94,95,97,99,100,101,102,103,105,106,107,108,109,110, 5:94,95",
      "[(1,98,93), (1,98,94), (1,98,95), (1,98,97), (1,98,99), (1,98,100), (1,98,101), (1,98,102), (1,98,103), (1,104,99), (1,104,100), (1,104,101), (1,104,102), (1,104,103), (1,104,105), (1,104,106), (1,104,107), (1,104,108), (1,104,109)]" ],
    [ "1:1,2,3,4,5,6,7",
      "1:1,2,3,4,5,6,7",
      "[(1,1,1), (1,1,2), (1,1,3), (1,1,4), (1,1,5), (1,1,6), (1,2,1), (1,2,2), (1,2,3), (1,2,4), (1,2,5), (1,2,6), (1,2,7), (1,3,1), (1,3,2), (1,3,3), (1,3,4), (1,3,5), (1,3,6), (1,3,7), (1,4,1), (1,4,2), (1,4,3), (1,4,4), (1,4,5), (1,4,6), (1,4,7), (1,5,1), (1,5,2), (1,5,3), (1,5,4), (1,5,5), (1,5,6), (1,5,7), (1,6,1), (1,6,2), (1,6,3), (1,6,4), (1,6,5), (1,6,6), (1,6,7), (1,7,2), (1,7,3), (1,7,4), (1,7,5), (1,7,6), (1,7,7)]" ],
      
    [ "1:11,92; 17:6,16; 21:103,113,114",
      "4:8; 5:2; 17:11; 21:3, 97,108",
      "[(17,6,11), (17,16,11), (21,103,108), (21,113,108)]" ]
]


def popLeftOrNone(p):
  if len(p) > 0:
    posting = p.popleft()
  else:
    posting = None
  return posting
  


# Find proximity matches where the two words are within k words in the two postings lists 
#  Returns a list of (document, position_of_p1_word, position_of_p2_word) items.
#
def positionalIntersect(p1, p2, k):
  answer = []
  p1posting = popLeftOrNone(p1)
  p2posting = popLeftOrNone(p2)

  while p1posting is not None and p2posting is not None:
    if DBG:
      print >> sys.stderr, "Working on docs %d and %d" % (p1posting['docID'], p2posting['docID'])
    if p1posting['docID'] == p2posting['docID']:
      p1p = p1posting['positions']
      p2p = p2posting['positions']
      buffer = []
      pp1 = popLeftOrNone(p1p)
      pp2 = popLeftOrNone(p2p)
      while pp1 is not None:
        while pp2 is not None:
          if abs(pp1-pp2) <= k:
            buffer.append(pp2)
          elif pp2 > pp1:
            break
          pp2 = popLeftOrNone(p2p)
        while buffer != [] and abs(buffer[0]-pp1) > k:
          buffer.pop(0)
        for each in buffer:
          answer.append((p1posting['docID'],pp1,each))
        pp1 = popLeftOrNone(p1p)
      p1posting = popLeftOrNone(p1)
      p2posting = popLeftOrNone(p2)
    elif p1posting['docID'] < p2posting['docID']:
      p1posting = popLeftOrNone(p1)
    else:
      p2posting = popLeftOrNone(p2)
  return answer;


def loadPostingsList(s):
  ls = deque([])
  psts = s.split(";")
  for pst in psts:
    bits = pst.split(":")
    poses = bits[1].split(",")
    post = {}
    docID = int(bits[0].strip())
    positions = deque([])
    for pos in poses:
      positions.append(int(pos.strip()))
    post['docID'] = docID
    post['positions'] = positions
    ls.append(post)
  if DBG:
    print >> sys.stderr, "Loaded posting list: " + str(ls)
  return ls


args_len = len(sys.argv)
if args_len == 1:
  for test in testCases:
    pl1 = loadPostingsList(test[0])
    pl2 = loadPostingsList(test[1])
    print "Within 5 positional intersect of " + test[0]
    print "                             and " + test[1] + ": "
    ans = positionalIntersect(pl1, pl2, 5)
    ans_str = "[%s]" % ', '.join(["(%d,%d,%d)" % elm for elm in ans])
    print "Answer:    %s" % ans_str
    if not ans_str == test[2]:
      print "Should be: " + test[2]
      print "ERROR"
elif args_len != 4:
    print >> sys.stderr, "Usage: positional.py postingsList1 postingsList2 k"
    print >> sys.stderr, "       postingsList format: '1:17,25; 4:17,191,291,430,434; 5:14,19,10'"
else:
    pl1 = loadPostingsList(sys.argv[1]);
    pl2 = loadPostingsList(sys.argv[2]);
    ans = positionalIntersect(pl1, pl2, int(sys.argv[3].strip()))
    ans_str = "[%s]" % ', '.join(["(%d,%d,%d)" % elm for elm in ans])
    print "%s" % ans_str


