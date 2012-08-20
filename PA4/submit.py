
import urllib
import urllib2
import hashlib
import random
import email
import email.message
import email.encoders
import StringIO
import sys
import json
import subprocess
import getpass
from tempfile import NamedTemporaryFile
from time import time
from subprocess import Popen
from subprocess import PIPE

class NullDevice:
  def write(self, s):
    pass

def submit(partId):
    
  print '==\n== [inforetrieval] Submitting Solutions | Programming Exercise %s\n=='% homework_id()
  if(not partId):
    partId = promptPart()

  partNames = validParts()
  if not isValidPartId(partId):
    print '!! Invalid homework part selected.'
    print '!! Expected an integer from 1 to %d.' % (len(partNames) + 1)
    print '!! Submission Cancelled'
    return

  (login, password) = loginPrompt()
  if not login:
    print '!! Submission Cancelled'
    return

  print '\n== Connecting to coursera ... '

  # Setup submit list
  if partId == len(partNames) + 1:
    submitParts = range(1, len(partNames) + 1)
  else:
    submitParts = [partId]

  for partId in submitParts:
    # Get Challenge
    (login, ch, state, ch_aux) = getChallenge(login, partId)
    if((not login) or (not ch) or (not state)):
      # Some error occured, error string in first return element.
      print '\n!! Error: %s\n' % login
      return

    # Get source files
    src = ""

    # Attempt Submission with Challenge
    ch_resp = challengeResponse(login, password, ch)
    (result, string) = submitSolution(login, ch_resp, partId, output(partId, ch_aux), \
                                    src, state, ch_aux)
    print '== [inforetrieval] Submitted Homework %s - Part %d - %s' % \
          (homework_id(), partId, partNames[partId - 1])
    print '== %s' % string.strip()
    if (string.strip() == 'Exception: We could not verify your username / password, please try again. (Note that your password is case-sensitive.)'):
      print '== The password is not your login, but a 10 character alphanumeric string displayed on the top of the Assignments page'


def promptPart():
  """Prompt the user for which part to submit."""
  print('== Select which part(s) to submit for assignment ' + homework_id())
  partNames = validParts()
  for i in range(1, len(partNames)+1):
    print '==   %d) %s' % (i, partNames[i - 1])
  print '==   %d) All of the above \n==\n ' % (len(partNames) + 1)
  selPart = raw_input('Enter your choice [1-{0}]: '.format(len(partNames) + 1))
  partId = int(selPart)
  if not isValidPartId(partId):
    partId = -1
  return partId

def isValidPartId(partId):
  """Returns true if partId references a valid part."""
  partNames = validParts()
  return (partId and (partId >= 1) and (partId <= len(partNames) + 1))


# =========================== LOGIN HELPERS ===========================

def loginPrompt():
  """Prompt the user for login credentials. Returns a tuple (login, password)."""
  (login, password) = basicPrompt()
  return login, password


def basicPrompt():
  """Prompt the user for login credentials. Returns a tuple (login, password)."""
  login = raw_input('Login (Email address): ')
  password = raw_input('Password: ')
  return login, password


def homework_id():
  """Returns the string homework id."""
  return '4'


def getChallenge(email, partId):
  """Gets the challenge salt from the server. Returns (email,ch,state,ch_aux)."""
  url = challenge_url()
  values = {'email_address' : email, 'assignment_part_sid' : "%s-%s" % (homework_id(), partId), 'response_encoding' : 'delim'}
  data = urllib.urlencode(values)
  req = urllib2.Request(url, data)
  response = urllib2.urlopen(req)
  text = response.read().strip()

  # text is of the form email|ch|signature
  splits = text.split('|')
  if(len(splits) != 9):
    print 'Badly formatted challenge response: %s' % text
    return None
  return (splits[2], splits[4], splits[6], splits[8])



def challengeResponse(email, passwd, challenge):
  sha1 = hashlib.sha1()
  sha1.update("".join([challenge, passwd])) # hash the first elements
  digest = sha1.hexdigest()
  strAnswer = ''
  for i in range(0, len(digest)):
    strAnswer = strAnswer + digest[i]
  return strAnswer


def challenge_url():
  """Returns the challenge url."""
  return "https://stanford.coursera.org/inforetrieval/assignment/challenge"
  #return "https://stanford.coursera.org/inforetrieval-staging/assignment/challenge"
  
def submit_url():
  """Returns the submission url."""
  return "https://stanford.coursera.org/inforetrieval/assignment/submit"
  #return "https://stanford.coursera.org/inforetrieval-staging/assignment/submit"
  
def submitSolution(email_address, ch_resp, part, output, source, state, ch_aux):
  """Submits a solution to the server. Returns (result, string)."""
  source_64_msg = email.message.Message()
  source_64_msg.set_payload(source)
  email.encoders.encode_base64(source_64_msg)

  output_64_msg = email.message.Message()
  output_64_msg.set_payload(output)
  email.encoders.encode_base64(output_64_msg)
  values = { 'assignment_part_sid' : ("%s-%s" % (homework_id(), part)), \
             'email_address' : email_address, \
             'submission' : output_64_msg.get_payload(), \
             'submission_aux' : source_64_msg.get_payload(), \
             'challenge_response' : ch_resp, \
             'state' : state \
           }
  url = submit_url()
  inp = raw_input('Do you want to actually submit this (yes|y)?: ') #CHANGELIVE
  inp = inp.strip().lower()
  if inp != 'y' and inp != 'yes':
    print '== Fine, aborting'
    sys.exit(0) #CHANGELIVE
  data = urllib.urlencode(values)
  req = urllib2.Request(url, data)
  response = urllib2.urlopen(req)
  string = response.read().strip()
  # TODO parse string for success / failure
  result = 0
  return result, string

############ BEGIN ASSIGNMENT SPECIFIC CODE ##############

def validParts():
  """Returns a list of valid part names."""
  partNames = ['Deliverable 1: Multivariate (Binomial) Naive Bayes', \
                'Deliverable 2: Chi-square Feature Selection', \
                'Deliverable 3: Multinomial Naive Bayes', \
                'Deliverable 5: Transformed Weight-normalized Complement Naive Bayes' ]
  return partNames

def output(partId, ch_aux):
  """Uses the student code to compute the output for test cases."""
  res = []
  print '== Make sure $dataLocation points to the parsed result from running setup.sh'
  print '== Running your code ...'
  test_file = NamedTemporaryFile(delete=False)
  test_file.write(ch_aux)
  test_file.close()
  dataLocation = 'train.gz' # set it to out.pk if you used python
  
  if partId == 1:
    linesOutput = 400
    print 'Calling ./runNaiveBayes.sh with "binomial" option. This might take a while.'
    start = time()
    child = Popen(['./runNaiveBayes.sh', 'binomial', dataLocation, test_file.name], stdout=PIPE, stderr=PIPE, shell=False);
    (res, err) = child.communicate("")
    elapsed = time() - start
    guesses = res.splitlines()
    print err
    if (len(guesses) != linesOutput):
        print 'Warning. The number of lines in your output (' + str(len(guesses)) + ') is not correct. Please ensure that the output is formatted properly.'
  
  elif partId == 2:
    linesOutput = 420
    print 'Calling ./runNaiveBayes.sh with "binomial-chi2" option. This might take a while.'
    start = time()
    child = Popen(['./runNaiveBayes.sh', 'binomial-chi2', dataLocation, test_file.name], stdout=PIPE, stderr=PIPE, shell=False);
    (res, err) = child.communicate("")
    elapsed = time() - start
    guesses = res.splitlines()
    print err
    if (len(guesses) != linesOutput):
        print 'Warning. The number of lines in your output (' + str(len(guesses)) + ') is not correct. Please ensure that the output is formatted properly.'
  
  elif partId == 3:
    linesOutput = 20
    print 'Calling ./runNaiveBayes.sh with "multinomial" option. This might take a while.'
    start = time()
    child = Popen(['./runNaiveBayes.sh', 'multinomial', dataLocation, test_file.name], stdout=PIPE, stderr=PIPE, shell=False);
    (res, err) = child.communicate("")
    elapsed = time() - start
    guesses = res.splitlines()
    print err
    if (len(guesses) != linesOutput):
        print 'Warning. The number of lines in your output (' + str(len(guesses)) + ') is not correct. Please ensure that the output is formatted properly.'  
  
  elif partId == 4:
    linesOutput = 20
    print 'Calling ./runNaiveBayes.sh with "twcnb" option. This might take a while.'
    start = time()
    child = Popen(['./runNaiveBayes.sh', 'twcnb', dataLocation, test_file.name], stdout=PIPE, stderr=PIPE, shell=False);
    (res, err) = child.communicate("")
    elapsed = time() - start
    guesses = res.splitlines()
    print err
    if (len(guesses) != linesOutput):
        print 'Warning. The number of lines in your output (' + str(len(guesses)) + ') is not correct. Please ensure that the output is formatted properly.'

  else:
    print '[WARNING]\t[output]\tunknown partId: %s' % partId
    sys.exit(1)

  print '== Finished running your code'
  return json.dumps( { 'result': res, 'time': elapsed } )

def test_python_version():
  """docstring for test_python_version"""
  if sys.version_info < (2,6):
    print >> sys.stderr, "Your python version is too old, please use >= 2.6"
    sys.exit(1)

if __name__ == '__main__':
  test_python_version()
  submit(0)
