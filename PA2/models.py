
import sys
import os.path
import gzip
import itertools
import marshal
from glob import iglob
from collections import Counter
from EditModel import EditModel

char_counts = Counter()
char_bigram_counts = Counter()


def scan_corpus(training_corpus_loc):
    """
    Scans through the training corpus and counts unigrams and bigrams
    """
    unigram_count = Counter()
    bigram_count = Counter()
    for block_fname in iglob( os.path.join( training_corpus_loc, '*.gz' ) ):
        print >> sys.stderr, 'processing dir: ' + block_fname
        with gzip.open( block_fname ) as fin:
            words = fin.read().lower().split()
            bigrams = itertools.izip(words[:-1],words[1:])
            unigram_count.update(words)
            bigram_count.update(bigrams)
    # Go from counts to probabilities. DIvide bigram count by unigram count of first word
    #Smooth bigrams
    V = float(len(unigram_count))
    print >> sys.stderr, "Processing bigrams"
    for each in bigram_count:
        bigram_count[each] = (bigram_count[each] + 1) / (V + unigram_count[each[0]])
    # Divide unigram counts by total number of words
    N = float( sum( unigram_count.values() ) )
    print >> sys.stderr, "Processing Unigrams"
    for each in unigram_count:
        unigram_count[each] /= N
    print >> sys.stderr, "Writing to file - unigram model"
    serialize_data(dict(unigram_count), 'unigram_model')
    print >> sys.stderr, "Writing to file - bigram model"
    serialize_data(dict(bigram_count), 'bigram_model')
    print >> sys.stderr, "Done!"

def read_edit1s(edit1s_loc):
    """
    Returns the edit1s data
    It's a list of tuples, structured as [ .. , (misspelled query, correct query), .. ]
    """
    with gzip.open(edit1s_loc) as f:
        # the .rstrip() is needed to remove the \n that is stupidly included in the line
        edit1s = [ line.rstrip().split('\t') for line in f if line.rstrip() ]
    return edit1s

def count_chars(w):
    word = '$' +w+ '$'
    char_counts.update(list(w))
    char_bigrams = []
    for each in itertools.izip(word,word[1:]):
        char_bigrams.append(''.join(each))
    char_bigram_counts.update(char_bigrams)

def get_char_bigram_count(chs):
    return char_bigram_counts.get(chs, 0);

def get_char_unigram_count(ch):
    return char_counts.get(ch, 0);

def scan_edits( edits_file ):
    
    print >> sys.stderr, "Processing "+edits_file
    editmodel = EditModel('')
    edit_probs = Counter()
    edits1 = read_edit1s(edits_file)
    print >> sys.stderr, "Counting"
    for error,correct in edits1:
        count_chars(correct)
        v, edit_types = editmodel.get_edits( correct, error )
        edit_types = set(edit_types)
        edit_types = [each for each in edit_types if each[0] != editmodel.nc]
        edit_probs.update(edit_types)
    num_char_unigrams = len(char_counts)
    print >> sys.stderr, "Normalizing"
    norm_edit_probs = {}
    for kind,str in edit_probs.keys():
        if kind == editmodel.dl:
            norm_edit_probs[(kind,str)] = (edit_probs[(kind,str)] + 1.0)/(get_char_bigram_count(str) + num_char_unigrams + 1)
        elif kind == editmodel.ins:
            norm_edit_probs[(kind,str)] = (edit_probs[(kind,str)] + 1.0)/(get_char_unigram_count(str[0]) + num_char_unigrams + 1)
        elif kind == editmodel.sub:
            #If this is a substitution, reverse the characters because of bug in get_edits
            norm_edit_probs[(kind,str[::-1])] = (edit_probs[(kind,str)] + 1.0)/(get_char_unigram_count(str[0]) + num_char_unigrams + 1)
        elif kind == editmodel.trs:
            norm_edit_probs[(kind,str)] = (edit_probs[(kind,str)] + 1.0)/(get_char_bigram_count(str) + num_char_unigrams + 1)
    print >> sys.stderr, "Writing to file - edits_model"
    serialize_data(norm_edit_probs, 'edit_model')
    serialize_data(dict(char_counts), 'char_unigram_model')
    serialize_data(dict(char_bigram_counts), 'char_bigram_model')


def serialize_data(data, fname):
  """
  Writes `data` to a file named `fname`
  """
  with open(fname, 'wb') as f:
    marshal.dump(data, f)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Usage: python corrector.py <training corpus dir> <training edit1s file>"
        exit(1)
    scan_edits(sys.argv[2])
    scan_corpus(sys.argv[1])
