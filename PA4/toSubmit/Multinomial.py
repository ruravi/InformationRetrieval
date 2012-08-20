from __future__ import print_function

from message_iterators import MessageIterator
from collections import defaultdict
import math


class MultinomialNB():
    def __init__(self, messageIterator):
        self.messageIterator = messageIterator
        self.prior = {}
        self.language_model = defaultdict(dict)
        
    #Goes through MessageIterator and trains the conditional probabilities needed for classification
    def train(self):
        N = 0
        totalWordsInClass = {}
        for message in self.messageIterator:
            N += 1
            docClass = message.newsgroupnum
            self.prior[docClass] = self.prior.get(docClass,0) + 1
            for word,count in message.body.items():
                self.language_model[word][docClass] = self.language_model[word].get(docClass,0) + count
                totalWordsInClass[docClass] = totalWordsInClass.get(docClass,0) + count
            for word,count in message.subject.items():
                self.language_model[word][docClass] = self.language_model[word].get(docClass,0) + count
                totalWordsInClass[docClass] = totalWordsInClass.get(docClass,0) + count
        V = len(self.language_model.keys())
        #Divide raw counts of #docs of each class by total # of docs
        for each in self.prior.keys():
            self.prior[each]  = float(self.prior[each]) / N
        #Divide conditional probabilities by counts of all words in class
        for word in self.language_model.keys():
            for eachClass in totalWordsInClass.keys():
                self.language_model[word][eachClass] = (self.language_model[word].get(eachClass,0) + 1.0) / (totalWordsInClass[eachClass] + V)
    
    
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
                for word, wordCount in msg.body.items():
                        score += math.log(self.language_model[word][eachClass])
                for word, wordCount in msg.subject.items():
                        score += math.log(self.language_model[word][eachClass])
                scoreVector.append(score)
                print(score,end='\t')
            winner = max(scoreVector)
            winnerClass = scoreVector.index(winner)
            if winnerClass == msg.newsgroupnum:
                correct += 1
            print()