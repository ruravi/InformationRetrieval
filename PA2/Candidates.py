class Candidates:
    
    def __init__(self, lm, em):
        self.languagemodel = lm
        self.editmodel = em
    
    # Returns a set of tuples - each tuple is a (candidate word, its probability, isJoin) 
    # So returns set( (word,prob,true) , (word,prob,false), (), ... )
    def generate_candidates(self, prevword, word):
        # Here consider the possibility of two words joined together
        separate = self.generate_splits_of_word(word)
        if self.languagemodel.known(word):
            word_unchanged = set([(word, self.editmodel.getprob_of_word_itself(), False)])
        else:
            word_unchanged = set()
        isJoin = False
        candidates = word_unchanged | self.editmodel.known_edits1(word, isJoin) | self.editmodel.known_edits2(word, isJoin) 
        #check if prevword is not empty, otherwise a word with itself will be marked True for isjoin
        isJoin = True
        if prevword is not "":
            if self.languagemodel.known(prevword + word):
                candidates = candidates | set([(prevword + word, self.editmodel.getprob_of_join(prevword,word), isJoin)])
        for each in separate:
            candidates.add(each)
        return candidates
    
    def generate_splits_of_word(self, word):
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        candidate = []
        for word1,word2 in splits:
            if self.languagemodel.known(word1) and self.languagemodel.known(word2):
                candidate.append( ( (word1,word2), self.editmodel.getprob_of_split(word1,word2), False) )
        return candidate