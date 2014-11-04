# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:09:13 2014

@author: francescocorea
"""

import logging, gensim
import pdb
import random
import re
import argparse

def lda_testing(dictionary_array, corpus_array, topic_array, logfile='gensim.lda_testing.log', 
    eval_every=20, chunksize=10000, passes=2):

    """Function to test LDA on a variety of corpora with their corresponding dictionaries over a number of topics"""

    logging.basicConfig(filename=logfile, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    for dictionary,corpus in zip(dictionary_array, corpus_array):

        id2word = gensim.corpora.Dictionary.load_from_text(dictionary)

        mm = gensim.corpora.MmCorpus(corpus)

        logging.info('Using dictionary {0}'.format(dictionary))
        logging.info('Loaded corpus {0}'.corpus)

        print 'Using dictionary {0}'.format(dictionary)
        print 'Using corpus {0}'.format(corpus)

        for ntop in topic_array:

            logging.info('Using topic number {0}'.format(ntop))
            print 'Using topic number {0}'.format(ntop)

            lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=ntop, 
                eval_every=eval_every, chunksize=chunksize, passes=passes)

    return

parser = argparse.ArgumentParser(description = 'Applying LDA to a corpus')
parser.add_argument('-d', '--dictionary', help = 'Dictionary file', required = True, type = str)
parser.add_argument('-c', '--corpus', help='Corpus file', required = True, type = str)
parser.add_argument('-t', '--topics', help = 'Number of topics', required = True, type = int)
parser.add_argument('-l', '--logfile', help = 'Logfile', default='gensim.lda.log')
parser.add_argument('-s', '--savemodel', help='Option to save model. Default=False', default=False, action='store_true')    

def main():

    """Will run gensim LDA on a dictionary, corpus and set number of topics.  
    Optional arguments to give specific name to log file or to save model to file.
    To run over a range of these, checkout the lda_testing() function"""
    
    args = parser.parse_args()

    id2word = gensim.corpora.Dictionary.load_from_text(args.dictionary)

    topics = args.topics

    logging.basicConfig(filename=args.logfile, format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    mm = gensim.corpora.MmCorpus(args.corpus)

    print (args.corpus)
    print(mm)

    logging.info("Using corpus {0}".format(args.corpus))
    logging.info("Using topic number {0}".format(topics))
    print 'Running topic {0}'.format(topics)

    #This is the pure gensim version. It uses variational Bayes
    lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=topics, eval_every=20, chunksize=10000, passes=5, alpha='auto')

    if (args.savemodel==True):

        lda.save('model_{0}_auto.lda'.format(args.corpus))


    #apply to corpus again

    outlabel_name = 'lda_document_labels.{0}_auto.txt'.format(args.corpus)
    outlabel = open(outlabel_name, 'w')

    outtopic_name = 'lda_topic_vectors.{0}_auto.txt'.format(args.corpus)
    outtopic = open(outtopic_name, 'w')

    for idx,doc in enumerate(mm):
    
        tops = lda[doc]
        doc_tops=[]
        for j in range(topics):
            search = [v[1] for v in tops if v[0] == j]

            if len(search)>0:
                doc_tops.append(search[0])
            else:
                doc_tops.append(0.)

        most_important = doc_tops.index(max(doc_tops))
        outlabel.write('{0}\n'.format(most_important))
        outtopic.write('\t'.join([str(d) for d in doc_tops])+'\n')

    outlabel.close()
    outtopic.close()


    
if __name__ == "__main__":

    main()