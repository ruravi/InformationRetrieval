#!/bin/sh

# We will call your code using this script.
# This will get called as
# runNaiveBayes.sh <mode>
# where mode specifies which part of the assignment you should run.

# When we test your code, we will first call 
# ./setup.sh <ourNewTrainDir>
# which should build your code and spit out train.gz
# if your code needs them.
#
# Then, to test the different parts of the assignment, we will call
# ./runNaiveBayes.sh binomial
# ./runNaiveBayes.sh binomial-chi2
# ./runNaiveBayes.sh multinomial
# ./runNaiveBayes.sh twcnb
#
# (you should test your code the same way)

python naive_bayes_classifier.py $1 out.pk

