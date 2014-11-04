# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:09:32 2014

@author: francescocorea
"""

"""
This function computes the ngrams of a random sample of emails from the database and writes
a/two file/s with the results (bigrams.txt and/or trigrams.txt)

Usage:
python collocations --sample 0.5 --min_freq 1000 --max_ngrams 100 --word_len 3
"""
import logging

import argparse
import math
import random
import MySQLdb as mdb
import specialwords as words

#from ngrams import abb_dictionary

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

parser = argparse.ArgumentParser(description="Generating a dictionary of stopwords")
parser.add_argument("--sample",help="Size of sample in percentage", required=True,type=float)
parser.add_argument("--min_freq",help="Minimal frequency of ocurrence to be considered",required=True,type=int)
parser.add_argument("--max_ngrams",help="Maximal number of collocations to be found",required=True,type=int)
parser.add_argument("--word_len",help="Minimal word length to be considered",required=True,type=int)


def main():
    args = parser.parse_args()
    N = args.sample
    freq = args.min_freq
    n_col = args.max_ngrams
    min_len = args.word_len

    print ("Sample Size: {0}*total").format(N)
    print ("Minimum frequency: {0}").format(freq)
    print ("Maximun number of collocations: {0}").format(n_col)
    print ("Minimum word length: {0}").format(min_len)

    # Open the connection to the DB
    connection = mdb.connect('localhost', 'kpmg1', 's2ds','enron')
    cur=connection.cursor()


    # In our case the IDs are ordered by entry. Otherwise you could do:
    #  cur.execute("SELECT COUNT(*) FROM emails;")
    # The last ID number gives us the number of rows of the table.
    cur.execute("select id from emails order by id desc limit 1;")
    res = cur.fetchall()
    size=[int(col) for row in res for col in row]


    # We generate a random sample of the entries.
    #random.seed(123)
    sample=random.sample(range(size[0]),int(math.floor(size[0]*N)))

    texts=[]

    # We query the emails in the sample and store them in a list
    for id in sample:
        cur.execute(" select text from emails where id = {0} ".format(id))
        tmp=cur.fetchall()
        texts.append(tmp[0][0])

    # Join all the text into a string to be able to count the frequency of ocurrence
    raw=" ".join(texts)

    # Call a function written in specialwords
    words.ngramsFinder(raw,freq, n_col,min_len)

    # Close all cursors
    connection.close()

    return


if __name__ == "__main__":
    main()

