
from __future__ import print_function
import sys
from message_iterators import MessageIterator
from BinomialNB import BinomialNB
from BinomialChiSquare import BinomialChiSquare
from Twncb import Twncb
from Multinomial import MultinomialNB
#from SvmClassifier import SVM
from MultinomialChi2 import MultinomialChiSquare

def binomial(mi):
    classifier = BinomialNB(mi)
    classifier.train()
    classifier.test()

def binomial_chi2(mi):
    classifier = BinomialChiSquare(mi)
    classifier.train()
    classifier.test()

def multinomial(mi):
    classifier = MultinomialNB(mi)
    classifier.train()
    classifier.test()
    

def twcnb(mi):
    classifier = Twncb(mi)
    classifier.train()
    classifier.test()

def svm(mi):
    pass
#    classifier = SVM(mi)
#    classifier.train()
#    classifier.test()
    
def multinomial_chi2(mi):
    classifier = MultinomialChiSquare(mi)
    classifier.train()
    classifier.test()

def output_probability(probs):
  for i, prob in enumerate(probs):
    if i == 0:
      sys.stdout.write("{0:1.8g}".format(prob))
    else:
      sys.stdout.write("\t{0:1.8g}".format(prob))
  sys.stdout.write("\n")


MODES = {
    'binomial': binomial,
    'binomial-chi2': binomial_chi2,
    'multinomial': multinomial,
    'twcnb': twcnb,
    'svm': svm,
    'multinomial-chi2': multinomial_chi2
    # Add others here if you want
    }

def main():
  if not len(sys.argv) == 3:
    print("Usage: python {0} <mode> <train>".format(__file__), file=sys.stderr)
    sys.exit(-1)
  mode = sys.argv[1]
  train = sys.argv[2]

  mi = MessageIterator(train)

  try:
    MODES[mode](mi)
  except KeyError:
    print("Unknown mode: {0}".format(mode),file=sys.stderr)
    print("Accepted modes are: {0}".format(MODES.keys()), file=sys.stderr)
    sys.exit(-1)

if __name__ == '__main__':
  main()

