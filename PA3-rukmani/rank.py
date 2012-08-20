import sys
import marshal
from CosineSimilarity import CosineSimilarity
from BM25 import BM25
from SmallestWindow import SmallestWindow
from Inlinks import Inlinks


def unserialize_data(fname):
  """
  Reads a pickled data structure from a file named `fname` and returns it
  IMPORTANT: Only call marshal.load( .. ) on a file that was written to using marshal.dump( .. )
  marshal has a whole bunch of brittle caveats you can take a look at in teh documentation
  It is faster than everything else by several orders of magnitude though
  """
  with open(fname, 'rb') as f:
    return marshal.load(f)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage: python rank.py task_number queryDocTrainData queryDocTrainRel queryDocTestData"
        exit(0)
    task_number = sys.argv[1]
    training_file = sys.argv[4]
    #Load idf
    idf = unserialize_data('model/idf')
    avg_doc_length = unserialize_data('model/avg_file_length')
    weights_file = open('Weights','w')
    if task_number == '1':
        #Build Cosine similarity measure
        scorer = CosineSimilarity(training_file, idf)
        weights_file.write(str(scorer.C1) + ' ' + str(scorer.C2) + ' '  + str(scorer.C3))
        weights_file.close()
    elif task_number == '2':
        #Build BM25 similarity measure
        scorer = BM25(training_file, idf, avg_doc_length)
        weights_file.write(str(scorer.W_title) + ' ' + str(scorer.W_body) + ' '  + str(scorer.W_anchor) + ' ' +\
                           str(scorer.B_title) + ' ' + str(scorer.B_body) + ' ' + str(scorer.B_anchor) + str(scorer.K1))
        weights_file.close
    elif task_number == '3':
        #Build smallest window similarity measure with Cosine Similarity
        scorer = SmallestWindow(training_file,"cosinesimilarity", idf)
        weights_file.write(str(scorer.C1) + ' ' + str(scorer.C2) + ' '  + str(scorer.C3) +  ' ' + str(scorer.B))
        weights_file.close()
    elif task_number == '4':
        #Build page_inportance model
        scorer = Inlinks(training_file,"cosinesimilarity", idf)
        weights_file.write(str(scorer.C1) + ' ' + str(scorer.C2) + ' '  + str(scorer.C3))
    scorer.rank()
    