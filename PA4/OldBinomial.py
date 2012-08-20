from __future__ import print_function

from message_iterators import MessageIterator
from collections import defaultdict
import math


class BinomialNB():
    def __init__(self, messageIterator):
        self.messageIterator = messageIterator
        self.prior = {}
        self.language_model = defaultdict(dict)
        self.V = set()
        
    #Goes through MessageIterator and trains the conditional probabilities needed for classification
    def train(self):
        N = 0
        for message in self.messageIterator:
            N += 1
            docClass = message.newsgroupnum
            self.prior[docClass] = self.prior.get(docClass,0) + 1
            wordsInDoc = set(message.body).union(set(message.subject))
            for word in wordsInDoc:
                self.language_model[word][docClass] = self.language_model[word].get(docClass,0) + 1
        self.V = set(self.language_model.keys())
        #Divide conditional probabilities by #docs in class
        for word in self.language_model.keys():
            for eachClass in self.prior.keys():
                self.language_model[word][eachClass] = (self.language_model[word].get(eachClass,0) + 1.0) / (self.prior[eachClass] + 2)
        #Divide raw counts of #docs of each class by total # of docs
        for each in self.prior.keys():
            self.prior[each]  = float(self.prior[each]) / N
        print(len(self.V))
    
    #Deliverable1: Go through first 20 messages in each newsgroup and output its P(c|d) in log scale
    def test(self):
        count = 0
        previousClass = 0
        correct = 0
        for msg in self.messageIterator:
            count += 1
            if count > 20 and msg.newsgroupnum == previousClass:
                continue
            elif count > 20 and msg.newsgroupnum != previousClass:
                count = 1
            previousClass = msg.newsgroupnum
            scoreVector = []
            for eachClass in self.prior.keys():
                score = 0
                prior = self.prior[eachClass]
                score += math.log(prior)
                wordsInDoc = set(msg.body).union(set(msg.subject))
                for word in wordsInDoc:
                    score += math.log(self.language_model[word][eachClass])
                for word in self.V - wordsInDoc:
                    score += math.log(1 - self.language_model[word][eachClass])
                scoreVector.append(score)
                print(score,end='\t')
            winner = max(scoreVector)
            winnerClass = scoreVector.index(winner)
            print(winnerClass)
            if winnerClass == msg.newsgroupnum:
                correct += 1
            print()
        #TODO: Remove following line before submitting
        print('Accuracy = ',correct/400.0)