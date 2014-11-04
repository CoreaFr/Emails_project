# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:26:57 2014

@author: francescocorea
"""

from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer
from nltk.tokenize import PunktWordTokenizer
#from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import EnglishStemmer
from nltk.stem.snowball import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer


# Put the NLTK compendium of stop words into a set
english_stops = set(stopwords.words('english'))


def tokenizeString(string,lower=True,tokenizer="wordpunct"):
    if tokenizer=="wordpunct":
        tokenized=WordPunctTokenizer().tokenize(string)
        if lower==True:
            tokenized=[w.lower() for w in tokenized]
    if tokenizer=="punktword":
        tokenized=PunktWordTokenizer().tokenize(string)
        if lower==True:
            tokenized=[w.lower() for w in tokenized]
    return tokenized

def cleanVector(tokens,clean=True,stopremove=True,minlen=2):
    output=[]
    disallowedchar=set(["!","?",'"',"'",",",".",":",";"])
    english_stops = set(stopwords.words('english'))
    for i in tokens:
        found=False
        if len(set(i).intersection(disallowedchar))>0 or i.endswith('dn'):
            found=True
        if found==False and stopremove==False:
            output.append(i)
        if found==False and stopremove==True and minlen==0:
            if i not in english_stops:
                output.append(i)
        if found==False and stopremove==True and minlen>0:
            if i not in english_stops and len(i)>=minlen:
                output.append(i)
    return output

def stemVector(vector,method="lemmatize"):
    output=[]
    if method=='lemmatize':
        wnl = WordNetLemmatizer()
        for i in vector:
            i=wnl.lemmatize(i)
            output.append(i)
    if method=='snowball':
        st=EnglishStemmer()
        for i in vector:
            i=st.stem(i)
            output.append(i)
    if method=='porter':
        st=PorterStemmer()
        for i in vector:
            i=st.stem(i)
            output.append(i)
    if method=='lancaster':
        st=LancasterStemmer()
        for i in vector:
            i=st.stem(i)
            output.append(i)
    return output
