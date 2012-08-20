from QueryDocParser import QueryDocParser
from Query import Query

class BM25():
    def __init__(self, training_file, idf, avg_doc_length):
        self.training_file = training_file
        self.B_title = 0.6
        self.B_body = 0.5
        self.B_anchor = 0.6
        self.W_title = 13
        self.W_body = 1
        self.W_anchor = 11
        self.K1 = 8
        self.idf = idf
        self.avg_doc_length = avg_doc_length
        
    def rank(self):
        parser = QueryDocParser(self.training_file, self.idf)
        queries = parser.parse()
        avg_lengths = [parser.avg_title_length, parser.avg_body_length, parser.avg_anchor_length]
        #Go through each query. For each query do the following:
        # 1. For each url, compute its score
        # 2. Sort in descending order of score
        # 3. print out
        for each_query in queries:
            doc_score_map = {}
            for each_doc in each_query.docs:
                score = self.score_this_doc(each_doc, each_query.idf_vec, avg_lengths)
                doc_score_map[each_doc.url] = score
            answers = doc_score_map.keys()
            answers.sort(key = lambda y: doc_score_map[y])
            print 'query: ' + str(each_query.query_string)
            for each_result in answers[::-1]:
                print " " + str(each_result)
    
    # doc - DOc object containing the info about title,query and anchor words/Tf
    # query_vector = [term1 term2 ...]
    #avg_lengths = average lengths of [title body anchor_text]
    def score_this_doc(self, doc, query_vector, avg_lengths):
        #Normalize title vector
        title_length = float(len(doc.title_terms))
        title_vector = []
        for each in doc.title_vector:
            if each == 0:
                title_vector.append(0)
            else:
                title_vector.append( each / (1 + self.B_title * (title_length/avg_lengths[0] - 1 ) ) )
        #Form and normalize body vector
        len_body_vector = [len(doc.hits.get(each,[])) for each in doc.query.query_terms]
        body_vector = []
        for each in len_body_vector:
            if each == 0:
                body_vector.append(0)
            else:
                body_vector.append(each / (1 + self.B_body * ( float(doc.body_length) / self.avg_doc_length - 1) ) )
        anchor_text_count = float( sum( doc.anchor_text_words.values() ) )
        anchor_vector = []
        for each in doc.anchor_vector:
            if each == 0:
                anchor_vector.append(0)
            else:
                anchor_vector.append(each / (1 + self.B_anchor * ( anchor_text_count / avg_lengths[2] - 1 ) ) )
        total_doc_vector = [self.W_title*title_vector[i] + self.W_body * body_vector[i] + \
                            self.W_anchor * anchor_vector[i] for i in range(len(query_vector))]
        score = sum( [float(query_vector[i]) * total_doc_vector[i] / (self.K1 + total_doc_vector[i]) for i in range( len(query_vector) ) ] ) 
        return score
   
        
    