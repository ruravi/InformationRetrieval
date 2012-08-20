import math

class Query:
    def __init__(self, idf):
        self.query_string = ''
        self.query_terms = []
        self.docs = []
        self.idf_vec = []
        self.idf = idf
        self.N = 98998
        
    def add_doc(self, doc):
        self.docs.append(doc)
    
    def set_query(self, q):
        self.query_string = q.strip()
        self.query_terms = q.strip().split()
        self.idf_vec = [self.idf.get(each, 0.0) for each in self.query_terms]