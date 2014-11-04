# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:06:02 2014

@author: francescocorea
"""

import numpy as np
from sklearn.naive_bayes import MultinomialNB
import argparse
from sklearn import cross_validation
import pdb
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
import matplotlib.pyplot as plt

from gensim import corpora, matutils



parser = argparse.ArgumentParser(description='K-fold Testing using Naive Bayes on a model')
parser.add_argument('-c', '--corpus', help = 'The corpus file in MM format. It will be translated into a sparse scipy matrix.', required = True, type = str)
parser.add_argument('-l', '--labels', help = 'A file containing a list of labels for each document in the corpus', required = True, type = str)
parser.add_argument('-k', '--kfold', help='Number of kfolds', default = 10, type=int)
parser.add_argument('-t', '--topics', help='Number of topics in model. Will do all and plot first 10', type=int)
parser.add_argument('-b', '--best_topics', nargs='+', help = 'Which labels do you want to keep?', type = int)
parser.add_argument('-s', '--stratified', help = 'Use stratified kfolds', default = False, action='store_true')

def main():

    args = parser.parse_args()

    y = np.genfromtxt(args.labels, unpack = True, dtype=int)

    ynew = []
    if (args.topics > 0):
        classes = [x for x in range(args.topics)]
        pclasses = [x for x in range(10)]
        ynew = y


    if len(args.best_topics)>0:
        classes = args.best_topics
        pclasses = classes

        for yy in y:

            if yy not in args.best_topics:

                yy = args.best_topics[np.random.randint(0,10)]

            ynew.append(yy)

    ynew = np.array(ynew)



    corpus_file = args.corpus

    print 'Reading in corpus: {0}'.format(corpus_file)

    new_corpus = corpora.mmcorpus.MmCorpus(corpus_file)

    print 'Converting corpus to sparse matrix'

    X = matutils.corpus2csc(new_corpus, new_corpus.num_terms, num_docs=new_corpus.num_docs)
        
    X = X.transpose()


    #interesting topics

   # topics = [54, 71, 21, 18, 57, 47, 49,  3,  2, 24]


    clf2 = MultinomialNB()
   # clf.fit(X,y)

    n_elements = len(ynew)
    nfolds = args.kfold

    #[x for x in range(args.topics)]

    #ybin = label_binarize(y, classes=classes)

    print 'Creating k-folds'

    #
    if args.stratified == True:

        kf = cross_validation.StratifiedKFold(y, n_folds=nfolds)

    else: 

        kf = cross_validation.KFold(n_elements, n_folds=nfolds, shuffle = True)

    score = np.zeros(nfolds)

    tpr_list = [{} for i in xrange(nfolds)]
    fpr_list = [{} for i in xrange(nfolds)]
    roc_list = [{} for i in xrange(nfolds)]



    for idx, (train, test) in enumerate(kf):

        print 'Running k-fold {0}'.format(idx)

        xtrain, ytrain = X[train], ynew[train]
        xtest, ytest = X[test], ynew[test]
        
        clf2.fit(xtrain, ytrain)
        score[idx] = clf2.score(xtest,ytest)
        y_score = clf2.predict(xtest)   #different for NB or SVC


    #fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
    #roc_auc[i] = auc(fpr[i], tpr[i])

        print 'Looping over labels'


        for cls in classes:

            fpr_list[idx][cls], tpr_list[idx][cls], threshold = roc_curve(ytest, y_score, pos_label=cls)
            
            roc_list[idx][cls] = auc(fpr_list[idx][cls], tpr_list[idx][cls])
            

        #do micro averaging over all classes

        #fpr_list[idx]["micro"], tpr_list[idx]["micro"], _ = roc_curve(ytest.ravel(), y_score.ravel())
        #roc_list[idx]["micro"] = auc(fpr_list[idx]["micro"], tpr_list[idx]["micro"])


        #make ROC curve for each class in this fold

        # Plot ROC curve
        plt.figure(idx)
        
        for cls in pclasses:
            plt.plot(fpr_list[idx][cls], tpr_list[idx][cls], label='ROC curve of class {0} (area = {1:0.2f})'
                                           ''.format(cls, roc_list[idx][cls]))

        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve for k-fold {0}'.format(idx))
        plt.legend(loc="lower right")
        plt.show()



    #for idx,sc in enumerate(score): print '{0}\t{1}'.format(idx+1, sc)
    #print 'Mean score: {0}'.format(np.mean(score))






if __name__=='__main__':

    main()