# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:24:56 2014

@author: francescocorea
"""

"""We can use the getattr() function to test a whole range of functions/set-ups/combinations
in one place

To use this at the command line use the following:

python stemming_test.py --help (will output the correctly formatted help command)
python stemming_test.py -f 0.01 [-o mytimingsoutput.log]

-f is the fraction of the dataset you want to work on
-o an option to change the name of the output file for the timings, otherwise it writes to timings.log
"""


import os, shutil
import gensim
import nltk
from nltk.corpus import stopwords
import MySQLdb as mdb
import enron
import pdb
import os
import csv
import time
import argparse
import specialwords as words

def getFunctionName(fstring):

    """Get function/module names from the command input"""

    t1 = fstring.split()
    t2 = t1[-1][2:].strip('()')
    return t2

def cleanTokens(tokens,minlen=2):
    output=[]
    disallowedchar=set(["!","?",'"',"'",",",".",":",";","-","<",">", "/","="])

    for i in tokens:
        if ((len(set(i).intersection(disallowedchar)) == 0) and 
            (not i.endswith('dn')) and 
            (len(i) > minlen)):
            output.append(i)
        
    return output

parser = argparse.ArgumentParser(description="Testing the different tokenisation/stemming methods")
parser.add_argument('-f', '--fraction', help = 'Fraction of sample required', required = True, type=float)
parser.add_argument('-o', '--output_timelog', help = 'Output logname for timings', default = 'timings.log', type = str)
parser.add_argument('-n', '--ngrams', help='Remove ngrams', default = False, action = 'store_true')
parser.add_argument('-a', '--abbrev', help='Replace abbreviations', default = False, action = 'store_true')
parser.add_argument('-e', '--email_list', help = 'Use existing email log', type = str)
parser.add_argument('-d', '--directory', help = 'Output sub-directory name. Defaults to output', type=str, default='output')



def main():

    args = parser.parse_args()

    rootdir=os.getcwd()
    foldername=args.directory
    folderpath=os.path.join(rootdir,foldername)
    if (os.path.exists(folderpath)==True):
        shutil.rmtree(folderpath)
        os.makedirs(folderpath)
    else:
        os.makedirs(folderpath)

    stop_words = enron.getCustomStopwords()


    

    timinglog = open(os.path.join(folderpath,args.output_timelog), 'w')

    timinglog.write('#Tokeniser Stemmer/Lemmatiser Codetime Writetime\n')
    
    
    
    # NB if you make changes here also do it below for the args/kwargs


    token_command = [
    				["nltk", "f = p.tokenize.WordPunctTokenizer()", "tokenize"],
    				["nltk", "f = p.tokenize.PunktWordTokenizer()", "tokenize"],
    		      	["gensim", "f = p.utils", "tokenize"]

    ]
    
    stem_command = [
    				["nltk", "g = q.stem.snowball.EnglishStemmer()", "stem"],
    				["nltk", "g = q.stem.snowball.PorterStemmer()", "stem"],
    				["nltk", "g = q.stem.lancaster.LancasterStemmer()", "stem"],
    	       	   	["nltk", "g = q.stem.WordNetLemmatizer()", "lemmatize"],
    				["gensim", "g = q.utils", "lemmatize"]
    ]


    #Either get text as new random sample, or use existing list

    if (args.email_list==None):

        print 'Creating random sample'

        text, email_ids = enron.querySample(args.fraction, return_sample = True)

        with open(os.path.join(folderpath,'email_sample.log'), 'w') as elog:

            for id in email_ids:

                elog.write('{0}\n'.format(id))

    else:

        print 'Using existing sample ids'

        with open(args.email_list, 'r') as einput:

            email_sample = einput.readlines()

        email_sample = [e.strip('\n') for e in email_sample]

        con,cur = enron.connectDB('enron')

        text = []

        for e_id in email_sample:

            cur.execute(" select text from emails where id = {0} ".format(e_id))
            tmp=cur.fetchall()
            text.append(tmp[0][0])

        con.close()


        #make email log file anyway

        with open(os.path.join(folderpath,'email_sample.log'), 'w') as elog:

            elog.write('Email sample duplicated from {0}\n'.format(args.email_list))

            for e_id in email_sample:

                elog.write('{0}\n'.format(e_id))

        



    text = [t.lower() for t in text]

    text = ' '.join(text)

    if (args.abbrev == True):

        if os.path.exists("word_replace_dic.txt"):
            os.remove("word_replace_dic.txt")

        print "Replacing technical terms..."
        text=words.abbreviations(text,"dic_enron.csv")




    if (args.ngrams == True):

        if os.path.exists("ngrams_found.txt"):
            os.remove("ngrams_found.txt")
        print "Joining ngrams..."
        text=words.ngramsText(text,3,"bigrams.txt","trigrams.txt")


    token_args = [
                text,
                text, 
                text
                ]
    token_kwargs = [
                {},
                {},
                {}
                ]
    
    stem_kwargs = [
                {}, 
                {}, 
                {}, 
                {}, 
                {}
                ]

    
    #loop over each version


    for (tcommand, targ, tkwarg) in zip(token_command, token_args, token_kwargs):
    

        for (scommand, skwarg) in zip(stem_command, stem_kwargs):

            n1 = tcommand[0]
            n2 = getFunctionName(tcommand[1])+'.'+tcommand[2]
            n3 = scommand[0]
            n4 = getFunctionName(scommand[1])+'.'+scommand[2]
    
            output = os.path.join(folderpath,'testing_{0}.{1}_{2}.{3}.csv'.format(n1,n2,n3,n4))

            print 'Currently working on {0}.{1} with {2}.{3}'.format(n1,n2,n3,n4)
        

            start_code = time.time()

            p = __import__(tcommand[0])
            exec tcommand[1]
            text_token = list(getattr(f, tcommand[2])(targ,**tkwarg))

            #tokenising complete

            text_token = cleanTokens(text_token)

            text_token = [x for x in text_token if x not in stop_words]
    
            q = __import__(scommand[0])
            exec scommand[1]
    
            if scommand[0] == 'gensim':
    
            	text_stem  = getattr(g, scommand[2])(unicode(text_token))
    
            
            else:

    
            	text_stem = [getattr(g, scommand[2])(word) for word in text_token]
    
    
            
    
            end_code = time.time()

            codetime = end_code - start_code

            print 'Total time for set-up: {0}'.format(codetime)

            start_write = time.time()

            with open(os.path.join(folderpath,output), "wb") as f:
                writer = csv.writer(f)  
                writer.writerows([text_stem])

            end_write = time.time()

            writetime = end_write - start_write
    
            print 'Total time for write out: {0}'.format(writetime)

            timinglog.write("{0}.{1}\t{2}.{3}\t{4}\t{5}\n".format(n1, n2, n3, n4, codetime, writetime))

    timinglog.close()


if __name__ == '__main__':
    main()