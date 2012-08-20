
from collections import deque
import sys,os

# A deque is like a list but with efficient adding and consuming at both ends.  (But we'll only consume from the front.)
# d = deque([])
# d.append("foo")
# d.appendleft("foo")
# el = d.pop()
# el = d.popleft()


DBG = False

intersectTestCases = [ 
    [ "1:7,18,33,72,86,231; 2:1,17,74,222,255; 4:8,16,190,429,433; 5:363,367; 7:13,23,191; 13:28",
      "1:17,25; 4:17,191,291,430,434; 5:14,19,101; 6:19; 8:42; 10:11; 13:24",
      "[1, 4, 5, 13]" ],
    [ "1:11,35,77,98,104; 5:100",
      "1:21,92,93,94,95,97,99,100,101,102,103,105,106,107,108,109,110, 5:94,95",
      "[1]" ],
    [ "1:1,2,3,4,5,6,7",
      "1:1,2,3,4,5,6,7",
      "[1]" ],
    [ "1:11,92; 17:6,16; 21:103,113,114",
      "4:8; 5:2; 17:11; 21:3, 97,108",
      "[17, 21]" ],
    [ "5:4; 11:7,18; 12:1,17; 14:8,16; 15:363,367; 7:13,23,191; 103:28",
      "3:2; 8:9; 11:17,25; 14:17,434; 15:101; 16:19; 18:42; 100:11; 103:24; 109:11",
      "[11, 14, 15, 103]" ],
    [ "1:1; 5:1; 11:1; 13:1; 19:1; 43:1",
      "2:1; 3:1; 5:1; 9:1; 11:1; 15:1; 19:1; 33:1; 45:1",
      "[5, 11, 19]" ],
]



def popLeftOrNone(p):
  if len(p) > 0:
    posting = p.popleft()
  else:
    posting = None
  return posting


# Find docouments that contain both words
#
def intersect(p1, p2):
  answer = []

  p1posting = popLeftOrNone(p1)
  p2posting = popLeftOrNone(p2)
  
  while p1posting is not None and p2posting is not None:
    if p1posting['docID'] == p2posting['docID']:
      answer.append(p1posting['docID'])
      p1posting = popLeftOrNone(p1)
      p2posting = popLeftOrNone(p2)
    elif p1posting['docID'] < p2posting['docID']:
      p1posting = popLeftOrNone(p1)
    else:
      p2posting = popLeftOrNone(p2)
  return answer


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
  for test in intersectTestCases:
    pl1 = loadPostingsList(test[0])
    pl2 = loadPostingsList(test[1])
    print "Intersect of " + test[0]
    print "         and " + test[1] + ": "
    ans = intersect(pl1, pl2)
    ans_str = "[%s]" % ', '.join(["%d" % elm for elm in ans])
    print "Answer:    %s" % ans_str
    if not ans_str == test[2]:
      print "Should be: " + test[2]
      print "ERROR"
    print
elif args_len != 3:
    print >> sys.stderr, "Usage: intersect.py postingsList1 postingsList2"
    print >> sys.stderr, "       postingsList format: '1:17,25; 4:17,191,291,430,434; 5:14,19,10'"
else:
    pl1 = loadPostingsList(sys.argv[1]);
    pl2 = loadPostingsList(sys.argv[2]);
    ans = intersect(pl1, pl2)
    ans_str = "[%s]" % ', '.join(["%d" % elm for elm in ans])
    print "%s" % ans_str

