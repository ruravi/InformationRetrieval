from array import array
from collections import deque

#No Encoding
def encodeNumber( n ):
	return n

def encodeNumbers( numbers ):
	return numbers
	
def compress( postings_list ):
	return arrayToBytes(postings_list)

def decode( bytearray ):
	return bytesToArr(bytearray)
	
def arrayToBytes( arr ):
	barr = array('B')
	#Write each number as 4 bytes
	numberSoFar = deque(array('B'))
	for n in arr:
		for index in range(0, 4):
			numberSoFar.appendleft( n & 0xFF )
			n = n / 256
		barr.extend(numberSoFar)
		numberSoFar = deque(array('B'))
	return barr
	
def bytesToArr( barr ):
	arr = []
	numberSoFar = 0
	i = 0
	#Read in 4 bytes at a time and add them up to get one number
	for b in barr:
		numberSoFar = numberSoFar + ord(b)
		i = i + 1
		if i == 4:
			i = 0
			arr.append(numberSoFar)
			numberSoFar = 0
		else:
			numberSoFar = numberSoFar * 256
	return arr

#postings is a byte array
def writePostingsList( dictFile, postingsFile, termId, postings, numPostings  ):
	b = arrayToBytes([ termId, postingsFile.tell(), len(postings) , numPostings] )
	dictFile.write( b )
	postingsFile.write( postings )
	
#Returns a line[termID, Filepos, length of postings] from the .dict file
def getPostingHeader( dictFile ):
	dEntry = dictFile.read(16)
	if len(dEntry) == 0 :
		return None
	dEntry = bytesToArr(dEntry)
	return dEntry

# returns a tuple[ termID, [postings list] ], where postings list is decoded and in integer format
def getNextPostingsList( dictFile, postingsFile ):
	dEntry = dictFile.read(16)
	if len(dEntry) == 0 :
		return None
	#dEntry contains [termID, Filepos, lenofpostings]
	dEntry = bytesToArr(dEntry)
	postingsFile.seek(dEntry[1])
	#posting is a string
	posting = postingsFile.read( dEntry[2] )
	posting = decode(posting)
	return [ dEntry[0], posting ]

def mergePostings( pos1, pos2 ):
	pos = []
	i = 0
	j = 0
	while i < len(pos1) and j < len(pos2):
		if pos1[i] < pos2[j]:
			pos.append(pos1[i])
			i = i + 1
		elif pos2[j] < pos1[i]:
			pos.append(pos2[j])
			j = j + 1
		else:
			print 'Shouldnt happen, since postings are from different blocks'
			pos.append(pos2[j])
			j = j + 1
			i = i + 1
	while i < len(pos1):
		pos.append( pos1[i] )
		i = i + 1
	while j < len(pos2):
		pos.append( pos2[j] )
		j = j + 1			
	return pos

def mergeAndWritePostings( dictFile, postingsFile, termId1, pos1, pos2 ):
	mergedPos = mergePostings( pos1, pos2 )
	numPostings = len(mergedPos)
	writePostingsList(dictFile, postingsFile, termId1, compress(mergedPos), numPostings)