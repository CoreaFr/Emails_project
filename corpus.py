# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:00:39 2014

@author: francescocorea
"""

import os
import time
import MySQLdb as mdb
from gensim import corpora, models, matutils
from sklearn.feature_extraction import DictVectorizer
import enron
import create_dic as dic
import argparse
import stemming as stem


def main():

    with open('new_dic.txt') as myfile:
        count = sum(1 for line in myfile)
    print count
    corpus = corpora.mmcorpus.MmCorpus('test.mm')
    print corpus[20]
    # Define a model (which is the gensim name for a transformation) based on this corpus which performs the TFIDF transformation/calculation
    tfidf = models.TfidfModel(corpus)
    # Apply it to the input corpus
    new_corpus = tfidf[corpus]
    # Save the new corpus
    corpora.mmcorpus.MmCorpus.serialize('corpus_tfidf.mm', new_corpus)
    # print new_corpus[20]
    new_corpus = corpora.mmcorpus.MmCorpus('corpus_tfidf.mm')
    print new_corpus[20]
    matrix=matutils.corpus2dense(new_corpus,56666,num_docs=100)

    print len(new_corpus)

    # dictionary.id2token("4300")

if __name__ == '__main__':
    main()
