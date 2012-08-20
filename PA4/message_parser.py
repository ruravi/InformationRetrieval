
from __future__ import print_function

import re
import cPickle as pickle
import sys, os

from stemmer import PorterStemmer as Stemmer
from message_features import MessageFeatures

STOP_FILE = "english.stop"
stopwords = set()
stemmer = Stemmer()


def load_stopwords():
  global stopwords
  with open(STOP_FILE, 'r') as stopwfile:
    for word in stopwfile:
      stword = word.strip()
      stopwords.add(stemmer.stem(stword, 0, len(stword)-1))
  return stopwords


def parse_training_dirs(inp_dir, out_file):
  inp_dir = os.path.abspath(inp_dir)
  with open(out_file, 'wb') as outstream:
    writer = pickle.Pickler(outstream, pickle.HIGHEST_PROTOCOL)
    training_dirs = sorted(os.listdir(inp_dir))
    writer.dump(len(training_dirs))
    num_msgs = [0] * len(training_dirs)
    for group, train_dir in enumerate(training_dirs):
      num_msgs[group] = len(os.listdir(os.path.join(inp_dir,train_dir)))
    writer.dump(sum(num_msgs))
    writer.dump(num_msgs)
    for group, train_dir in enumerate(training_dirs):
      parse_newsgroup(group, os.path.join(inp_dir,train_dir), writer)

def parse_newsgroup(group_num, train_dir, writer):
  try:
    msgs = sorted(os.listdir(train_dir))
    print("Parsing {0} with {1} messages".format(train_dir, len(msgs)) ,
      file=sys.stderr)
    for msg in msgs:
      mf = MessageFeatures(group_num, os.path.join(train_dir,msg), stemmer, stopwords)
      writer.dump(mf)
  except IOError as e:
    print('Cannot locate directory: '+train_dir, file=sys.stderr)
    sys.exit(-1)


def main():
  if len(sys.argv) != 3:
    print("Usage: python {0} <directory> <output_file>".format(__file__))
    return
  inp_dir = sys.argv[1]
  out_file = sys.argv[2]
  load_stopwords()
  parse_training_dirs(inp_dir, out_file)

if __name__ == '__main__':
  main()

