# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:26:14 2014

@author: francescocorea
"""

"""
This file contains the following functions:

abbreviations(file)
Replace the words of the dictionary found in text by the abbreviations.
Don't forget to remove the file called "word_replace_dic.txt" otherwise
it will append the new results to the old file:
os.remove("word_replace_dic.txt")

best_ngrams(words, top_n, min_freq) -->
Computes best ngrams from an input text

ngramsText(text,n,file1,file2=None) -->
Returns a text where the ngrams read from
an external file are joined as a single token.
n=2 considers only bigrams given in file1
n=3 considers bigrams and trigrams given in file1 and file2 respectively
Returns the text and a file with all the occurrences

ngramsFinder(text,min_freq,num_col,word_len) -->
Writes to a file the ngrams found in an input text.

"""
import logging
import re
import os
import csv
from nltk.collocations import TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures

import gensim
from gensim.parsing.preprocessing import STOPWORDS

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

def abbreviations(text,fname,id=None):

    """
    This function looks for phrases given in a dictionary (file) and replace them by their abbreviations
    in text.
    It returns the modified text and an output file with all the ocurrences
    You need to remove the file called "word_replace_dic.txt" otherwise it will append the results to the old file
    os.remove("word_replace_dic.txt")

    """

    # Open and read input file
    with open(fname, 'Ur') as inputfile:
        dic = list(tuple(rec) for rec in csv.reader(inputfile, delimiter=';'))
    #Open output file
    outfile = open('word_replace_dic.csv', 'a+')

    for i in range(len(dic)):
        if dic[i][1].lower() in text.lower():
            text=re.sub(dic[i][1].lower(),dic[i][0].lower(), text.lower())
            outfile.writelines("{0} ; {1} ; {2}\n".format(id,dic[i][0].lower(),dic[i][1].lower()))
    outfile.close()

    return text


def ngramsText(text,N,file1,file2,id=None):
    """
    This function takes a raw text and joins the trigrams and/or bigrams stored in file1(bigrams)
    and file2(trigrams) using underscores. In this way the tokenizer will consider them a single token.
    The argument n controls if only bigrams are to be found or also trigrams are expected.
    It returns the processed text.
    Remove the file "ngrams_found.csv"

    """
    #Open output file
    outfile = open('ngrams_found.csv', 'a+')

    if N == 3:

        #print "Reading trigrams..."
        with open(file2) as f1:
            trigrams = f1.readlines()
            trigrams=[t.strip('\n') for t in trigrams]
            f1.closed

        for item in trigrams:
            itemst=str(item).lower()
            if itemst in text.lower():
                text=re.sub(itemst,itemst.replace(' ','_'), text.lower())
                outfile.writelines("{0} ; {1} \n".format(id,itemst))

    if N == 2 or N == 3:

        #print "Reading bigrams..."
        with open(file1) as f1:
            bigrams = f1.readlines()
            bigrams=[b.strip('\n') for b in bigrams]
            f1.closed

        for item in bigrams:
            itemst=str(item).lower()
            if N == 3:
                if itemst in text.lower():
                    text=re.sub(itemst,itemst.replace(' ','_'), text.lower())
                    outfile.writelines("{0} ; {1} \n".format(id,itemst))

            elif N == 2:
                if itemst in text.lower():
                    text=re.sub(itemst,itemst.replace(' ','_'), text.lower())
                    outfile.writelines("{0} ; {1} \n".format(id,itemst))


    else:
        print "Please insert the correct argument:\n 2 for bigrams \n 3 for bigrams and trigrams\n"

    outfile.close()

    return text

def ngramsFinder(text,min_freq,num_col,word_len):
    """
     This function takes a text, looks for the best n-grams,
     and returns a new text where the n-grams have been replaced by
     single token joined by '_'. In addition it generates two files with the
     results (bigrams.txt and trigrams.txt)

    """

    # Additional stopwords found in the results
    add_stopwords=['http','https','www','com','href','nbsp','arial','helvetica',
                   'font','verdana','sans','serif','fri','sat','font','bgcolor','ffffff',
                   'tel','fax','aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa']

    # Tokenize the text eliminating non alphanumeric characters, stopwords and also words of length <= 3
    tokens=[word for word in gensim.utils.tokenize(text, lower=True)
                if word not in STOPWORDS and len(word) > word_len if word not in add_stopwords]

    # Find the collocations in our text based on the frequency they appear.
    # Here is where all the magic happens :-)
    bigrams, trigrams=best_ngrams(tokens, top_n=num_col, min_freq=min_freq)

    #  re.sub is a function of the regular expressions library (re) which returns a string obtained
    #  by looking for 'pattern' in 'string' and replace it by 'repl'.
    # re.sub(pattern, repl, string, count=0, flags=0)
    # lambda is used in python to create anonymous functions. The equivalence is:
    # def function(N): return f(N)  -->  lambda N: f(N)

    tmp=re.sub(trigrams, lambda match: match.group(0).replace(u' ', u'_'), text.lower())
    newtext=re.sub(bigrams, lambda match: match.group(0).replace(u' ', u'_'), tmp)

    return newtext

def best_ngrams(words, top_n, min_freq):

    """
    This function has been extracted from an Europython 2014 tutorial about
    topic modelling given by Radim Rehurek and modified for this particular project.

    Extract `top_n` most salient collocations (bigrams and trigrams),
    from a stream of words. Ignore collocations with frequency
    lower than `min_freq`.
    This fnc uses NLTK for the collocation detection itself -- not very scalable!
    Return the detected ngrams as compiled regular expressions, for their faster
    detection later on.

    """
    tcf = TrigramCollocationFinder.from_words(words)
    tcf.apply_freq_filter(min_freq)
    trigrams = [' '.join(w) for w in tcf.nbest(TrigramAssocMeasures.chi_sq, top_n)]
    logging.info("%i trigrams found: %s..." % (len(trigrams), trigrams[:20]))

    bcf = tcf.bigram_finder()
    bcf.apply_freq_filter(min_freq)
    bigrams = [' '.join(w) for w in bcf.nbest(BigramAssocMeasures.pmi, top_n)]
    logging.info("%i bigrams found: %s..." % (len(bigrams), bigrams[:20]))

    # Write collocations to two files to be read by the preprocess program
    f1 = open('bigrams.txt', 'w')
    f1.writelines(["{0}\n".format(item)  for item in bigrams])
    f1.close()

    f2 = open('trigrams.txt', 'w')
    f2.writelines(["{0}\n".format(item)  for item in trigrams])
    f2.close()

    pat_gram2 = re.compile('(%s)' % '|'.join(bigrams), re.UNICODE)
    pat_gram3 = re.compile('(%s)' % '|'.join(trigrams), re.UNICODE)

    return pat_gram2, pat_gram3
