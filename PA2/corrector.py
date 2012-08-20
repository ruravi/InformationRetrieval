
import sys
import marshal
import math
from collections import defaultdict
from LanguageModel import LanguageModel
from Candidates import Candidates
from EditModel import EditModel


gold_loc = 'data/gold.txt'
google_loc = 'data/google.txt'

def read_query_data(queries_loc):
  """
  all three files match with corresponding queries on each line
  """
  queries = []
  gold = []
  google = []
  with open(queries_loc) as f:
    for line in f:
      queries.append(line.rstrip())
  with open(gold_loc) as f:
    for line in f:
      gold.append(line.rstrip())
  with open(google_loc) as f:
    for line in f:
      google.append(line.rstrip())
  #assert( len(queries) == len(gold) and len(gold) == len(google) )
  return (queries, gold, google)

class SpellCorrect():
    
    def __init__(self, lm, em):
        self.languagemodel = lm
        self.editmodel = em
        
    def spell_correct_query(self, query):
        possibilities = []
        eachline = query.strip().split()
        #first word will be left out
        cand_generator = Candidates(self.languagemodel, self.editmodel)
        candidates = cand_generator.generate_candidates("",eachline[0])
        possibilities.append(candidates)
        for prevword, eachword in zip(eachline, eachline[1:]):
            candidates = cand_generator.generate_candidates(prevword, eachword)
            possibilities.append(candidates)
        solutions = defaultdict(tuple)
        answer =  self.rank_highest(possibilities[::-1], solutions)
        return ' '.join(answer[0].split()[::-1])
    
    #Sequence is list of sets [ set[(candidates1,prob, IsJoin),(candidate,prob, isJoin)...]  set[(candidates2,prob,isJoin)..] [...] ]
    def rank_highest(self, sequence, solutions):
        #Base Cases
        #There's only one word
        if len(sequence) == 1:
            #There are candidates
            if len(sequence[0]) != 0:
                return languagemodel.unigram_max(sequence[0])
            else:
                #There are no candidates !
                return "",1
        #Empty string
        elif len(sequence) == 0:
            #This can happen when a join occurs at the last two words, thus making sequence[2:] be nothing
            return "",1
        # Recursive step
        else:
            max = float('-inf')
            #There are no candidates!, skip to next word
            if len(sequence[0]) == 0:
                seq_of_rest, score_of_rest  = self.rank_highest(sequence[1:], solutions)
                return ''.join(seq_of_rest), score_of_rest
            for eachword,error_prob,isJoin in sequence[0]:
                #Possible speed improvement here, a map of sequences and the solution pair (result,score)
                if isJoin and solutions.has_key(len(sequence[2:])):
                    seq_of_rest, score_of_rest  = solutions[len(sequence[2:])]
                elif isJoin and not solutions.has_key(len(sequence[2:])):
                    seq_of_rest, score_of_rest  = self.rank_highest(sequence[2:], solutions)
                    solutions[len(sequence[2:])] = (seq_of_rest, score_of_rest)
                elif solutions.has_key(len(sequence[1:])):
                    seq_of_rest, score_of_rest  = solutions[len(sequence[1:])]
                else:
                    seq_of_rest, score_of_rest  = self.rank_highest(sequence[1:], solutions)
                    solutions[len(sequence[1:])] = (seq_of_rest, score_of_rest)
                #score is the language model probability + Error model probability
                if seq_of_rest is not "":
                    nextword = seq_of_rest.split()[0] 
                else:
                    nextword = ""
                score = languagemodel.add_up_scores(eachword, nextword, error_prob, score_of_rest)
                if score > max:
                    max = score
                    if type(eachword) is tuple:
                        result = eachword[1] + ' ' + eachword[0] + ' ' + ''.join(seq_of_rest) 
                    else:
                        result = eachword  + ' ' + ''.join(seq_of_rest) 
            return result, max



if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage: python corrector.py <dev | test> <uniform | empirical> <queries file>"
        exit(0)
    queries_file = sys.argv[3]
    queries, gold, google = read_query_data(queries_file)
    kind_of_editmodel = sys.argv[2]
    #Read in unigram and bigram probs
    print >> sys.stderr, "Loading language model"
    languagemodel = LanguageModel('unigram_model','bigram_model')
    print >> sys.stderr, "Loading edit model"
    editmodel = EditModel(kind_of_editmodel,languagemodel)
    languagemodel.init_edit_model(editmodel)
    print >> sys.stderr,"Loading spell correct"
    spell_corrector = SpellCorrect(languagemodel, editmodel)
    answers = []
    qc = 0
    for eachquery in queries:
        answer = spell_corrector.spell_correct_query(eachquery)  
        print answer  
        print >> sys.stderr, "%d" % (qc)
        qc+=1
        answers.append(answer)
    #Accuracy evaluation
    wrong = 0
    correct = 0
    for i in range(len(answers)):
        if answers[i] != gold[i]:
            wrong += 1
        else:
            correct += 1
    print >> sys.stderr, "accuracy = " + str(float(correct)/len(answers))
    