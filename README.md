InformationRetrieval
====================

This repository contains all my programming assignments for CS276 - Information Retrieval and web search

How To Run - PA1
===========

Block Sort Based Indexing, Index compression using a) Variable Byte Encoding b) Gamma Encoding

Usage:
======

Task1: 

> \>python index.py arg1 arg2  
Indexes all files from arg1 into arg2  
arg1 -- directory containing all files to be indexed  
arg2 -- output directory where indexed files will be stored by the program i.e folder where the postings list will be stored

> \>python query.py arg1  
Enter query terms after issuing this command. Searches the built index for relevant files (unranked retrieval)  
arg1 -- directory where the indexed files were written to in the previous step i.e arg2 of step 1 above  

Task2

> \>python index.py arg1 arg2
Indexes all files from arg1 into arg2 with variable byte compression. Notice the reduction in the size of the index
arg1 -- directory containing all files to be indexed  
arg2 -- output directory where indexed files will be stored by the program i.e folder where the postings list will be stored

> \>python query.py arg1  
Enter query terms after issuing this command. Searches the built index for relevant files (unranked retrieval)  
arg1 -- directory where the indexed files were written to in the previous step i.e arg2 of step 1 above  

Task3

> \>python index.py arg1 arg2
Indexes all files from arg1 into arg2 with gamma compression. Notice the even more reduction in index size
arg1 -- directory containing all files to be indexed  
arg2 -- output directory where indexed files will be stored by the program i.e folder where the postings list will be stored

> \>python query.py arg1  
Enter query terms after issuing this command. Searches the built index for relevant files (unranked retrieval)  
arg1 -- directory where the indexed files were written to in the previous step i.e arg2 of step 1 above  
