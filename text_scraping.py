# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:23:49 2014

@author: francescocorea
"""

import sys, re, os, fileinput, glob
import numpy as np
import pprint as pp

# File name should be '.'+[1-9]{1,2,3,4}, check this

# Write a bash script which goes through all the folders and calls this Python script


# Do we want to use our in-house scrapping like this one, or the BeautifulSoup package?
def scrapeText(filename):
    """Scrape the text from the input text file."""
    file=open(filename,'r')
    text=file.read()
    words=text.split()
    # Come up with a dictionary with words with no value (a, the, on, in, it, etc) and remove them here, or define a separate function for this
    # Use the package Scrapy to reduce text encoding formats to ASCII
    # Insert variable type recognition? Recognise emails, phone numbers, addresses for example as well?
    # Deal with letter casings differently or unify to case insensitive?
    wordfreq={}
    for word in words:
        if word in wordfreq:
            wordfreq[word]+=1
        else:
            wordfreq[word]=1
    wordprobvector={}
    corpus_size=len(words)
    for word in wordfreq:
        wordprobvector[word]=float(wordfreq[word])/corpus_size
    # def sort_function(a, b):
    #     if a[1] > b[1]:
    #        return -1
    #     elif a[1] < b[1]:
    #         return 1

    wordfrqvec = []
    for word, prob in wordfreq.items():
         wordfrqvec.append((word,prob))
        
    sortedwordfrqvec=sorted(wordfrqvec, key=lambda prob: prob[1], reverse=True)

    return sortedwordfrqvec
    #result=wordfrqvec.sort(sort_function)

    #return wordfreq

    #return result[:2]

# Scrub the text to remove punctuation marks and non-words (e.g. text separators: '------------------------'

filelist=sorted(os.listdir(os.getcwd()))
for i in filelist:
    if "test_email" in i and "~" not in i and "#" not in i:
        result=scrapeText(i)
        pp.pprint(result)


