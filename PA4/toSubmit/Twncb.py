from __future__ import print_function

from message_iterators import MessageIterator
from collections import defaultdict
import math

class Twncb():
	
	def __init__(self, messageIterator):
		self.messageIterator = messageIterator
		self.prior = {}
		self.language_model = defaultdict(dict)
		self.V = 0
		self.correct = 0
		
	def train(self):
		N = 0
		allDsInClass = defaultdict(int)
		allClasses = set()
		multinomialmodel = defaultdict(dict)
		docFrequency = defaultdict(int)
		#Calculate df[word]
		for message in self.messageIterator:
			if message.isTest(self.messageIterator.num_msgs):
				continue
			N += 1
			for word,count in message.body.items():
				docFrequency[word] += 1
		#Perform transforms
		for message in self.messageIterator:
			if message.isTest(self.messageIterator.num_msgs):
				continue
			docClass = message.newsgroupnum
			allClasses.add(docClass)
			self.prior[docClass] = self.prior.get(docClass,0) + 1
			d = {}
			for word,count in message.body.items():
				d[word] = math.log(count + 1) * math.log( float(N) / docFrequency[word])
			normalizeDenominator = math.sqrt( sum( [x**2 for x in d.values()] ) )
			for word,count in message.body.items():
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
				#score += math.log(1.0/20)
				for word, wordCount in msg.body.items():
						score += self.language_model[word].get(eachClass,0) * wordCount
				scoreVector.append(score)
				#print(score,end='\t')
			winner = min(scoreVector)
			winnerClass = scoreVector.index(winner)
			print(winnerClass,end='\t')
			if winnerClass == msg.newsgroupnum:
				correct += 1

	def test_marked(self):
		self.t = 0
		for msg in self.messageIterator:
			if not msg.isTest(self.messageIterator.num_msgs):
				continue
			scoreVector = []
			for eachClass in self.prior.keys():
				score = 0
				#score += math.log(1.0/20)
				for word, wordCount in msg.body.items():
						score += self.language_model[word].get(eachClass,0) * wordCount
				scoreVector.append(score)
				#print(score,end='\t')
			winner = min(scoreVector)
			winnerClass = scoreVector.index(winner)
			#print(winnerClass,end='\t')
			self.t+=1
			if winnerClass == msg.newsgroupnum:
				self.correct += 1

