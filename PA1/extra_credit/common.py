from array import array
import math
from collections import deque

class bitarray:
	def __init__(self):
		self.data = array('B')
		self.s = -1
		
	def createFromString( self, str ):
		self.data = array('B')
		for s1 in str:
			self.data.append( ord(s1) )
		self.s = len( self.data )*8 - 1
		
		
	def getByteNum( self, index ):
		return index/8
	
	def getBitMask(self, index):
		ri = index % 8
		shift = (8-ri) - 1
		return 1<<shift
		
	def __getitem__( self, index ):
		if self.data[self.getByteNum( index )] & self.getBitMask(index) > 0:
			return 1
		else:
			return 0
	
	def __setitem__( self, index, val ):
		self.s = max(self.s, index)
		bi = self.getByteNum(index)
		while bi >= len( self.data ):
			self.data.append(0)
		if val > 0:
			self.data[ self.getByteNum(index) ] = self.data[ self.getByteNum(index) ] | self.getBitMask(index)
		else:
			self.data[ self.getByteNum(index) ] = self.data[ self.getByteNum(index) ] & ~self.getBitMask(index)
			
	def append(self, val):
		self.s +=1
		self.__setitem__( self.s, val )
		
	def appendMany(self, val, count):
		for i in range(0, count):
			self.append(val)
			
	def appendNumberMinusFirstOne(self, n):
		shift = len(bin(n)) - 4
		if shift >= 0:
			mask = 1 << shift
			for i in range(0, shift+1):
				if n & mask > 0:
					self.append( 1 )
				else:
					self.append( 0 )
				mask = mask >> 1
	
	
	def appendBitsFromString( self, bits ):
		if len(bits) > 0:
			self.s += 1
			for bit in bits:
				if bit == '0':
					b = 0
				else:
					b = 1
				self.__setitem__( s, b )
	
	def getByteArray( self ):
		valid = self.s+1
		if valid%8 == 0:
			return self.data
		else:
			mask = '0'*(valid%8) + '1'*(8 - valid%8)
			self.data[-1] = self.data[-1] | int(mask,2)
			return self.data
		
	def printAsBin( self ):
		d = self.getByteArray()
		for bt in d:
			print bin( bt )
		
		

#Gamma Encoding
def encodeNumber( bitArr, n ):
	bl = len(bin( n )) - 2
	bitArr.appendMany( 1, bl-1 )
	bitArr.append(0)
	bitArr.appendNumberMinusFirstOne( n )
	
def decodeGamma( bitArr ):
	nums = []
	ones = 0
	p = 0
	i = 0
	while i <= bitArr.s:
		if bitArr[i] == 1:
			ones += 1
		elif bitArr[i] == 0:  
			p = math.pow(2, ones)
			n = 0
			for j in range(0, ones):
				n *= 2
				n += bitArr[i+1+j]	
			n += p
			i += (ones)
			ones = 0
			nums.append(int(n))
		i+=1
	return nums

def encodeNumbers( numbers ):
	br = bitarray()
	for n in numbers:
		encodeNumber( br, n )
	return br.getByteArray()
	
def compress( postings_list ):
	pl = []
	prev = 0
	#First get the delta values for the postings list
	for n in postings_list:
		pl.append( n - prev )
		prev = n
	return encodeNumbers(pl)

def decode( str ):
	br = bitarray()
	br.createFromString( str )
	pl = decodeGamma(br)
	postings_list = []
	postings_list.append(pl[0])
	if len(pl) > 1:
		for i in range( 1, len(pl) ):
			postings_list.append( pl[i] + postings_list[i-1] )
	return postings_list

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
def writePostingsList( dictFile, postingsFile, termId, postings, numPostings ):
	b = arrayToBytes([ termId, postingsFile.tell(), len(postings), numPostings ])
	dictFile.write( b )
	postingsFile.write( postings )
	
#Returns a line[termID, Filepos, length of postings] from the .dict file
def getPostingHeader( dictFile ):
	dEntry = dictFile.read(16)
	if len(dEntry) == 0 :
		return None
	dEntry = bytesToArr(dEntry)
	return dEntry

def getNextPostingsList( dictFile, postingsFile ):
	dEntry = dictFile.read(16)
	if len(dEntry) == 0 :
		return None
	#dEntry contains [termID, Filepos, lenofpostings, docfreq]
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