# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:27:10 2014

@author: francescocorea
"""

"""Code to read in entries from MySQL database"""

import os,sys
import argparse
import MySQLdb as mdb


### This code is to test that you can connect from this script to the database created by the Terminal code above. It should output something like
###    "Database version : 5.5.38-0ubuntu0.14.04.1"
# try:
#     con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');
#     cur = con.cursor()
#     cur.execute("SELECT VERSION()")
#     ver = cur.fetchone()
#     print "Database version : %s " % ver
# except mdb.Error, e:
#     print "Error %d: %s" % (e.args[0],e.args[1])
#     sys.exit(1)
# finally:    
#     if con:    
#         con.close()


# TODO: Add parsing arguments
#parser = argparse.ArgumentParser("Retrieve entry from MySQL library.")
#parser.add_argument("entry", type = int, help='Desired feature to be retrieved from database')

#args = vars(parser.parse_args())

def retrieve():
    """Retrieve an entry from the MySQL database."""
    con = mdb.connect('localhost', 'kpmg1', 's2ds', 'enron');
    with con:
        cur = con.cursor()
        #cur.execute("SELECT * FROM `Metadata`")
        
    # TABLES['emails'] = (\
    #     "CREATE TABLE `emails` (\
    #       `id` INT NOT NULL AUTO_INCREMENT,\
    #       `sender` varchar(500) NOT NULL,\
    #       `to` longtext NOT NULL,\
    #       `subject` varchar(500), \
    #       `date` datetime NOT NULL,\
    #       `cc` longtext,\
    #       `bcc` longtext,\
    #       `rawtext` longtext NOT NULL,\
    #       `text` longtext NOT NULL,\
    #       `fileloc` varchar(1000) NOT NULL,\
    #       PRIMARY KEY (id)\
    #     ) ENGINE=InnoDB;")

        cur.execute("SELECT `sender` FROM `emails`")
        #row = cur.fetchall()
        row = cur.fetchone()
    return row
    con.close()

print retrieve()
