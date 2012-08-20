#!/bin/env python
import sys
from collections import deque
from array import array
import math

testCases1 = [
  # linguistics
  [207, 208],
  # the
  [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 17, 19, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 89, 90, 91, 92, 93, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 122, 123, 124, 125, 126, 127, 129, 130, 131, 132, 134, 135, 137, 138, 140, 141, 142, 143, 145, 146, 147, 148, 149, 150, 151, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 168, 169, 170, 173, 174, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 195, 196, 197, 198, 199, 201, 202, 203, 204, 205, 207, 208, 209, 210, 211, 212, 214, 215, 216, 217, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 231, 232, 234, 235, 236, 237, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 250, 251, 252, 253, 254, 255, 256, 257, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 283, 285, 286, 287, 289, 290, 291, 292, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 306, 307, 308, 309, 310, 311, 312, 313, 316, 317, 318, 319, 320, 321, 322, 324, 325, 326, 327, 328, 329, 330, 331, 332, 334, 335, 336, 337, 338, 340, 341, 342, 343, 344, 345, 346, 348, 349, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 399, 400, 402, 403, 404, 405, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 443, 444, 445, 446, 447, 449, 450, 451, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 466, 467, 468, 469, 470, 471, 472, 474, 475, 477,
 478, 479, 480, 481, 483, 484, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 567, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 586, 587, 588, 589, 590, 591, 592, 594, 595, 596, 597, 598, 599, 600, 601, 602, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 620, 621, 622, 623, 624, 625, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 655, 656, 657, 658, 659, 660, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 702, 703, 704, 705, 706, 709, 710, 711, 712, 713, 714, 715, 716, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 729, 730, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 746, 747, 748, 750, 751, 752, 754, 755, 756, 758, 759, 760, 762, 763, 764, 765, 767, 768, 769, 770, 771, 772, 773, 774, 776, 777, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842, 843, 844, 845, 846, 847, 848, 849, 850, 852, 853, 854, 855, 856, 857, 859, 860, 861, 862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 886, 887, 888, 889, 890, 891, 892, 893, 895, 896, 897, 898, 899, 900, 901, 902, 903, 905, 906, 907, 908, 909, 912, 913, 914,
 915, 916, 917, 918, 919, 921, 923, 925, 926, 927, 928, 929, 930, 932, 933, 934, 935, 936, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 950, 952, 953, 954, 955, 956, 958, 959, 960, 961, 962, 963, 965, 966, 967, 968, 969, 970, 971, 972, 973, 974, 976, 977, 978, 979, 980, 981, 982, 983, 984, 985, 986, 987, 988, 989, 990, 991, 992, 993, 995, 996, 997, 998, 999, 1000],
  # faculty
[3, 4, 9, 16, 19, 24, 25, 27, 28, 30, 31, 32, 33, 35, 36, 43, 46, 47, 52, 55, 57, 60, 61, 62, 64, 65, 66, 77, 78, 80, 83, 86, 91, 98, 99, 100, 101, 102, 103, 104, 106, 108, 112, 113, 116, 117, 119, 120, 127, 141, 147, 151, 156, 158, 168, 170, 172, 175, 179, 182, 184, 185, 187, 195, 197, 199, 202, 206, 207, 208, 209, 210, 213, 221, 225, 227, 228, 233, 238, 249, 252, 255, 256, 266, 267, 268, 270, 271, 273, 274, 281, 284, 285, 289, 290, 292, 294, 299, 301, 302, 303, 306, 308, 312, 320, 321, 322, 325, 326, 328, 329, 332, 334, 335, 337, 341, 342, 344, 345, 347, 349, 356, 357, 358, 360, 364, 376, 377, 379, 382, 383, 385, 395, 397, 403, 404, 405, 406, 410, 412, 417, 418, 423, 430, 431, 432, 433, 434, 437, 440, 441, 445, 446, 452, 453, 454, 461, 464, 466, 469, 477, 480, 486, 487, 488, 495, 496, 506, 507, 511, 512, 517, 518, 520, 522, 524, 526, 532, 535, 540, 543, 549, 550, 558, 562, 563, 564, 571, 574, 581, 586, 587, 592, 597, 598, 604, 607, 608, 615, 620, 621, 622, 625, 633, 634, 635, 636, 639, 640, 642, 653, 654, 656, 658, 660, 668, 671, 676, 680, 681, 683, 686, 687, 689, 694, 697, 702, 703, 708, 710, 711, 714, 722, 723, 729, 730, 737, 739, 742, 746, 747, 750, 756, 757, 758, 759, 764, 765, 766, 769, 770, 772, 777, 780, 782, 783, 784, 791, 795, 798, 801, 807, 812, 815, 816, 822, 823, 824, 825, 828, 830, 833, 835, 836, 837, 841, 852, 854, 863, 864, 865, 868, 870, 873, 880, 882, 884, 887, 888, 889, 897, 902, 906, 912, 914, 918, 922, 924, 925, 928, 929, 932, 933, 934, 938, 939, 941, 943, 944, 947, 948, 952, 955, 961, 962, 963, 968, 971, 973, 975, 979, 980, 983, 984, 987, 989, 993, 995, 996, 999],
  # student
  [3, 8, 16, 19, 23, 29, 31, 40, 47, 52, 57, 61, 83, 86, 87, 100, 101, 103, 110, 113, 117, 119, 125, 127, 145, 148, 154, 156, 159, 182, 185, 202, 208, 228, 231, 233, 240, 244, 248, 255, 264, 271, 278, 283, 289, 297, 303, 306, 307, 308, 312, 323, 325, 332, 335, 337, 341, 344, 356, 357, 379, 402, 430, 435, 437, 441, 453, 457, 461, 462, 463, 466, 480, 486, 487, 502, 507, 511, 520, 532, 535, 542, 548, 550, 551, 552, 557, 559, 584, 589, 592, 604, 605, 619, 621, 625, 629, 635, 640, 648, 653, 658, 663, 668, 670, 686, 702, 709, 719, 722, 729, 747, 750, 751, 759, 769, 770, 782, 785, 788, 796, 798, 807, 811, 813, 815, 822, 824, 825, 828, 840, 849, 857, 860, 880, 882, 889, 906, 918, 922, 925, 932, 933, 934, 938, 939, 941, 942, 946, 947, 955, 962, 963, 967, 968, 971, 978, 979, 983, 984, 989, 996],
  # biology
  [9, 80, 116, 124, 137, 146, 170, 182, 197, 209, 212, 213, 237, 245, 250, 256, 290, 303, 307, 311, 321, 333, 338, 358, 364, 377, 463, 486, 496, 512, 524, 550, 558, 572, 581, 586, 588, 615, 622, 654, 665, 675, 683, 711, 714, 758, 791, 795, 798, 812, 840, 875, 901, 907, 937, 938, 943, 950, 979, 980, 981, 995],
  # advanced
  [27, 46, 55, 62, 99, 117, 122, 127, 130, 159, 212, 225, 236, 255, 256, 335, 341, 357, 413, 437, 446, 466, 510, 535, 550, 622, 664, 666, 680, 745, 792, 798, 826, 845, 866, 874, 888, 947, 980],
  # anthropology
  [324, 335, 418, 466, 505, 686],
  # classics
  [19, 190, 435, 519, 590],
  
]

testCases = [[9,15,18,77,84]]


# -----------------------------
def jeff_encode_num(n):
    bytesa = deque(array('B'))
    times =0
    while True:
        times += 1
        bytesa.appendleft(n % 64)
        if n < 64:
            break
        n = n /64
    bytesa[0] += times << 6
    return bytesa

class bitarray:
    def __init__(self):
        self.data = array('B')
        self.s = -1
        
    def createFromString( self, str ):
        self.data = array('B')
        for s1 in str:
            self.data.append( s1 )
        self.s = len( self.data )*8 -1
        
        
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
                self.__setitem__( self.s, b )
    
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
        #Count the number of ones
        if bitArr[i] == 1:
            ones += 1
        if bitArr[i] == 0:
            #"done with ones", p is the 2^(length of string-1)  
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
    
def gamma_compress( postings_list ):
    pl = []
    prev = 0
    #First get the delta values for the postings list
    #for n in postings_list:
    #    pl.append( n - prev )
    #    prev = n
    print encodeNumbers(postings_list)
    return encodeNumbers(postings_list)

def gamma_decode( string ):
    br = bitarray()
    br.createFromString( string )
    pl = decodeGamma(br)
    #postings_list = []
    #postings_list.append(pl[0])
    #if len(pl) > 1:
    #    for i in range( 1, len(pl) ):
    #        postings_list.append( pl[i] + postings_list[i-1] )
    return pl

        


def vb_encode_num(n):
    bytesa = deque(array('B'))
    while True:
        bytesa.appendleft(n % 128)
        if n < 128:
            break
        n = n/128
    bytesa[-1] += 128
    return bytesa


def vb_encode(arr):
  bytestream = []
  for n in arr:
      bytesa = vb_encode_num(n)
      bytestream.extend(bytesa)
  return bytestream

def vb_decode(bytesa):
  numbers = []
  n = 0
  for byte in bytesa:
      if byte < 128:
          n = (128*n) + byte
      else:
          n = (128*n) + (byte-128)
          numbers.append(n)
          n=0
  return numbers


# -------------------------------------

def null_encode_num(num):
  bytes = deque(array('B'))
  byte1 = num & 0xFF;
  byte2 = (num & 0xFF00) >> 8;
  byte3 = (num & 0xFF0000) >> 16;
  byte4 = (num & 0xFF000000) >> 24;
  bytes.append(byte4)
  bytes.append(byte3)
  bytes.append(byte2)
  bytes.append(byte1)
  return bytes

def null_encode(arr):
  bytestream = []
  for n in arr:
    bytes = null_encode_num(n)
    bytestream.extend(bytes)
  return bytestream

def null_decode(bytes):
  numbers = []
  n = 0
  i = 0
  for b in bytes:
    n = (n << 8) + b
    i = i + 1
    if i == 4:
      numbers.append(n)
      i = 0
      n = 0
  return numbers

# ----------------------------------

# Convert from an array of docIDs to an array of docDeltas (starting from zero)
def to_gaps(arr):
    docDeltas = []
    prev = 0
    for n in arr:
        docDeltas.append(n-prev)
        prev = n
    return docDeltas


# Convert from an array of docDeltas to an array of docIDs
def from_gaps(arr):
    docIDs = []
    prev = 0
    for n in arr:
        docIDs.append(n+prev)
        prev += n
    return docIDs

# -----------------------------------

# main method
method = "vb"
if len(sys.argv) > 1:
  method = sys.argv[1];
total = 0

for i in range(0, len(testCases)):
  # encode
  gaps = to_gaps(testCases[i])
  if method == "null":
    bytes = null_encode(gaps)
  elif method == "vb":
    #vb encoding
    bytes = gamma_compress(gaps)
    
  # Your encoded form must be in the variable bytes
  # decode
  if method == "null":
    decoded_gaps = null_decode(bytes)
  elif method == "vb":
    #vb decoding
    decoded_gaps = gamma_decode(bytes)
  decoded = from_gaps(decoded_gaps)

  # check and maintain length statistics
  status = "passed"
  if decoded != testCases[i]:
    status = "FAILED"
  length = len(bytes)
  print >> sys.stderr, 'test case %d: status is %s; bytes to encode postings %d' % (i+1, status, length)
  if status != "passed":
    print 'test case input is %s' % str(testCases[i])
    print 'output decoded is  %s' % str(decoded);
  print 
  total = total + length

print 'total length of encoded postings: %d bytes' % total
