# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:38:39 2014

@author: francescocorea
"""

import numpy as np
import argparse
from distutils.version import StrictVersion
import sys
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Get the top n topics. Plot histogram of all topics. NB requires Numpy 1.8+')
parser.add_argument('-f', '--filename', help = 'Filename containing the probability vectors for each document', required = True, type=str)
parser.add_argument('-n', '--number', help = 'Return the top n topics', required = True, type=int)
parser.add_argument('-p', '--plot', help = 'Plot histogram', action='store_true')

def main():

    numpy_version = np.__version__

    if StrictVersion('1.8.1') > StrictVersion(numpy_version):
        print """Your version of numpy is too old.  This code requires >= 1.8 
        but you have version {0}""".format(numpy_version)
        sys.exit()

    args = parser.parse_args()

    X = np.genfromtxt(args.filename, unpack = True)

    topics = np.shape(X)[0]

    score = []

    for t in range(topics):

        summation = np.sum(X[:][t])
        score.append(summation)

        print t, summation

    score = np.array(score)
    ind = np.argpartition(score, -args.number)[-args.number:]

    print 'Most important topics are: '
    print ind
    print 'with scores'
    print score[ind]

    if args.plot == True:

        fig, ax = plt.subplots()
        ax.bar([x for x in range(topics)], score, color='b')
        ax.set_ylabel('Score')
        ax.set_title('A measure of relative importance of each topic within the corpus')
        ax.set_xlabel('Topic number')
        ax.set_xticklabels(tuple([str(x*10) for x in range(topics/10)]))
        plt.show()


if __name__ == "__main__":
    main()
