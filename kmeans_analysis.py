# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:09:32 2014

@author: francescocorea
"""

from sklearn.cluster import KMeans, MiniBatchKMeans
import numpy as np
from gensim import corpora, models, matutils
from time import time
import struct
import argparse
import os
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt


def npmatrixCorpus(corpusname):
    t0 = time()
    # Read corpus from file
    new_corpus = corpora.mmcorpus.MmCorpus(corpusname)
    # Convert corpus to numpy array
    X = matutils.corpus2dense(new_corpus, new_corpus.num_terms, num_docs=new_corpus.num_docs)

    # Save array to file
    outfile = corpusname.split(".")[0] + '.npy'
    np.save(outfile, X)
    print "numpy array saved in {0} sec".format(time() - t0)
    return X


def binaryMatrix(inputfile):
    outputfile = inputfile.split(".")[0] + ".bin"
    t0 = time()
    # Load from the file
    mat = np.load(inputfile)

    # Create a binary file
    binfile = file(outputfile, 'wb')
    # and write out two integers with the row and column dimension
    header = struct.pack('2I', mat.shape[0], mat.shape[1])
    binfile.write(header)
    # then loop over columns and write each
    for i in range(mat.shape[1]):
        data = struct.pack('%id' % mat.shape[0], *mat[:, i])
        binfile.write(data)
    binfile.close()
    print "Binary file saved in {0} secs".format(time() - t0)


def kmeans_test(X, cluster_array, dictionary, makeplot=True, makefile=True, bfrac=10):
    """Runs the gap statistic on a number of clusters"""

    ks, wks, wkbs, sk = gap_statistic(X, cluster_array, bfrac, dictionary)

    if makefile == True:
        outarr = np.column_stack((ks, wks, wkbs, sk))

        print 'Gap statistic written to file gap_stat.out'

        np.savetxt('gap_stat.out', outarr)

    if makeplot == True:

        gap = wkbs - wks

        gap_fn = np.zeros(len(ks) - 1)

        for i in np.arange(len(ks) - 1): gap_fn[i] = gap[i] - (gap[i + 1] - sk[i + 1])

        plt.plot(ks[:-1], gap_fn, 'b-')
        plt.xlabel('Number of clusters')
        plt.ylabel('G(k) - (G(k+1) - s(k+1))')

        plt.show()

    return


def gap_statistic(X, cluster_array, bfrac, dictionary):
    """Gap statistic code.  Requires a numpy matrix, a list of clusters to try and the number of ref samples to create"""

    ks = cluster_array
    Wks = np.zeros(len(ks))
    Wkbs = np.zeros(len(ks))
    sk = np.zeros(len(ks))

    for indk, k in enumerate(ks):
        # just use k-means++ for now. This could change or be an option as in the main script

        model = MiniBatchKMeans(init='k-means++', n_clusters=k, n_init=10, max_no_improvement=10, verbose=0)

        allvals = model.fit(X)

        with open('kmeans_top10.txt', 'a') as outfile:
            outfile.write('Top terms per cluster when {0} clusters:\n'.format(k))
            order_centroids = allvals.cluster_centers_.argsort()[:, ::-1]
            for i in range(k):
                outfile.write("Cluster %d:" % i)
                for ind in order_centroids[i, :10]:
                    outfile.write(' %s ' % dictionary[ind])
                outfile.write('\n')


        Wks[indk] = np.log10(allvals.inertia_)

        B = bfrac

        BWkbs = np.zeros(B)
        print 'clusters = {0}'.format(k)
        for i in range(B):
            print 'B = {0}'.format(i)

            Xb = np.random.random(np.shape(X))
            Bval = model.fit(Xb)
            BWkbs[i] = np.log10(Bval.inertia_)

        Wkbs[indk] = sum(BWkbs) / B  # take the mean
        sk[indk] = np.sqrt(sum((BWkbs - Wkbs[indk]) ** 2) / B)  # sd = sqrt(sum(mean-indiv)**2/n)

    # rescale
    sk = sk * np.sqrt(1. + 1. / B)

    return (ks, Wks, Wkbs, sk)

parser = argparse.ArgumentParser(description="Applying k-means clustering")
parser.add_argument("--file", help="Name of the file stored: numpy array"
                    , required=True, type=str)
parser.add_argument("--gap", help="Compute statistical gap", default=False, action='store_true')
parser.add_argument("--minibatch", help="Use MiniBatchKMeans", default=False, action='store_true')
parser.add_argument("--plot", help="plot the results", default=False, action='store_true')
parser.add_argument('--bfrac', help = 'B for gap statistics',
                    default=10,required = False, type=int)

def main():
    args = parser.parse_args()
    filename = args.file
    plot = args.plot
    bfrac = args.bfrac

    if os.path.exists("kmeans_top10.txt"):
        os.remove("kmeans_top10.txt")
    if os.path.exists("kmeans_inertia.csv"):
        os.remove("kmeans_inertia.csv")

    print "Loading dictionary..."
    dictname = "new_dic_" + '_'.join(filename.split("_")[:4])+"_freq.txt"
    dict = corpora.Dictionary.load_from_text(dictname)

    print "Loading corpus..."
    npyfile = filename + '.npy'
    npy = np.load(npyfile)
    npy=npy.transpose()
    print("n_samples: %d, n_features: %d" % npy.shape)

    t0 = time()

    Nclusters = [2, 4, 6, 8, 10]

    if args.gap:
        kmeans_test(npy, Nclusters, dict,makeplot=plot,makefile=True,bfrac=bfrac)
    else:
        for n in Nclusters:
            if args.minibatch:
                km = MiniBatchKMeans(init='k-means++', n_clusters=n, n_init=10, verbose=True)
            else:
                km = KMeans(n_clusters=n, init='k-means++', max_iter=100, n_init=1, verbose=True)
            km.fit(npy)

            with open('kmeans_top10.txt', 'a') as outfile:
                outfile.write('Top terms per cluster when {0} clusters:\n'.format(n))
                order_centroids = km.cluster_centers_.argsort()[:, ::-1]
                for i in range(n):
                    outfile.write("Cluster %d:" % i)
                    for ind in order_centroids[i, :10]:
                        outfile.write(' %s ' % dict[ind])
                    outfile.write('\n')
            with open('kmeans_inertia.csv','a') as outfile2:
                outfile2.write('{0} ; {1}\n'.format(n,km.inertia_))

    print("done in %0.3fs" % (time() - t0))

if __name__ == '__main__':
    main()
