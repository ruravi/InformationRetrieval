class Document:
	def __init__(self, q):
		self.url = ''
		self.title_str = ''
		self.title_terms = []
		self.title_vector = []
		self.hits = {}
		self.anchor_text = {}
		self.anchor_text_words = {}
		self.anchor_text_count = 0
		self.anchor_vector = []
		self.query = q
		self.body_length = 0
		self.number_inlinks = 0
	
	def set_title(self, title):
		self.title_str = title
		self.title_terms = self.title_str.split()
		
	def set_url(self, url):
		self.url = url.strip()
	
	def set_body_length(self, length):
		self.body_length = int(length.strip())
	
	def add_body_hits(self, term, hits):
		self.hits[term] = [int(y.strip()) for y in hits]
		
	def add_anchor_text(self, text, count):
		#rukmani: have made changes here
		self.number_inlinks = self.number_inlinks + int(count.strip())
		self.anchor_text[text] = int(count.strip())
		ct = int(count.strip())
		self.anchor_text_count = self.anchor_text_count + ct
		for w in text.split():
			self.anchor_text_words[w] = self.anchor_text_words.get(w,0) + ct
		
	def calculate_vectors(self):
		self.anchor_vector = []
		#rukmani: have made changes here
		self.anchor_vector = [self.anchor_text_words.get(each,0) for each in self.query.query_terms]
		self.title_vector = []
		for t in self.query.query_terms:
			if t in self.title_terms:
				self.title_vector.append(1)
			else:
				self.title_vector.append(0)
		
				
	