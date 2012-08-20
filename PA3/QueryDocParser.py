import sys
from Query import Query
from Document import Document

class QueryDocParser:
    def __init__(self, queryDocPath, idf):
        self.queryDocPath = queryDocPath
        self.avg_anchor_length = 0
        self.avg_title_length = 0
        self.avg_body_length = 0
        self.avg_anchors_per_doc = 0
        self.docs = 0
        self.titles = 0
        self.anchors = 0
        self.idf = idf
        
    def parse(self):
        queries = []
        c_query = None
        c_doc = None
        self.avg_anchor_length = 0
        self.avg_title_length = 0
        self.avg_body_length = 0
        self.docs = 0
        self.titles = 0
        self.anchors = 0
        f = open(self.queryDocPath, 'r')
        line = f.readline().strip()
        while True:
            if line == None or line == "":
                break
            elif line.startswith('query'):
                c_query = Query(self.idf)
                queries.append(c_query)
                c_query.set_query(line.split(':')[1])
            elif line.startswith('url'):
                self.docs+=1
                if not c_doc == None:
                    c_doc.calculate_vectors()
                c_doc = Document(c_query)
                c_query.add_doc(c_doc)
                c_doc.set_url(line)
            elif line.startswith('title'):
                c_doc.set_title(line.split(':')[1])
                self.avg_title_length += len(c_doc.title_terms)
                self.titles += 1
            elif line.startswith('body_hits'):
                x = line.split(':')[1].strip().split()
                term = x[0]
                hits = x[1:]
                c_doc.add_body_hits(term, hits)
            elif line.startswith('body_length'):
                c_doc.set_body_length(line.split(':')[1])
                self.avg_body_length += c_doc.body_length
            elif line.startswith('anchor_text'):
                text = line.split(':')[1].strip()
                line = f.readline()
                count = line.split(':')[1].strip()
                c_doc.add_anchor_text(text, count)
                self.avg_anchor_length += int(count)
                self.avg_anchors_per_doc += int(count)
            line = f.readline().strip()
            
        if not c_doc == None:
                c_doc.calculate_vectors()
        #We calculate avg anchor length as follows:
        #Consider all words in anchor text for a doc as one BIG document, so count up all occurrences of anchor words
        # and divide them by the number of docs
        self.avg_anchor_length = self.avg_anchor_length*1.0/self.docs
        self.avg_title_length = self.avg_title_length*1.0/self.titles 
        self.avg_body_length = self.avg_body_length*1.0/self.docs     
        self.avg_anchors_per_doc = self.avg_anchors_per_doc*1.0 / self.docs  
        return queries