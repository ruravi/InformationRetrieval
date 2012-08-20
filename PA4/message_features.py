
from __future__ import print_function

import sys, re

from collections import Counter

SUBJECT_TAG = "Subject: "

MAX_TOKEN_LEN = 20
MIN_WORD_LEN = 3;
NUM_RE = re.compile(r"^([0-9]+)$")
WORD_RE = re.compile(r"^([a-zA-Z'\-]+)$")
ALPHANUM_RE = re.compile(r"^(\w+)$")
HYPERLINK_RE = re.compile(r"(http\:\/\/(\w+\.)+\w+)")
EMAIL_RE = re.compile(r"([\w\-\.]+@[\w\-\.]+)")
DELIMS_RE = re.compile(r"[\s\.()\"',-:;/\\?!@]+") 

class MessageFeatures:
  
  def __init__(self, newsgroupnum, filename, stemmer, stopwords):
    self.newsgroupnum = newsgroupnum
    self.filename = filename
    self.subject = Counter()
    self.body = Counter()
    self.parse(stemmer, stopwords)
  
  def parse(self, stemmer, stopwords):
    with open(self.filename, 'r') as msg:
      reading_subject = True
      for line in msg:
        if reading_subject and line.startswith(SUBJECT_TAG):
          self.parse_line(line[len(SUBJECT_TAG):], self.subject, stemmer,
              stopwords)
        elif reading_subject and not line:
          reading_subject = False
        else:
          self.parse_line(line, self.body, stemmer, stopwords)
  
  def parse_line(self, line, counts, stemmer, stopwords):
    line = line.lower()
    for linkmatch in HYPERLINK_RE.finditer(line):
      counts[linkmatch.group(0)] += 1
    for emailmatch in EMAIL_RE.finditer(line):
      counts[emailmatch.group(0)] += 1
    for token in DELIMS_RE.split(line):
      if len(token) < MAX_TOKEN_LEN:
        if NUM_RE.match(token):
          counts[token] += 1
        else:
          stemmed = stemmer.stem(token, 0, len(token)-1)
          if WORD_RE.match(stemmed) and len(stemmed) >= MIN_WORD_LEN and stemmed not in stopwords:
            counts[stemmed] += 1


if __name__ == '__main__':
  print(__file__ + " not meant to be invoked directly", file=sys.stderr)

