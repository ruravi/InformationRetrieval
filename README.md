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

How to run - PA2
=================

Spelling Corrector

Usage
======

> Step1: Train the noisy channel model  
\>./buildmodels.sh <training corpus> <training edits file>  
training corpus     -- corpus on which the noisy channel model will be trained for computing N-gram probabilties  
training edits file -- A file containing a word and its misspellings, used for training the edit model probabilities  

> Step2: Test the noisy channel model on sentences/queries with spelling errors  
\>./runcorrector.sh <dev | test> <uniform | emperical> <queries file>  
dev | test          -- really, pass in anything  
uniform | empirical -- Pass in uniform for using a uniform edit model, empirical for a trained edit model
queries file        -- A file containing one query string per line, with possible spelling mistakes

> Reference :  
Uniform edit model  -- An edit model that considers all spelling errors occur with the same probabilty  
Empirical edit model-- An edit model that is trained on a dataset provided in the edits file with buildmodel.sh  
                       This will be used in computing the probabilities for each kind of spelling error  
                       
How to run - PA3
=================

Ranked Information Retrieval based on  
1) Cosine Similarity  
2) BM25 ranking measure  
3) Smallest Window of query terms  
4) Number of in-links to a webpage  

Usage
======

> \>python rank.py task_number queryDocTrainData queryDocTrainRel queryDocTestData
task_number   -- 1 | 2 | 3 | 4
              1 -- Ranking based on cosine similarity
              2 -- Ranking based on BM25 similarity measure
              3 -- Ranking based on Smallest Window signal
              4 -- Ranking based on # in-links for a page
queryDocTrainData -- Use the file with the same name. This contains formatted data for training the model  
                     on a set of queries and a set of relevant results for each query.
queryDocTrainRel -- Use the file with the same name. This containes formatted data for training the model
                    on a set of queries and a set of relevant results for each query.
queryDocTestData -- A file containing a query followed by a set of documents. The program will rank the documents  
                    according to the specified ranking measure specified in task_number
                    
How to run - PA4
=================

Text Classification based on  
1) Binomial Naive Bayes  
2) Binomial Naive Bayes with Chi squared feature selection  
3) Multinomial Naive Bayes  
4) Multinomial Naive Bayes with Chi squared feature selection
5) Transform Weight normalized complementary Naive Bayes
6) Support Vector Machines
7) K fold cross validation performed for tuning parameters for each of the above learning algorithms

Usage:
=======

Detailed Instructions on how to run this assignment are given in PA4.pdf in the PA4 directory



                    