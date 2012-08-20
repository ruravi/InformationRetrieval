
import math
import heapq
import random

class TFIDF:
	def __init__(self, mi, k=5):
		self.mi = mi
		self.k = k
		self.initialize()
		
	def initialize(self):
		self.tf = {}
		self.occurs_in_class = {}
		self.icf = {}
		self.occurs_in_doc = {}
		self.class_vectors = {}
		self.tfidf_vec = {}
		self.class_of = {}
		for i in range(self.mi.numgroups):
			self.tf[i] = {}
			self.class_vectors[i] = {}
		self.total_messages = self.mi.tot_msgs
		self.correct = 0
		
	def get_icf(self, w):
		if w in self.occurs_in_class:
			return 1 + math.log10(len(self.occurs_in_class[w]))
		else:
			return 1
		
	
	def get_idf(self, w):
		if w in self.occurs_in_doc:
			return 1 + math.log10(len(self.occurs_in_doc[w]))
		else:
			return 1
		
	def get_tfidf(self, m, idf = True):
		test_tf = {}
		tf_idf = {}
		sm = 0
		for w in m.body:
			test_tf[w] = test_tf.get(w,0) +  m.body[w]
			sm += test_tf[w]*test_tf[w];
		sm = math.sqrt(sm)
		
		
		if idf:
			sm = 0
			for w in test_tf:
				tf_idf[w] = test_tf[w]*self.get_idf(w)
				sm += (tf_idf[w]*tf_idf[w])
			sm = math.sqrt(sm)
		
			for w in test_tf:
				tf_idf[w] /= sm
			return tf_idf
		else:
			for w in test_tf:
				test_tf[w] /= sm
			return test_tf
	
	def train1(self):
		self.initialize()
		for m in self.mi:
			if m.isTest(self.mi.num_msgs):
				continue

			for w in m.body:
				self.occurs_in_doc[w] = self.occurs_in_doc.get(w, {})
				self.occurs_in_doc[w][m.newsgroupnum] = 1
					
			#for w in m.subject:
			#	self.occurs_in_doc[w] = self.occurs_in_doc.get(w, {})
			#	self.occurs_in_doc[w][m.newsgroupnum] = 1
		i = 0
		for m in self.mi:
			i+=1
			if m.isTest(self.mi.num_msgs):
				continue

			self.tfidf_vec[i] = self.get_tfidf(m)
			self.class_of[i] = m.newsgroupnum

	def train(self):
		self.initialize()
		for m in self.mi:
			if m.isTest(self.mi.num_msgs):
				continue
			if not self.should_user(m.newsgroupnum):
				continue
			for w in m.body:
				self.tf[m.newsgroupnum][w] = self.tf.get(m.newsgroupnum, {}).get(w, 0) + m.body[w]
				self.occurs_in_class[w] = self.occurs_in_class.get(w, {})
				self.occurs_in_class[w][m.newsgroupnum] = 1
				self.occurs_in_doc[w][m.newsgroupnum] = 1
					
			for w in m.subject:
				self.tf[m.newsgroupnum][w] = self.tf.get(m.newsgroupnum, {}).get(w, 0) + m.subject[w]
				self.occurs_in_class[w] = self.occurs_in_class.get(w, {})
				self.occurs_in_class[w][m.newsgroupnum] = 1
				self.occurs_in_doc[w][m.newsgroupnum] = 1
				
		for c in range(self.mi.numgroups):
			sm = 0
			for w in self.tf[c]:
				self.class_vectors[c][w] = self.tf[c].get(w, 0) * self.get_icf(w)
				sm += math.pow(self.class_vectors[c][w], 2.0)
			sm = math.sqrt(sm)
			for w in self.tf[c]:
				self.class_vectors[c][w] = self.class_vectors[c][w]/sm
			
			
			
	def get_prob_xk(self, cj, w ):
		if w in self.prob_xk_cj[cj]:
			return self.prob_xk_cj[cj][w]
		else:
			return 1.0*self.k / (self.k*(len(self.vocab_cj[cj])))
	
	def get_prob_xk_body(self, cj, w ):
		if w in self.prob_xk_body_cj[cj]:
			return self.prob_xk_body_cj[cj][w]
		else:
			return 1.0*self.k / (self.k*(len(self.vocab_body_cj[cj])))
		
	def get_prob_xk_subject(self, cj, w ):
		if w in self.prob_xk_subject_cj[cj]:
			return self.prob_xk_subject_cj[cj][w]
		else:
			return 1.0*self.k / (self.k*(len(self.vocab_subject_cj[cj])))
	
	def get_class_probs(self, mi):
		probs = []
		mx = float('-inf')
		mx_index = -1
		for i in range(self.mi.numgroups):
			p1 = 0
			p2 = 0
			if self.body_weight > 0:
				for w in mi.body:
					try:
						p2 += math.log( self.get_prob_xk_body(i, w) )
					except:
						print 'Error'
			if self.subject_weight > 0:
				for w in mi.subject:
					p1 + math.log( self.get_prob_xk_subject(i, w) )
				
			p =  self.body_weight*p1 + self.subject_weight*p2 + math.log(self.prob_cj[i])		
		
			if p >= mx:
				mx = p
				mx_index = i
			probs.append( p )
		#probs.reverse()
		#probs.append(mx_index)
		#print "%d, %d" %(mx_index, mi.newsgroupnum)
		if mx_index == mi.newsgroupnum:
			self.correct+=1
		#print self.correct
		#probs.reverse()
		return [probs, mx_index]
		
	def get_class(self, m):
		test_tf = {}
		sm = 0
		for w in m.body:
			test_tf[w] = test_tf.get(w,0) +  m.body[w]
			sm += math.pow(test_tf[w], 2.0)
		for w in m.subject:
			test_tf[w]  = test_tf.get(w,0) + m.subject[w]
			sm += math.pow(test_tf[w], 2.0)
		sm = math.sqrt(sm)
		for w in test_tf:
			test_tf[w] = test_tf[w]/sm
		mx = float('-inf')
		mx_class = -1
		for c in self.class_vectors:
			v = 0
			for w in self.class_vectors[c]:
				v += self.class_vectors[c][w] * test_tf.get(w, 0)
			if v > mx:
				mx = v
				mx_class = c
		if mx_class == m.newsgroupnum:
			self.correct += 1
		return mx_class
	

	
	def get_class_kNN(self, m):
		mn = float('-inf')
		test_tfidf = self.get_tfidf(m, False)
		i = 0
		h = []
		for m1 in self.mi:
			i += 1
			if m1.isTest(self.mi.num_msgs):
				continue
			if not i in self.tfidf_vec:
				continue
			v = 0
			for w in self.tfidf_vec[i]:
				v += self.tfidf_vec[i][w] * test_tfidf.get(w, 0)
			heapq.heappush( h, [ v, self.class_of[i] ] )
			if len(h) > self.k:
				heapq.heappop(h)
		
		c_n = {}
		for v, i in h:
			c_n[i] = c_n.get(i, 0) + 1
		mx = max(c_n.values())
		mx_classes = [ x for x in c_n if c_n[x] == mx ]
		if len(mx_classes) > 1:
			h.reverse()
			for v, i in h:
				if i in mx_classes:
					mx_class = i
					break
		else:
			mx_class = mx_classes[0]
		if mx_class == m.newsgroupnum:
			self.correct += 1
		return mx_class
			
				