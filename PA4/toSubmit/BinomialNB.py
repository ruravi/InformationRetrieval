from __future__ import print_function

from message_iterators import MessageIterator
from collections import defaultdict
import math


class BinomialNB():
	def __init__(self, messageIterator):
		self.messageIterator = messageIterator
		self.prior = defaultdict(int)
		self.language_model = defaultdict(dict)
		self.vocabulary = set()
		self.top300 = set()
		self.classes = set()
		self.correct = 0
		self.top300_dict = {}
	
	
	#Returns a dict of dicts of words and their class frequencies of only the top 300 words for its class
	#Needs as input a list of words in the document i.e Vocabulary, a dict of dicts of raw counts 
	def selectFeatures(self, classId, N, totalNumDocs):
		top300Features = defaultdict(dict)
		mutualInfo = {}
		totalNumDocs += float(2*len(self.classes))
		for word in self.vocabulary:
			#Assume there are 2 more documents in each class that contain/don't contain the word respectively
			N11 = N[word][classId] + 1
			N1dot = sum(N[word].values()) + len(self.classes)
			N10 = N1dot - N11
			N0dot = totalNumDocs - N1dot
			Ndot1 = self.prior[classId] + 2
			Ndot0 = totalNumDocs - Ndot1
			N01 = Ndot1 - N11
			N00 = N0dot - N01
			mutualInfo[word] = float(N11) / totalNumDocs * math.log(totalNumDocs * N11 / (N1dot * Ndot1), 2) + \
							   float(N01) / totalNumDocs * math.log(totalNumDocs * N01 / (N0dot * Ndot1), 2) + \
							   float(N10) / totalNumDocs * math.log(totalNumDocs * N10 / (N1dot * Ndot0), 2) + \
							   float(N00) / totalNumDocs * math.log(totalNumDocs * N00 / (N0dot * Ndot0), 2)
		allWords = mutualInfo.keys()
		allWords.sort(key = lambda x: mutualInfo[x])
		allWords = allWords[-300:]
		allWords.reverse()
		for each in allWords:
			top300Features[each] = N[each]
		return top300Features
		
	#Goes through MessageIterator and trains the conditional probabilities needed for classification
	def train(self):
		N = defaultdict(dict)
		totalNumDocs = 0
		for msg in self.messageIterator:
			totalNumDocs += 1
			eachClass = msg.newsgroupnum
			self.prior[eachClass] += 1
			self.classes.add(eachClass)
			wordsInDoc = set(msg.body).union(set(msg.subject))
			for word in wordsInDoc:
				N[word][eachClass] = N[word].get(eachClass,0) + 1
		#Do the next dummy step, so that each word gets an entry in its dict for every class
		for word in N.keys():
			for eachClass in self.classes:
				N[word][eachClass] = N[word].get(eachClass,0)
		self.vocabulary = set(N.keys())
		for eachClass in self.classes:
			self.language_model.update(self.selectFeatures(eachClass, N, totalNumDocs))
		self.top300 = set(self.language_model.keys())
		#Divide raw count of docs in class containing word by total no. of docs in class 
		for word in self.language_model.keys():
			for eachClass in self.classes:
				self.language_model[word][eachClass] = (self.language_model[word][eachClass] + 1.0) / (self.prior[eachClass] + 2)
		#Divide raw counts of #docs of each class by total # of docs
		for each in self.prior.keys():
			self.prior[each]  = float(self.prior[each]) / totalNumDocs
			
		for w in self.top300:
			self.top300_dict[w] = 1
	
	#Deliverable1: Go through first 20 messages in each newsgroup and output its P(c|d) in log scale
	def test(self):
		count = 0
		previousClass = 0
		self.correct = 0
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
						score += math.log(self.language_model.get(word,{}).get(eachClass,1))
				for word in self.top300 - wordsInDoc:
					score += math.log(1 - self.language_model.get(word,{}).get(eachClass,0))
				scoreVector.append(score)
				print(score,end='\t')
			winner = max(scoreVector)
			winnerClass = scoreVector.index(winner)
			if winnerClass == msg.newsgroupnum:
				self.correct += 1
			print()

	def test_marked(self):

		self.correct = 0
		self.t = 0
		for msg in self.messageIterator:
			if msg.isTest(self.messageIterator.num_msgs) == False:
				continue
			
			wordsInDoc = {}
			for w in msg.subject:
				wordsInDoc[w] = 1
			for w in msg.body:
				wordsInDoc[w] = 1
			scoreVector = []
			for eachClass in self.prior.keys():
				score = 0
				prior = self.prior[eachClass]
				score += math.log(prior)
				for word in wordsInDoc:
						score += math.log(self.language_model.get(word,{}).get(eachClass,1))
				for word in self.top300_dict:
					if word in wordsInDoc:
						continue
					score += math.log(1 - self.language_model.get(word,{}).get(eachClass,0))
				scoreVector.append(score)
			winner = max(scoreVector)
			winnerClass = scoreVector.index(winner)
			#print(winnerClass, msg.newsgroupnum, self.correct)
			if winnerClass == msg.newsgroupnum:
				self.correct += 1
			self.t += 1
				