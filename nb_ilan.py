# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:07:16 2014

@author: francescocorea
"""

"""Compute the probability that a given document could be generated from a topic set (provided by LSI/LDA/...)"""

import enron
import stemming as stem
import cPickle as pickle


def importTopics(filename):
    topics_file = pickle.load(open(filename,'r'))
    topics =[]
    topicnumber=0
    for i in topics_file:
        for j in i:
            topics.append([topicnumber, str(j[1])])
        topicnumber+=1
    #print topics
    # The following removes word overlap between topics and leaves only unique words from all the topics. If this is not desired just return 'topics' instead
    found = set()
    for item in topics:
        if item[1] not in found:
            found.add(item[1])
    uniquetopics=list(found)
    #print uniquetopics
    return uniquetopics


def pofTgivenD(doc,topics):
    tokencount=0
    matchcount=0
    for i in doc:
        #print doc
        tokencount+=1
        for j in topics:
            if (i == j):
                matchcount+=1
                #print "Match found for word {0} in topic {1}".format(i,j[0])
    #print matchcount, tokencount
    try:
        proboftopicgivendoc = float(matchcount)/float(tokencount)
    except ZeroDivisionError:
        proboftopicgivendoc = 0.0
    return proboftopicgivendoc




def main():

    topics=importTopics('corpus_min1_stopwdsTrue_all_tfidf_lsi_topics.pkl')
    #topics=importTopics('test_corpus_lsi_topics.pkl')
    #print topics[0][0]

    con, cur=enron.connectDB("enron")

    cur.execute("select id from emails order by id desc limit 1;")
    res = cur.fetchall()
    tmp = [int(col) for row in res for col in row]
    size=tmp[0]

    #pofD=1./float(size)
    #pofT=1./10.

    tot=0
    for id in range(1,size):
        cur.execute(" select text from emails where id = {0} ".format(id))
        tmp = cur.fetchall()
        text = enron.cleanString(enron.stripCharacters(tmp[0][0]))
        text_stem = stem.stemmingString(text, id, stopwords=True)
        #topicprob=pofTgivenD(text_stem,topics)*pofD/pofT 
        topicprob=pofTgivenD(text_stem,topics)     
        tot+=topicprob
        if topicprob>1.: print "ERROR: PROBABILITY LARGER THAN 1",id, topicprob
        if id % 1000 == 0: print "Email {0} processed, probability sum: {1}".format(id,tot)
        #print "Probability of generating email {0} from this topic set: {1}".format(id,topicprob)
    con.close()


    print "Final sum of probabilities:",tot



if __name__ == '__main__':
    main()
