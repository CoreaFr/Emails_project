# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:23:10 2014

@author: francescocorea
"""

"""Code to perform the TF-IDF reweighting of the corpus"""

from gensim import corpora, models
import time
import argparse
import numpy as np
import math


def tfidfCorpus(corpusname,idf=True):

    start_time = time.time()

    # Load the raw count (TF) corpus
    corpus = corpora.MmCorpus(corpusname)

    # Define a model (which is the gensim name for a transformation) based on this corpus which performs
    #  the TFIDF transformation/calculation

    if idf == True:
        tfidf = models.TfidfModel(corpus, normalize=True)
        outname=corpusname.split(".")[0]+'_tfidf.'+corpusname.split(".")[1]
    else:
        tfidf = models.TfidfModel(corpus,wglobal=lambda doc_freq, total_docs: 1.0 ,normalize=True)
        outname=corpusname.split(".")[0]+'_unitnorm.'+corpusname.split(".")[1]

  # Apply it to the input corpus
    new_corpus = tfidf[corpus]

    # Save the new corpus
    corpora.mmcorpus.MmCorpus.serialize(outname, new_corpus)

    # This command displays the corpus. Or run a print loop over the elements of the corpus. For debugging purposes.
    #print(list(new_corpus))

    end_time=time.time()
    time_taken = end_time - start_time

    print 'Time taken to perform TF-IDF reweighting: {0}'.format(time_taken)

    return new_corpus



parser = argparse.ArgumentParser(description="Applying tf-idf to the given corpus")
parser.add_argument("--file", help="Name of the corpus in mm format",
                    default="corpus.mm",required = False, type=str)
def main():

    args = parser.parse_args()
    corpusname=args.file

    return  tfidfCorpus(corpusname,idf=True)


if __name__ == '__main__':
    main()