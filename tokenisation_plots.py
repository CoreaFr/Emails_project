# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:22:37 2014

@author: francescocorea
"""

import cPickle as pickle
import matplotlib.pyplot as plt
import numpy as np


with open('tokeniser_stats.pkl', 'rb') as pfile:
    results = pickle.load(pfile)

#make a plot of the number of unique tokens in each method

vals = [d['unique'] for d in results]
token = [d['tokeniser'] for d in results]
stem = [d['stemmer'] for d in results]
utoken = list(set(token))
ustem = list(set(stem))

n_measure = len(vals)
n_token = len(utoken)
n_stem = len(ustem)

width = 0.15
ind = np.arange(n_token)

fig, ax = plt.subplots()

col = ['#e41a1c', '#377eb8','#4daf4a','#984ea3','#ff7f00']



for idx, s in enumerate(ustem):

    lab = '.'.join(s.split('.')[-2:])
    print lab

    ax.barh(ind+width*idx, [r['unique'] for r in results if r['stemmer'] ==s],
        width, color=col[idx], label = lab)

    for bar in [r for r in results if r['stemmer']==s]:

        if bar['tokeniser'] == 'gensim.utils.tokenize':
            jdx = 0

        elif bar['tokeniser'] == 'nltk.tokenize.PunktWordTokenizer.tokenize':
            jdx = 1
        else:
            jdx = 2

        ax.text(bar['unique']-2500., jdx+width*idx+width/2.5, str(bar['unique']), color='k')

   




token_names = [u.split('.')[2] for u in utoken]

ax.set_yticks(ind + width*n_stem/2.)
ax.set_yticklabels(token_names)
ax.set_xlabel('Number of unique words generated')
ax.set_ylabel('Tokeniser')
#ax.set_ylim([2*width - 1, ind])


plt.legend(loc= 'lower right')


plt.show()