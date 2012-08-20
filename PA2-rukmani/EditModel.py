import marshal

class EditModel():
    
    def __init__(self, kind, lm=None):
        self.alphabet = "abcdefghijklmnopqrstuvwxyz0123546789&$+_'"
        self.languagemodel = lm
        self.kind = kind
        if self.kind == 'empirical':
            self.P = 0.05
            self.edit_prob = self.unserialize_data('edit_model')
            self.char_unigram_count = self.unserialize_data('char_unigram_model')
            self.char_bigram_count = self.unserialize_data('char_bigram_model')
        elif self.kind == 'uniform':
            self.P = 0.05
            self.edit_prob = self.unserialize_data('edit_model')
            self.char_unigram_count = self.unserialize_data('char_unigram_model')
            self.char_bigram_count = self.unserialize_data('char_bigram_model')
        self.nc = 4
        self.dl = 0
        self.ins = 1
        self.sub = 2
        self.trs = 3
        self.threshold = 0.0001
    
    def unserialize_data(self,fname):
        """
        Reads a pickled data structure from a file named `fname` and returns it
        IMPORTANT: Only call marshal.load( .. ) on a file that was written to using marshal.dump( .. )
        marshal has a whole bunch of brittle caveats you can take a look at in teh documentation
        It is faster than everything else by several orders of magnitude though
        """
        with open(fname, 'rb') as f:
            return marshal.load(f)

    #Following methods are for the uniform edit model  
    
    #Prob of word itself is highest = 1-P      
    def getprob_of_word_itself(self):
        return 1-self.P
    
    # A word splitting into two is slightly worse than a word at 1 edit distance away
    def getprob_of_split(self, word1, word2):
        return self.get_e_prob((self.dl, word1[-1]+ ' '))
    
    def getprob_of_join(self, word, nextword):
        return self.get_e_prob((self.ins, word[-1]+ ' '))
    
    def known_edits1(self, word, isJoin):
        if self.kind == 'uniform':
            return self.known_edits1_uniform(word, isJoin)
        else:
            return self.known_edits1_empirical(word, isJoin)
    
    def known_edits2(self, word, isJoin):
        if self.kind == 'uniform':
            return self.known_edits2_uniform(word, isJoin)
        else:
            return self.known_edits2_empirical(word, isJoin)  
    
    def edits1(self,word):
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        #Small caveat in deletes and inserts, at the beginning of the word is simply ignored
        deletes    = [a + b[1:] for a, b in splits if b and a and self.get_e_prob((self.ins, a[-1]+b[0])) > self.threshold]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1 and self.get_e_prob((self.trs, b[1]+b[0])) > self.threshold]
        replaces   = [a + c + b[1:] for a, b in splits for c in self.alphabet if b and self.get_e_prob((self.sub, b[0]+c)) > self.threshold]
        inserts    = [a + c + b     for a, b in splits for c in self.alphabet if a and self.get_e_prob((self.dl, a[-1]+c)) > self.threshold]
        return set(deletes + transposes + replaces + inserts)

    def edits2(self,word):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))
    
    def known_edits2_uniform(self,word, isJoin):
        return set((e2,self.P*self.P,isJoin) for e1 in self.edits1(word) for e2 in self.edits1(e1) if self.languagemodel.known(e2))

    def known_edits1_uniform(self,word, isJoin):
        return set((e1,self.P,isJoin) for e1 in self.edits1(word) if self.languagemodel.known(e1))

    def known_edits1_join(self,word):
        return set((e1,self.P,True) for e1 in self.edits1(word) if self.languagemodel.known(e1))
    
    
    #Methods for empirical edit model
    def known_edits1_empirical(self,word, isJoin):
        return set((e1,self.get_edit_prob( word, e1 ),isJoin) for e1 in self.edits1(word) if self.languagemodel.known(e1))
    
    def known_edits2_empirical(self,word, isJoin):
        return set((e2,self.get_edit_prob( word, e2 ),isJoin) for e1 in self.edits1(word) for e2 in self.edits1(e1) if self.languagemodel.known(e2))

    def get_edit_prob(self,word, correct_word):
        [ ed, edts ] = self.get_edits(correct_word, word)
        return self.get_edit_prob_from_edits(edts)
    
    def get_edit_prob_from_edits(self,edits):
        ep = 1
        for edit in edits:
            if edit[0] != self.nc:
                if edit[0] == self.trs:
                    if edit[1][0] != edit[1][1]:
                        ep *= self.get_e_prob(edit)
                else:
                    ep *= self.get_e_prob(edit)
        if ep == 1:
            return 1 - self.P
        else:
            return ep
        
    #For an unknown edit operation, we use 1/(V + 1 + respective_uni/bigram count) 
    def get_e_prob(self,edit):
        if ( edit[0], edit[1].strip() ) in self.edit_prob:
            return self.edit_prob[( edit[0], edit[1].strip() )]
        else:
            if edit[0] == self.dl or edit[0] == self.trs:
                return 1.0 / ( 1 + len(self.char_unigram_count) + self.char_bigram_count.get(edit[1],0) )
            elif edit[0] == self.ins:
                return 1.0 / ( 1 + len(self.char_unigram_count) + self.char_unigram_count.get(edit[1][0],0) )
            else:
                return 1.0 / ( 1 + len(self.char_unigram_count) + self.char_unigram_count.get(edit[1][1],0) )
    
    def get_edits(self,str1, str2):
        str1 = '$' +str1 + '$'
        str2 = '$'+ str2 + '$'   
       
        d = [[]] * (len(str1))
        chg = [[]] * (len(str1))
        
        
        for i in range(0, len(d)):
            d[i] = [0] * (len(str2))
            chg[i] = [(self.nc, '')] * (len(str2))
            
        cost = 0
        d[0][0] = 0
        for i in range(1, len(str1)):
            d[i][0] = i
            chg[i][0] = (self.dl, str1[i-1] + str1[i])
            
        for j in range(1, len(str2)):
            d[0][j] = j
            chg[0][j] = (self.ins, str1[min(j-1, len(str1)-1)] + str2[j])
        
        for i in range(1, len(str1)):
            for j in range(1, len(str2)):
                if str1[i] == str2[j]:
                    cost = 0
                else:
                    cost = 1
                    
                mn = min([d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost])
                d[i][j] = mn
                if mn == d[i - 1][j] + 1:
                    chg[i][j] = (self.dl, str1[i-1] + str1[i])
                elif mn == d[i][j - 1] + 1:
                    chg[i][j] = (self.ins, str1[i] + str2[j])
                elif cost > 0:
                    chg[i][j] = (self.sub, str1[i] + str2[j])
                else:
                    chg[i][j] = (self.nc, '')
                
                if i > 1 and j > 1 and str1[i] == str2[j - 1] and str1[i - 1] == str2[j] and str2[j] != str2[j-1]:
                    mn = min([ d[i][j], d[i - 2][j - 2] + cost])
                    d[i][j] = mn
                    if mn == d[i - 2][j - 2] + cost:
                        chg[i][j] = (self.trs, str1[i-1] + str1[i])
                    
#        s = '\t'.join( [a for a in str2] )
#        print '\t'+s
#        for i in range(0, len(chg)):
#            str = str1[i] + '\t'
#            for j in range(0, len(chg[i])):
#                str = str +'%d %d %s\t' % (d[i][j], chg[i][j][0], chg[i][j][1])
#            print str
                                     
        i = len(str1)-1
        j = len(str2)-1
        changes = [chg[i][j]]
        while i >= 1 and j >= 1:
        
            mn = min([d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost])
            ni = i 
            nj = j
            d[i][j] = mn
            if mn == d[i - 1][j] + 1:
                ni = i - 1
            elif mn == d[i][j - 1] + 1:
                nj = j - 1
            else:
                ni = i - 1
                nj = j - 1
                
            if i > 1 and j > 1 and str1[i] == str2[j - 1] and str1[i-1] == str2[j]:
                mn = min([ d[i][j], d[i - 2][j - 2] + cost])
                if mn == d[i][j]:
                    ni = i-1
                    nj = j-1
                else:
                    ni = i - 2
                    nj = j - 2
            i = ni
            j = nj
            changes.append(chg[i][j])
        
        changes.reverse()
        return [d[len(str1)-1][len(str2)-1], changes]

