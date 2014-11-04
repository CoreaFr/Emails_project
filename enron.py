# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:09:33 2014

@author: francescocorea
"""

"""Functions we might find useful"""

import MySQLdb as mdb
from nltk.corpus import stopwords
import random
import math
import re


def stripCharacters(string, backslash_char = True):

    """Strips the weird non-unicode characters that appear in the odd email"""

            
    newstring = re.sub(r"[\x90-\xff]", '',string)

    if (backslash_char == True):
        newstring2 = re.sub(r'\r|\n|\t', ' ', newstring)
    else:
        newstring2 = newstring

    return newstring2

def cleanString(textstring):


    textstring = textstring.lower()

    #first remove all the \n and unicode remnants

    textstring = stripCharacters(textstring)


    match = re.search(r'Original Message', textstring)

    #match.start is the index of the first occurance of the search string. Want the 
    #message from the beginning to that point

    if (match==None):
        textstring = textstring
    else:
        textstring = textstring[:match.start()]

    #next remove any email addresses
    #sometimes they are not xxx@enron.com, but Name/HOU/ECT@ECT so need to include
    #internal messages
    textstring = re.sub(r"[a-z,A-Z,0-9,/]+@+[\w]+", r' ', textstring)
    textstring = re.sub(r'/HOU/ECT', r'', textstring)
    
    #proper emails
    textstring = re.sub(r"[a-z,A-Z,0-9,/,.]+@+[\w]+.\w*", r' ', textstring)
    #relic html tags
    textstring = re.sub(r"<(|/)\w+>", r' ', textstring)
    #websites
    #this isn't going to be perfect but I think it's good enough in this case
    #there are pages of discussions about what to do with regex to extract
    #urls on the internet and none of them work on everything
    #this works on anything starting http(s) or www.
    textstring = re.sub(r"(?:http(s)?://|www.)\S+", r'  ', textstring)

    #times

    textstring = re.sub(r"\d{2}(:|\s)\d{2}\s(p|a)m", r' ', textstring)

    #dates

    textstring = re.sub(r"\d{2}/\d{2}/\d{4}", r' ', textstring)
    #attachment names
    textstring = re.sub(r"[0-9,a-z,.,_]*.pdf",r' ',textstring)
    textstring = re.sub(r"[0-9,a-z,.,_]*.doc",r' ',textstring)

    textstring = re.sub(r"\d{3}(-|\s)\d{3}(-|\s)\d{4}", r'  ', textstring)

    #any directories showing up

    textstring = re.sub(r"(|\w*)\\[a-z,\\]*", r' ', textstring)

    #removes all numeric strings or anything that is a mix of numbers and letters

    textstring = re.sub (r"\b(?=\w*\d)\w+", r'  ', textstring)

    #assorted punctuation punctuation
    textstring = re.sub(r"""\[\^~\+=!-\*@#\$<>\.,;:\?!\|\-\(\)/"\'\[\]\{\}\\]""", r'  ' , textstring)
    
    #finally any character which repeats >2 times
    #will remove any extra whitespace for example
    textstring = re.sub(r'(.)\1{2,}\w+', r' ', textstring)

    textstring = re.sub(r'\s\s*', r' ', textstring)

    return textstring

def getCustomStopwords(filename='add_stopwords.txt'):

    """Returns the full list, plus our new list of stopwords"""

    swords = stopwords.words('english')

    with open(filename, 'r') as f:

        new = f.readlines()

    new = [unicode(n.strip()) for n in new]

    updated = swords + new

    return updated

def addToStopwords(word, filename = 'add_stopwords.txt'):

    """Add single word to stopwords file"""

    with open(filename, 'a') as f:
        f.write(unicode(word+'\n'))

    return

def queryDb(table, column, criteria):
    con, cur=connectDB("enron")
    cur.execute("select {0} from {1} where {2} ".format(column,table,criteria))
    tmp=cur.fetchall()
    results=tmp
    con.close()
    return results

def querySample(N, seed=False, return_sample = False):
    con, cur=connectDB("enron")

    cur.execute("select id from emails order by id desc limit 1;")
    res = cur.fetchall()
    size=[int(col) for row in res for col in row]

    # We generate a random sample of the entries.
    if seed != False:
        random.seed(seed)

    sample=random.sample(range(size[0]),int(math.floor(size[0]*N)))
    print "{0}% sample ({1} emails) extracted at random".format(N*100.,int(math.floor(size[0]*N)))
    texts=[]

    # We query the emails in the sample and store them in a list
    for id in sample:
        cur.execute(" select text from emails where id = {0} ".format(id))
        tmp=cur.fetchall()
        texts.append(tmp[0][0])

    con.close()

    if not return_sample:
        return texts
    else:
        return (texts, sample)

def deleteTable(cur, tablename):
        """Delete a table when you are connected to the database"""
        cur.execute("""DROP TABLE IF EXISTS {0}""".format(tablename))
        return

def deleteDB(cur, dbname):
	"""Delete a database when you are connected to it"""
        cur.execute("""DROP DATABASE IF EXISTS {0}""".format(dbname))
        return

def connectDB(db):
	"""Connect to a database with the following credentials"""
        connection = mdb.connect('localhost', 'kpmg1', 's2ds', db)
        cursor=connection.cursor()
        return (connection,cursor)
