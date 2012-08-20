
from __future__ import print_function

import sys
from Multinomial import Multinomial
from BinomialNB import BinomialNB
from BinomialChiSquare import BinomialChiSquare
from Twncb import Twncb
from TFIDF import TFIDF
from SvmClassifier import SVM
from MultinomialChi2 import MultinomialChiSquare

from collections import Counter
from message_iterators import MessageIterator
from message_features import MessageFeatures

def binomial(mi):
	MessageFeatures.test_fold = -1
	classifier = BinomialNB(mi)
	classifier.train()
	classifier.test()

def binomial_chi2(mi):
	MessageFeatures.test_fold = -1
	classifier = BinomialChiSquare(mi)
	classifier.train()
	classifier.test()

def multinomial(mi):
	MessageFeatures.test_fold = -1
	mn = Multinomial(mi)
	mn.train()
	mn.test()
	#print(mn.correct)	
	pass

def multinomial_chi2(mi):
    classifier = MultinomialChiSquare(mi)
    classifier.train()
    classifier.test()

def tfidf(mi):
	MessageFeatures.test_fold = -1
	tf = TFIDF(mi, 3)
	tf.train1()
	cj = 0
	cj_count = 0
	tf.correct = 0
	cj = 0
	cj_count = 0
	tf.correct = 0
	for m in mi:
		if cj_count >= 20:
			cj_count = 0
			cj += 1
		elif m.newsgroupnum == cj:
			cj_count += 1
			c = tf.get_class_kNN(m)
			print(c)
	print(tf.correct)	
	pass

def kfcvkNN(mi, k=10):
	correct = []
	tested = []
	tot = 0
	cor = 0
	for i in range(k):
		#mark_test_set(mi, k, i)
		MessageFeatures.test_fold = i
		MessageFeatures.folds = k
		
		tf = TFIDF(mi, 3)
		tf.train1()
		tf.correct = 0
		tf.correct = 0
		c = 0
		t = 0
		for m in mi:
			if m.isTest(mi.num_msgs):
				cl = tf.get_class_kNN(m)
				#print(cl)
				if cl == m.newsgroupnum:
					c+=1
				t+=1
		print(tf.correct)	
		correct.append(c)
		tested.append(t)
		tot+=t
		cor+=c
	print (1.0*cor/tot)
		
	pass

def mark_test_set(mi, k, f):
	cj = -1
	cj_index = 0
	for m in mi:
		if not cj == m.newsgroupnum:
			cj+=1
			cj_index = 0
		else:
			cj_index += 1
		if cj_index >= (f*mi.num_msgs[cj]/k) and cj_index < ((f+1)*mi.num_msgs[cj]/k):
			m.isTest = True
		else:
			m.isTest = False
			
def kfcvmc(mi, k=10):
	correct = []
	tested = []
	c = 0
	t = 0
	for i in range(k):
		#mark_test_set(mi, k, i)
		MessageFeatures.test_fold = i
		MessageFeatures.folds = k
		bn = MultinomialChiSquare(mi)
		bn.output = False
		bn.train()
		bn.test_marked()
		c = bn.correct
		t = bn.t
		correct.append(c)
		tested.append(t)
	print (1.0*sum(correct)/sum(correct))
	
def kfcvm(mi, k=10):
	correct = []
	tested = []
	tot = 0
	cor = 0
	for i in range(k):
		#mark_test_set(mi, k, i)
		MessageFeatures.test_fold = i
		MessageFeatures.folds = k
		mn = Multinomial(mi)
		mn.train()
		mn.test_marked()
	
def kfcvb(mi, k=10):
	correct = []
	tested = []
	c = 0
	t = 0
	for i in range(k):
		#mark_test_set(mi, k, i)
		MessageFeatures.test_fold = i
		MessageFeatures.folds = k
		bn = BinomialNB(mi)
		bn.train()
		bn.test_marked()
		c = bn.correct
		t = bn.t
		correct.append(c)
		tested.append(t)
	print (1.0*sum(correct)/sum(correct))

def kfcvbc(mi, k=10):
	correct = []
	tested = []
	c = 0
	t = 0
	for i in range(k):
		#mark_test_set(mi, k, i)
		MessageFeatures.test_fold = i
		MessageFeatures.folds = k
		bn = BinomialChiSquare(mi)
		bn.display = False
		bn.train()
		bn.test_marked()
		c = bn.correct
		t = bn.t
		correct.append(c)
		tested.append(t)
	print (1.0*sum(correct)/sum(correct))
	
def kfcvtwcnb(mi, k=10):
	correct = []
	tested = []
	c = 0
	t = 0
	for i in range(k):
		#mark_test_set(mi, k, i)
		MessageFeatures.test_fold = i
		MessageFeatures.folds = k
		bn = Twncb(mi)
		bn.train()
		bn.test_marked()
		c = bn.correct
		t = bn.t
		correct.append(c)
		tested.append(t)
	print (1.0*sum(correct)/sum(correct))

def twcnb(mi):
	classifier = Twncb(mi)
	classifier.train()
	classifier.test()


def svm(mi):
    classifier = SVM(mi)
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
		'kfcvm': kfcvm,
		'kfcvb': kfcvb,
		'kfcvbc': kfcvbc,
		'tfidf': tfidf,
		'kfcvknn': kfcvkNN,
        'svm': svm,
        'kfcvtwcnb': kfcvtwcnb,
        'multinomial-chi2': multinomial_chi2,
        'kfcvmc': kfcvmc
		# Add others here if you want
		}

def main():
	if not len(sys.argv) == 3:
		print("Usage: python {0} <mode> <train>".format(__file__), file=sys.stderr)
		sys.exit(-1)
	mode = sys.argv[1]
	train = sys.argv[2]

	mi = MessageIterator(train)

	#try:
	MODES[mode](mi)
	#except KeyError:
	#	print("Unknown mode: {0}".format(mode),file=sys.stderr)
	#	print("Accepted modes are: {0}".format(MODES.keys()), file=sys.stderr)
	#	sys.exit(-1)

if __name__ == '__main__':
	main()

