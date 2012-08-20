from CosineSimilarity import CosineSimilarity
from BM25 import BM25
from SmallestWindow import SmallestWindow
import os
import marshal
import subprocess

def unserialize_data(fname):
  """
  Reads a pickled data structure from a file named `fname` and returns it
  IMPORTANT: Only call marshal.load( .. ) on a file that was written to using marshal.dump( .. )
  marshal has a whole bunch of brittle caveats you can take a look at in teh documentation
  It is faster than everything else by several orders of magnitude though
  """
  with open(fname, 'rb') as f:
    return marshal.load(f)


MAX = 100
i = 0
training_file = 'queryDocTrainData'
idf = unserialize_data('model/idf')
curr_C1 = 0.0
results = open('results','w')
while i < MAX:
    file = open('test','w')
    scorer = CosineSimilarity(training_file, idf, file)
    curr_C1 = curr_C1 + 0.1
    scorer.C1 = curr_C1
    scorer.rank()
    file.close()
    i = i + 1 
    subprocess.check_output(['java -jar Ndcg.jar test queryDocTrainRel'])
results.close()