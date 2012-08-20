
from __future__ import print_function

from cPickle import Unpickler
import sys


class MessageIterator(object):

  def __init__(self, inp_filename):
    self.filename = inp_filename
    with open(self.filename, 'rb') as inpfile:
      reader = Unpickler(inpfile)
      self.numgroups = reader.load()
      self.tot_msgs = reader.load()
      self.num_msgs = reader.load()

  def __iter__(self):
    with open(self.filename, 'rb') as inpfile:
      reader = Unpickler(inpfile)
      [reader.load() for i in xrange(3)]
      for i in xrange(self.tot_msgs):
        yield reader.load()


def main():
  if len(sys.argv) != 2:
    print('Usage: python {0} <input_file>'.format(__file__), file=sys.stderr)
    sys.exit(-1)
  mi = MessageIterator(sys.argv[1])

  for mf in mi:
    print("{0} ({1})".format(mf.filename,mf.newsgroupnum))
    print("Subject:")
    for subj,count in mf.subject.items():
      print("Count for "+subj+" is "+str(count))
    for word,count in mf.body.items():
      print("Count for "+word+" is "+str(count))

if __name__ == '__main__':
  main()

