from __future__ import print_function

import sys

sys.path.append('../libsvm/python')
from svmutil import *
from collections import Counter

class SVM():
    def __init__(self, messageIterator):
        self.messageIterator = messageIterator
        self.vocabulary = set()
        
    def train(self):
        #count vocabulary
        print('counting vocabulary')
        vocab = Counter()
        for msg in self.messageIterator:
            vocab.update(msg.subject)
            vocab.update(msg.body)
        self.vocabulary = list(vocab)
        #Populate input feature vectors
        print('populating feature vectors')
        y = []
        x = []
        for msg in self.messageIterator:
            y.append(msg.newsgroupnum)
            featurevector = [msg.body.get(eachword,0) for eachword in self.vocabulary]
            x.append(featurevector)
        print('training SVM')
        prob  = svm_problem(y, x)
        param = svm_parameter('-t 0 -c 4 -b 1')
        self.model = svm_train(prob, param)
        
        
    def test(self):
        print('Collecting Test Set: ')
        count = 0
        previousClass = 0
        goldLabels = []
        testset = []
        #Collect first 20 for testset
        for msg in self.messageIterator:
            count += 1
            if count > 20 and msg.newsgroupnum == previousClass:
                continue
            elif count > 20 and msg.newsgroupnum != previousClass:
                count = 1
            previousClass = msg.newsgroupnum
            goldLabels.append(msg.newsgroupnum)
            featurevector = [msg.body.get(eachword,0) for eachword in self.vocabulary]
            testset.append(featurevector)
        print('Predicting: ')
        p_label, p_acc, p_val = svm_predict(goldLabels, testset, self.model, '-b 1')
        