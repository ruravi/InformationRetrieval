from __future__ import print_function

from message_iterators import MessageIterator
from collections import defaultdict
import math
from collections import Counter


class MultinomialChiSquare():
	def __init__(self, messageIterator):
		self.messageIterator = messageIterator
		self.prior = defaultdict(int)
		self.language_model = defaultdict(dict)
		self.vocabulary = set()
		self.top300 = set()
		self.output = True
	
	#Returns a dict of dicts of words and their class frequencies of only the top 300 words for its class
	#Needs as input a list of words in the document i.e Vocabulary, a dict of dicts of raw counts 
	def selectFeatures(self, classId, N, totalNumDocs):
		top300Features = defaultdict(dict)
		chiSquare = {}
		for word in self.vocabulary:
			N11 = N[word][classId]
			N1dot = sum(N[word].values())
			N10 = N1dot - N11
			N0dot = totalNumDocs - N1dot
			Ndot1 = self.prior[classId]
			N01 = Ndot1 - N11
			N00 = N0dot - N01
			chiSquare[word] = float(totalNumDocs) * (N11 * N00 - N10 * N01) ** 2 / ( (N11 + N01) * (N11 + N10) * (N10 + N00) * (N01 + N00) )
		allWords = chiSquare.keys()
		allWords.sort(key = lambda x: chiSquare[x])
		allWords = allWords[-300:]
		allWords.reverse()
		#Deliverable 2: Output 20 best words in each class
		if self.output:
			for word in allWords[:20]:
				print(word,end='\t')
			print()
		for each in allWords:
			top300Features[each] = N[each]
		return top300Features
	
	#Populates a dict of dicts containing raw counts of terms in classes. selects 300 features for each class
	#and populates the language model with the union of the 300 features from all classes
	def train(self):
		N = defaultdict(dict)
		classes = set()
		totalNumDocs = 0
		totalWordsInClass = {}
		for msg in self.messageIterator:
			
			if msg.isTest(self.messageIterator.num_msgs):
				continue
			totalNumDocs += 1
			eachClass = msg.newsgroupnum
			self.prior[eachClass] += 1
			classes.add(eachClass)
			text = Counter()
			text.update(msg.subject)
			text.update(msg.body)
			for word,count in text.items():
				self.language_model[word][eachClass] = self.language_model[word].get(eachClass,0) + count
				totalWordsInClass[eachClass] = totalWordsInClass.get(eachClass,0) + count
				N[word][eachClass] = N[word].get(eachClass,0) + 1
		#Do the next dummy step, so that each word gets an entry in its dict for every class
		for word in N.keys():
			for eachClass in classes:
				N[word][eachClass] = N[word].get(eachClass,0)
		#Select 300 features from each class
		self.vocabulary = set(N.keys())
		top = defaultdict(dict)
		for eachClass in classes:
			top.update(self.selectFeatures(eachClass, N, totalNumDocs))
		#Select the vocabulary
		self.top300 = set(top.keys())
		#Recompute total# words in each class based on only the top300 words
		totalWordsInClass = defaultdict(int)
		for word in self.top300:
			for eachClass in classes:
				totalWordsInClass[eachClass] += self.language_model[word].get(eachClass,0)
		#Divide raw count of docs in class containing word by total no. of docs in class 
		for word in self.language_model.keys():
			for eachClass in totalWordsInClass.keys():
				self.language_model[word][eachClass] = (self.language_model[word].get(eachClass,0) + 1.0) / (totalWordsInClass[eachClass] + len(self.top300))
		#Divide raw counts of #docs of each class by total # of docs
		for each in self.prior.keys():
			self.prior[each]  = float(self.prior[each]) / totalNumDocs
	
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
				text = Counter()
				text.update(msg.subject)
				text.update(msg.body)
				for word, wordCount in text.items():
					if word in self.top300:
						score += math.log(self.language_model.get(word,{}).get(eachClass,1)) * wordCount
				scoreVector.append(score)
				print(score,end='\t')
			winner = max(scoreVector)
			winnerClass = scoreVector.index(winner)
			#print(winnerClass)
			if winnerClass == msg.newsgroupnum:
				correct += 1
			print()
		
		
	def test_marked(self):
		self.t = 0
		self.correct = 0
		for msg in self.messageIterator:
			if not msg.isTest(self.messageIterator.num_msgs):
				continue
			
			scoreVector = []
			for eachClass in self.prior.keys():
				score = 0
				prior = self.prior[eachClass]
				score += math.log(prior)
				text = Counter()
				text.update(msg.subject)
				text.update(msg.body)
				for word, wordCount in text.items():
					if word in self.top300:
						score += math.log(self.language_model.get(word,{}).get(eachClass,1)) * wordCount
				scoreVector.append(score)
				#print(score,end='\t')
			winner = max(scoreVector)
			winnerClass = scoreVector.index(winner)
			#print(winnerClass)
			self.t +=1
			#print(winnerClass,end='\t')
			if winnerClass == msg.newsgroupnum:
				self.correct += 1
			#print()
	
	
		