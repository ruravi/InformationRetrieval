import math
from QueryDocParser import QueryDocParser

class SmallestWindow():
        
    def __init__(self, training_file, task, idf):
        self.training_file = training_file
        self.C1 = 0.1
        self.C2 = 0.1
        self.C3 = 0.8
        self.idf = idf
        self.B = 1;
        
    def rank(self):
        parser = QueryDocParser(self.training_file, self.idf)
        queries = parser.parse()
        #Go through each query. For each query do the following:
        # 1. For each url, compute its score
        # 2. Sort in descending order of score
        # 3. print out
        
        for each_query in queries:
            doc_score_map = {}
            for each_doc in each_query.docs:
                score = self.score_this_doc(each_doc, each_query.idf_vec)
                doc_score_map[each_doc.url] = score
            answers = doc_score_map.keys()
            answers.sort(key = lambda y: doc_score_map[y])
            print 'query: ' + str(each_query.query_string)
            for each_result in answers[::-1]:
                print " " + str(each_result)
            
    def score_this_doc(self, doc, query_vector):
        #Normalize title vector
        title_length = float(len(doc.title_terms))
        if title_length == 0:
            title_vector = [0.0] * len(query_vector)
        else:
            #title_vector = [self.C1 * each/title_length for each in doc.title_vector]
            #title_vector = [self.C1 * (1 + math.log10(each+1)) for each in doc.title_vector]
            title_vector = []
            for each in doc.title_vector:
                if each == 0:
                    title_vector.append(0)
                else:
                    title_vector.append(self.C1 * (1 + math.log10(each)))
                    #title_vector.append(self.C1 * each/title_length)
        #Form and normalize body vector
        len_body_vector = [len(doc.hits.get(each,[])) for each in doc.query.query_terms]
        if doc.body_length == 0:
            body_vector = [0.0] * len(query_vector)
        else:
            #body_vector = [self.C2 * float(each)/doc.body_length for each in body_vector]
            #body_vector = [self.C2 * (1 + math.log10(each+1)) for each in body_vector]
            body_vector = []
            for each in len_body_vector:
                if each == 0:
                    body_vector.append(0)
                else:
                    body_vector.append(self.C2 * (1 + math.log10(each)))
                    #body_vector.append(self.C2 * float(each)/doc.body_length)
        anchor_text_count = float( sum( doc.anchor_text_words.values() ) )
        #anchor_text_count = float(doc.anchor_text_count)
        if anchor_text_count == 0:
            anchor_vector = [0.0] * len(query_vector)
        else:
            #anchor_vector = [self.C3 * each/anchor_text_count for each in doc.anchor_vector]
            #anchor_vector = [self.C3 * (1+ math.log10(each+1)) for each in doc.anchor_vector]
            anchor_vector = []
            for each in doc.anchor_vector:
                if each == 0:
                    anchor_vector.append(0)
                else:
                    anchor_vector.append(self.C3 * (1 + math.log10(each)))
                    #anchor_vector.append(self.C3 * each/anchor_text_count)
        [smallest_window_title, smallest_window_body, smallest_window_anchor] = self.get_smallest_window(doc)
        smallest_window = min(smallest_window_title, smallest_window_body, smallest_window_anchor)
        #if smallest_window == float('inf'):
        #    Boost = 1
        #elif smallest_window == len(query_vector):
        #    Boost = self.B
        #else:
            #Boost = 1 + (1.0/smallest_window) * self.B 
        #    Boost = 1 + (self.B) * math.pow(math.e,-smallest_window)
        X = smallest_window / len(query_vector)
        Boost = (self.B-1) * math.pow(math.e,-X+1) + 1
        #total_doc_vector = [Boost_title * title_vector[i] + Boost_body* body_vector[i] + Boost_anchor * anchor_vector[i] for i in range(len(query_vector))]
        total_doc_vector = [title_vector[i] + body_vector[i] + anchor_vector[i] for i in range(len(query_vector))]
        score = sum( [query_vector[i] * total_doc_vector[i] for i in range( len(query_vector) ) ] ) 
        return score * Boost
   
        
    def get_window(self, pointers, hits):
        arr = [ hits[k][pointers[k]] for k in hits ]
        return max(arr) - min(arr)

    def all_pointers_valid(self, pointers, hits):
        for k in hits:
            if pointers[k] >= len(hits[k]):
                return False
        return True
    
    def advance_pointer(self, pointers, hits):
        mn = min([ hits[k][pointers[k]] for k in hits ])
        for k in hits:
            if hits[k][pointers[k]] == mn:
                pointers[k] += 1
                return pointers
        return pointers
    
    def get_smallest_window_from_lists(self, hits):
        pointers = {}
        for ht in hits:
            pointers[ht] = 0
            
        smallest_window = float('inf')
        while self.all_pointers_valid(pointers, hits):
            smallest_window = min([smallest_window, self.get_window(pointers, hits)])
            pointers = self.advance_pointer(pointers, hits)
        return int(smallest_window + 1)
    
    def get_smallest_window(self, doc):
        smallest_window = float('inf')
        pointers = {}
        query_hits = {}
        smalles_window_body = float('inf')
        smalles_window_title = float('inf')
        smalles_window_anchor = float('inf')
        win_body = True
        win_title = True
        win_anchor = True
        for qw in doc.query.query_terms:
            if qw in doc.hits:
                query_hits[qw] = doc.hits[qw]
            else:
                win_body = False
                break
        if win_body:
            smalles_window_body = self.get_smallest_window_from_lists(query_hits)
        
        query_hits = {}
        for qw in doc.query.query_terms:
            if qw in doc.title_terms:
                query_hits[qw] = [i for i in range(len(doc.title_terms)) if doc.title_terms[i] == qw]
            else:
                win_title = False
                break
        if win_title:
            smalles_window_title = self.get_smallest_window_from_lists(query_hits)
        
        query_hits = {}    
        for anchor in doc.anchor_text:
            anchor_words = anchor.split()
            query_hits = {}
            for qw in doc.query.query_terms:
                if qw in anchor_words:
                    query_hits[qw] = [i for i in range(len(anchor_words)) if anchor_words[i] == qw]
                else:
                    win_anchor = False
                    break
            if win_anchor:
                smalles_window_anchor = min([self.get_smallest_window_from_lists(query_hits), smalles_window_anchor])
        
        return [smalles_window_title, smalles_window_body, smalles_window_anchor]