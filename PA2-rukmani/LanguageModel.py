import marshal
import math
from EditModel import EditModel

class LanguageModel:
    
    def __init__(self,unigramfile, bigramfile, em=0):
        self.unigram_prob = self.unserialize_data(unigramfile)
        self.bigram_prob = self.unserialize_data(bigramfile)
        self.editmodel = em
        #Lambda gives more importance to bigram prob than to backed off unigram prob
        self.LAMBDA = 0.1
        #Mu gives equal importance to language model and error model
        self.MU = 1
        
    def init_edit_model(self, em):
        self.editmodel = em
        
    def unserialize_data(self,fname):
        """
        Reads a pickled data structure from a file named `fname` and returns it
        IMPORTANT: Only call marshal.load( .. ) on a file that was written to using marshal.dump( .. )
        marshal has a whole bunch of brittle caveats you can take a look at in teh documentation
        It is faster than everything else by several orders of magnitude though
        """
        with open(fname, 'rb') as f:
            return marshal.load(f)
        
    def known(self, word):
        return word in self.unigram_prob
    
    # Returns the word in the sequence with max Unigram probability
    # and the value of the maximum unigram prob as a tuple (word, log probability)
    # Sequence is a set of tuples of type(candidate_word, prob of error)
    def unigram_max(self,sequence):
        sequence = list(sequence)
        sequence.sort(key = lambda tuple: self.getGramProb( tuple[0], tuple[1] ) )
        most_probable_word = sequence[-1][0]
        if type(most_probable_word) is tuple:
            score = math.log(sequence[-1][1]) + self.MU * math.log( self.get_bigram_prob(most_probable_word[0],most_probable_word[1]))
            most_probable_word = most_probable_word[::-1]
            most_probable_word = ' '.join(most_probable_word)
        else:
            score = math.log(sequence[-1][1]) + self.MU * math.log( self.unigram_prob[most_probable_word])
        return (most_probable_word, score)
    
    def getGramProb(self, word, error_prob):
        if type(word) is tuple:
            return math.log( self.get_bigram_prob(word[0], word[1]) ) + math.log(error_prob)
        else:
            return math.log( self.unigram_prob[word] ) + math.log(error_prob) 
    def getGramProb_nolog(self, word):
        if type(word) is tuple:
            return  self.get_bigram_prob(word[0], word[1])
        else:
            return self.unigram_prob[word]
        
    # We assume that the unigram is always present in the dictionary
    def get_bigram_prob(self, word1, word2):
        if word1 == "":
            return self.unigram_prob[word2]
        return self.LAMBDA * self.unigram_prob[word2] + (1 - self.LAMBDA) * self.bigram_prob.get((word1,word2),0)

    def add_up_scores(self, word, prevword, error_prob, score_of_rest):
        if type(word) is tuple:
            return math.log( self.MU * self.get_bigram_prob(prevword, word[0])) + \
                             self.MU * math.log(self.get_bigram_prob(word[0], word[1])) + \
                             math.log(error_prob) + score_of_rest
        else:    
            return math.log( self.MU * self.get_bigram_prob(prevword, word)) + math.log(error_prob) + score_of_rest


