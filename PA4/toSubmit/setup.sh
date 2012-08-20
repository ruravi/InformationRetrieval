#/bin/sh

# This code will be called when we grade your assignment.
# This code gets called with 1 command line parameters, <traindir>
# which is directory that contains several directories (one for each newsgroup).
# While testing your code, use <traindir> = /afs/ir/data/linguistic-data/TextCat/20Newsgroups/20news-18828

python message_parser.py $1 out.pk

