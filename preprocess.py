# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:05:16 2014

@author: francescocorea
"""

import random
from optparse import OptionParser
import MySQLdb as mdb

# These files must be present in working directory!
import scrubbing


# parser = argparse.ArgumentParser("Create database from email files")
# parser.add_argument("startdir", type = str, help='Starting place for directory tree')
# parser.add_argument("tokenizer", type = str, help='Select tokenizer: wordpunct or punktword')
# parser.add_argument("tokenminlen", type = str, help='Select minimum length of admissible tokens')
# parser.add_argument("stemmer", type = str, help='Select stemmer: lemmatize, snowball, porter or lancaster')

parser=OptionParser(usage='Usage: %prog [options]')
parser.add_option("-t","--tokenizer",action="store",type='string',default='wordpunct',
        dest="tokenizer",
        help="Set the desired tokenizer: wordpunct or punktword.")
parser.add_option("-l","--tokenminlen",action="store",type='int',default=2,dest="tokenminlen",
        help="Set the minimum character length for tokens.")
parser.add_option("-s","--stemmer",action="store",type='string',default='lemmatize',
        dest="stemmer",
        help="Choose the stemmer: lemmatize, snowball, porter or lancaster.")
parser.add_option("-sample",action="store",type='float',default='1',
        help="Use for testing fase to analyze only a sample of size N*total.")

args,opts=parser.parse_args()


def main():
    # Read arguments
    stemmer=args.stemmer
    tokenizer=args.tokenizer
    tokenminlen=args.tokenminlen
    N=args.sample

    # Open the connection to the DB
    connection = mdb.connect('localhost', 'kpmg1', 's2ds','enron')
    cur=connection.cursor()

    #Generate random sample
    random.seed(123)
    sample=random.sample(range(size[0]),int(math.floor(size[0]*N)))

    rawtext=[]

    # Query to obtain the raw emails
    for id in sample:
        cur.execute(" select text from emails where id = {0} ".format(id))
        tmp = cur.fetchall()
        rawtext.append(tmp[0][0])

    tokenizedtext=scrubbing.stemVector(scrubbing.cleanVector
                                       (scrubbing.tokenizeString(rawtext,True,tokenizer),
                                        True,True,tokenminlen),stemmer)

    f = open('output.txt', 'w')
    f.writelines(["%s\n" % item  for item in tokenizedtext])
    f.close()

    # Close all cursors
    connection.close()

if __name__ == "__main__":
main()