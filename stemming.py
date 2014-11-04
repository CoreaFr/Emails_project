# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:25:47 2014

@author: francescocorea
"""

import re
import specialwords as words
import scrubbing as scrub
import nltk
import enron
from string import digits

def stemmingListofStrings(textsid, stopwords=False):

    """
    This function takes a list of tuples (id,text) and returns the text after cleaning, tokenizer and stemming
    :param textsid: list of tuples with raw text (id,text)
    :return: returns the stemmed text as a list of tuples (id,stem_text)
    """

    texts = [text for id, text in textsid]
    ids = [id for id, text in textsid]

    # Initialize the stemmer snowball
    #stem = nltk.stem.snowball.EnglishStemmer()
    stem = nltk.stem.WordNetLemmatizer()

    # Clean the text eliminating symbols and numbers
    texts = [text.translate(None, digits) for text in texts]
    # texts = [re.sub(r'(.)\1{2}', r'', text) for text in texts]
    # texts = [re.sub('[\^~+=!-*@#$<>.,;:?|!\-\(\)/"\'\[\]]', '', text.replace('\\','')) for text in texts]

    textsid = zip(ids, texts)

    # Replace any found term in the dictionary by its abbreviation
    texts = [words.abbreviations(text.lower(), "dic_enron.csv", id) for id, text in textsid]

    textsid = zip(ids, texts)

    # Joins any ngrams found in the given files
    texts = [words.ngramsText(text.lower(), 3, "bigrams.txt", "trigrams.txt", id) for id, text in textsid]

    # Tokenize the texts and eliminates stopwords and all words with length < 2
    texts_token = [scrub.tokenizeString(text, lower=True, tokenizer="punktword") for text in texts]

    if stopwords == True:
        #Initialize the stop words
        stop_words = enron.getCustomStopwords()
        texts_token = [[x for x in text_token if x not in stop_words and len(x) > 1] for text_token in texts_token]
    elif stopwords == False:
        texts_token = [[x for x in text_token if len(x) > 1] for text_token in texts_token]

    # Apply stemming
    #texts_stem = [[stem.stem(word) for word in text_token] for text_token in texts_token]
    texts_stem = [[stem.lemmatize(word) for word in text_token] for text_token in texts_token]

    textsid = zip(ids, texts_stem)

    return textsid


def stemmingString(text, id, stopwords=False):
    """
    This function takes a text and an id and returns the text after cleaning, tokenizer and stemming
    :param text: raw text
    :param id: id of the text
    :return: returns the stemmed text
    """

    # Initialize the stemmer snowball
    #stem = nltk.stem.snowball.EnglishStemmer()
    stem = nltk.stem.WordNetLemmatizer()

    # Clean the text eliminating symbols and numbers
    text = text.translate(None, digits)
    # text = re.sub(r'(.)\1{2}', r'', text)
    # text = re.sub('[\^~+=!-*@#$<>.,;:?!|\-\(\)/"\'\[\]]', '', text.replace('\\',''))

    # Replace any found term in the dictionary by its abbreviation
    text = words.abbreviations(text.lower(), "dic_enron.csv", id)

    # Joins any ngrams found in the given files
    text = words.ngramsText(text.lower(), 3, "bigrams.txt", "trigrams.txt", id)

    # Tokenize the texts and eliminates stopwords and all words with length < 2
    text_token = scrub.tokenizeString(text, lower=True, tokenizer="punktword")
    if stopwords == True:
        #Initialize the stop words
        stop_words = enron.getCustomStopwords()
        text_token = [x for x in text_token if x not in stop_words and len(x) > 1]
    elif stopwords == False:
        text_token = [x for x in text_token if len(x) > 1]

    # Apply stemming
    #text_stem = [stem.stem(word) for word in text_token]
    text_stem = [stem.lemmatize(word) for word in text_token]

    return text_stem
