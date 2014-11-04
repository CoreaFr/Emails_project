# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:07:49 2014

@author: francescocorea
"""

from gensim.models.lsimodel import LsiModel
from gensim.models.lsimodel import stochastic_svd
import time, argparse, shutil, os
from gensim import corpora
import pprint as pp
#import logging
from operator import itemgetter
import cPickle as pickle


#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

def createLsiModelforCorpus(corpusfile, dictfile, numtop):
    print "\nLoading dictionary..."
    dict = corpora.Dictionary.load_from_text(dictfile)
    print(dict)
    print "\nLoading corpus..."
    corpus = corpora.MmCorpus(corpusfile)
    print(corpus)
    print "\nPerforming Latent Semantic Indexing..."
    lsi = LsiModel(corpus=corpus, num_topics=numtop, id2word=dict, distributed=False)
    ## This is the fancy stochastic (aka truncated) SVD, however it throws runtime memory errors for me (e.g. segmentation fault)
    #lsi = stochastic_svd(corpus,rank=100,num_terms=args.ntopics)
    corpustopics=lsi.show_topics(num_words=10, log=True, formatted=False)

    rootdir=os.getcwd()
    foldername='lsi_output'
    folderpath=os.path.join(rootdir,foldername)
    if (os.path.exists(folderpath)==True):
        shutil.rmtree(folderpath)
        os.makedirs(folderpath)
    else:
        os.makedirs(folderpath)
    os.chdir(folderpath)
    lsimodelfile=(str(args.corpus).replace('.mm',''))+'_lsi.model'
    lsi.save(lsimodelfile)
    filename1= (str(args.corpus).replace('.mm',''))+'_lsi_topics.pkl'
    with open(filename1,'wb') as output:
        pickle.dump(corpustopics, output)
    os.chdir(rootdir)

    return corpustopics, lsi




parser = argparse.ArgumentParser(description='Performs Latent Semantic Analysis on an input corpus.')
parser.add_argument("--corpus","-c",help="Input name of corpus file (MM file type)",default=None, required=True, type=str)
parser.add_argument("--dict","-d",help="Input name of dictionary file",default=None, required=True, type=str)
parser.add_argument("--ntopics","-nt",help="Input desired number of topics",default=10, required=True, type=int)
parser.add_argument("--query","-q",help="Input document for similarity query against topics found",default=-1, required=False, type=int)
parser.add_argument("--nwords","-nw",help="Input desired number of words to show per topic",default=10, required=False, type=int)
parser.add_argument("--force","-f",help="Force creation of new LSI model for corpus",action='store_true',default=False, required=False)


args = parser.parse_args()



def main():

    start_time=time.time()

    rootdir=os.getcwd()
    foldername='lsi_output'
    folderpath=os.path.join(rootdir,foldername)
    if (os.path.exists(folderpath)==False or (os.path.exists(folderpath)==True and args.force==True)):
        topics, lsi = createLsiModelforCorpus(args.corpus, args.dict, args.ntopics)
    else:
        os.chdir(folderpath)
        lsimodelfile=(str(args.corpus).replace('.mm',''))+'_lsi.model'
        topicsfile=(str(args.corpus).replace('.mm',''))+'_lsi_topics.pkl'
        modelpath=os.path.join(folderpath,lsimodelfile)
        topicspath=os.path.join(folderpath,topicsfile)
        lsi = LsiModel.load(modelpath)
        topics=pickle.load(open(topicspath,'r'))
        os.chdir(rootdir)
        
    pp.pprint(lsi.show_topics(num_words=10, log=False, formatted=True))

    corpus = corpora.MmCorpus(args.corpus)

    if args.query!=-1:
        queryresult = lsi[corpus[args.query]]
        sortedqueryresult = sorted(list(queryresult), key=lambda query: abs(query[1]), reverse=True)
        print "\nSimilarity of document number {0} in corpus with corpus topics:".format(args.query)
        pp.pprint(sortedqueryresult)

    
    # Generate topic probability-document matrix, along with vector containing most probable topic (assumed to be the label) for each document
    #os.chdir(folderpath)
    outlabel_name = 'lsi_document_labels_{0}.txt'.format((args.corpus).replace('.mm',''))
    outlabel = open(outlabel_name, 'w')

    outtopic_name = 'lsi_topic_vectors_{0}.txt'.format((args.corpus).replace('.mm',''))
    outtopic = open(outtopic_name, 'w')

    for idx,doc in enumerate(corpus):
    
        tops = lsi[doc]
        doc_tops=[]
        for j in range(args.ntopics):
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

    #os.chdir(rootdir)
 
    end_time=time.time()
    runtime=end_time-start_time
    print "\nRuntime: {0} seconds\n".format(runtime)



if __name__ == "__main__":

    main()
