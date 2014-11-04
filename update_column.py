# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:38:41 2014

@author: francescocorea
"""

"""Update any column of text with a new version
In the case of the script so far, we employ a more thorough cleaning
to the rawtext column and update the text column
Only assumption is really that you have an ID field in the table
"""

import MySQLdb as mdb
import argparse
import enron
import createdb
import re
import logging
import pdb

parser = argparse.ArgumentParser("Update a column in an existing database")
parser.add_argument("-n", "--name", help = 'Database name', required = True, type = str)
parser.add_argument("-t", "--table", help = 'Table name', required = True, type = str)
parser.add_argument("-c", "--column", help = 'Column name', required = True, type =str)




def ultraClean(textstring):

    """Extra cleaning the text"""

    textstring = textstring.lower()

    #first remove all the \n and unicode remnants

    textstring = enron.stripCharacters(textstring)


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


    #assorted punctuation punctuation
    textstring = re.sub('[\^~+=!-*@#$<>.,;:?!|\-\(\)/"\'\[\]]', r' ' , textstring)
    
    #finally any character which repeats >2 times
    #will remove any extra whitespace for example
    textstring = re.sub(r'(.)\1{2,}', r' ', textstring)



    return textstring


def main():


    args = parser.parse_args()
    print args

    connection, cursor = enron.connectDB(args.name)

    cursor.execute("select ID from emails order by id desc limit 1;")
    #cursor.execute("select ID from {0} order by id desc limit 1;".format(args.table))
    numrows = int(cursor.fetchone()[0])

    #loop over number of rows
    #this is less efficient than operating on the database as a whole
    #but it won't make your computer slow down and explode

    
    for id in range(1, numrows+1):
        
        #fetch the rawtext

        cursor.execute("select rawtext from emails where id = {0}".format(id))
        rawtext = cursor.fetchone()[0]

        cleantext = ultraClean(rawtext)

        cleantext_escape = mdb.escape_string(cleantext)

        query = """UPDATE emails set {0}='{1}' where `id` =  {2};""".format(args.column, cleantext_escape, id)
        #query = """UPDATE {0} set {1}='{2}' where `id` =  {3};""".format(args.table, args.column, cleantext_escape, id)
        
        cursor.execute(query)
        connection.commit()

        print 'Updated entry {0}'.format(id)


    connection.close()

if __name__ =='__main__':

    main()

