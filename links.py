# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:08:47 2014

@author: francescocorea
"""

"""Extract links from MySQL database and dump into CSV file"""

import enron
import csv, argparse
import numpy as np



# def queryDb(table, column, criteria):
#     con, cur=connectDB("enron")
#     cur.execute("select {0} from {1} where {2} ".format(column,table,criteria))
#     tmp=cur.fetchall()
#     results=tmp
#     con.close()
#     return results

import pdb


###########
# regex for extracting email addresses ([a-z,A-Z,0-9,/,/./_/']+@+[\w]+(.[\w]+)+|/HOU/ECT)
############

def indexLinks():

    con, cur=enron.connectDB("enron")
    cur.execute("select distinct `sender` from `emails`")

    tmp=cur.fetchall()
    tmp=[x[0].strip() for x in tmp]

    tmp_unique = list(set(tmp))
    
    cur.execute("select distinct `to` from `emails`")
    tmp1=cur.fetchall()
    
    print tmp1[0]
    #tmp1=[element.split(',') for element[0] in tmp1]
    #tmp1=(element for str(element).split(', ') in tmp1)

    tmp2 = [x[0].strip().split(',') for x in tmp1]
    tmp2 = [item.strip() for sublist in tmp2 for item in sublist]
    tmp2_unique = list(set(tmp2))

    cur.execute("select distinct `cc` from `emails`")
    tmp3=cur.fetchall()
    
    
    tmp4 = [x[0].strip().split(',') for x in tmp3]
    tmp4 = [item.strip() for sublist in tmp4 for item in sublist]
    tmp4_unique = list(set(tmp4))

    all_addresses = tmp_unique + tmp2_unique + tmp4_unique
    all_addresses_unique = list(set(all_addresses))
    all_addresses_unique.sort()
    con.close()
    address_file = open('addresses_all.txt', 'w')

    for idx,email in enumerate(all_addresses_unique):
        address_file.write("""{0}\t"{1}"\n""".format(idx,email))

    address_file.close()
        
    return list(enumerate(all_addresses_unique))





def sendersAndReceivers(sender):

    print 'Querying database'
    
    con,cur = enron.connectDB('enron')
    query = """select `sender`,`to`,`cc`,`id` from emails where `sender` like '%{0}%' or `to` like '%{0}%' 
            or `cc` like '%{0}%' limit 1000;""".format(sender)
    print query
    cur.execute(query)
    sendandrec = cur.fetchall()
    con.close()

    return sendandrec


    #indexdict = indexLinks()


def matchEmail(email, address_list):


    indices = [i for i, s in enumerate(address_list['email_address']) if email in s]

    if type(indices)==list:

        person_id = address_list['person_id'][indices[0]]
        return person_id

    if type(indices)==int:

        person_id=address_list['person_id'][indices]
        return person_id

    print 'Nothing found in matchEmail'
    return


parser = argparse.ArgumentParser(description='Extracts links from MySQL database and produces CSV file')
parser.add_argument("--person","-p",help="Person of interest", required=True, type=str)

#

def main():

    args = parser.parse_args()

    poi = args.person

    addresses = np.genfromtxt('addresses_all.txt', unpack = True, dtype=[('person_id','i8'), ('email_address', 'S400')], 
        delimiter='\t')


    datarows = sendersAndReceivers(args.person)

    print 'Sorting through data received'

    outname = 'email_links.txt'

    outfile = open(outname, 'w')

    for sender,to,cc,id in datarows:

        recipients = [x.strip() for x in to.split(',')+cc.split(',')]

        if (poi in sender):

            sender_id = matchEmail(sender, addresses)

            for rec in recipients:

                rec_id = matchEmail(rec,addresses)

                outfile.write('{0}\t{1}\n'.format(sender_id, rec_id))

        else:

            #get sender id

            sender_id = matchEmail(sender, addresses)

            person = recipients[[poi in x.lower() for x in recipients].index(True)]
            rec_id = matchEmail(person, addresses)

            outfile.write('{0}\t{1}\n'.format(sender_id, rec_id))


    outfile.close()



#print indexdict
#senandreclist = sendersAndReceivers(args.criteria)
#print senandreclist

#for i in senandreclist:
#    print senandreclist[0,i]


#select `sender` from `emails` where `sender` like '%sherri%';

if __name__ == '__main__':
    main()
