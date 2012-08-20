from __future__ import print_function

from message_iterators import MessageIterator
from collections import defaultdict
from collections import Counter
import math

class Twncb():
    
    def __init__(self, messageIterator):
        self.messageIterator = messageIterator
        self.prior = {}
        self.language_model = defaultdict(dict)
        self.V = 0
        
    def train(self):
        N = 0
        allDsInClass = defaultdict(int)
        allClasses = set()
        multinomialmodel = defaultdict(dict)
        docFrequency = defaultdict(int)
        #Calculate df[word]
        for message in self.messageIterator:
            N += 1
            wordsInDoc = set(message.body).union(set(message.subject))
            for word in wordsInDoc:
                docFrequency[word] += 1
        #Perform transforms
        for message in self.messageIterator:
            docClass = message.newsgroupnum
            allClasses.add(docClass)
            self.prior[docClass] = self.prior.get(docClass,0) + 1
            d = {}
            text = Counter()
            text.update(message.subject)
            text.update(message.body)
            for word,count in text.items():
                d[word] = math.log(count + 1) * math.log( float(N) / docFrequency[word])
            normalizeDenominator = math.sqrt( sum( [x**2 for x in d.values()] ) )
            for word,count in text.items():
                multinomialmodel[word][docClass] = multinomialmodel[word].get(docClass,0) + float(d[word]) / normalizeDenominator
                allDsInClass[docClass] += multinomialmodel[word][docClass]
        self.V = len(multinomialmodel.keys())
        #NC complement: count of all d's in classes other than c
        NCComplement = defaultdict(int)
        for eachClass in allClasses:
            for otherClass in allClasses - set([eachClass]):
                NCComplement[eachClass] += allDsInClass[otherClass]        
        weightsSum = defaultdict(float)
        #Get conditional probabilities : P(t|c) = d[ij] of term t not in c / #d[kj] of all terms k in all docs j not in c
        for word in multinomialmodel.keys():
            for eachClass in allClasses:
                NCicomplement = 0
                #NCiComplement hold d's of the word in docs of classes other than c
                for otherClass in allClasses - set([eachClass]):
                    NCicomplement += multinomialmodel[word].get(otherClass,0)
                self.language_model[word][eachClass] = math.log( (NCicomplement + 1.0) / (NCComplement[eachClass] + self.V) )
                weightsSum[eachClass] += abs(self.language_model[word][eachClass])
        #Weight normalize each word's conditional probability
        for word in multinomialmodel.keys():
            for eachClass in allClasses:
                self.language_model[word][eachClass] = self.language_model[word][eachClass] / float(weightsSum[eachClass])
        #Divide raw counts of #docs of each class by total # of docs
        for each in self.prior.keys():
            self.prior[each]  = float(self.prior[each]) / N
    
    
    def test(self):
        count = 0
        previousClass = 0
        correct = 0
        for msg in self.messageIterator:
            count += 1
            if count > 20 and msg.newsgroupnum == previousClass:
                continue
            elif count > 20 and msg.newsgroupnum != previousClass:
                print()
                count = 1
            previousClass = msg.newsgroupnum
            scoreVector = []
            for eachClass in self.prior.keys():
                score = 0
                for word, wordCount in msg.body.items():
                        score += self.language_model[word].get(eachClass,0) * wordCount
                #for word, wordCount in msg.subject.items():
                #        score += self.language_model[word].get(eachClass,0) * wordCount
                scoreVector.append(score)
            winner = min(scoreVector)
            winnerClass = scoreVector.index(winner)
            print(winnerClass,end='\t')
            if winnerClass == msg.newsgroupnum:
                correct += 1
