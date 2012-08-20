from QueryDocParser import QueryDocParser
from Query import Query
import math

class CosineSimilarity:
    
    def __init__(self, training_file, idf):
        self.training_file = training_file
        self.C1 = 0.1
        self.C2 = 0.1
        self.C3 = 0.8
        self.idf = idf
        
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
        total_doc_vector = [title_vector[i] + body_vector[i] + anchor_vector[i] for i in range(len(query_vector))]
        score = sum( [query_vector[i] * total_doc_vector[i] for i in range( len(query_vector) ) ] ) 
        return score
   
        
        
        