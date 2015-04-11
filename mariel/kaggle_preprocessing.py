"""
Preprocessing text and html (Tokenizing words and sentences, clean HTML, clean text, removing stopwords, stemming and lemmatization)
__author__ : Triskelion user@Kaggle (Thanks: Abhishek Thakur & Foxtrot user@Kaggle)
"""

# -*- coding: utf-8 -*-

import re

from nltk import clean_html
from nltk import SnowballStemmer
from nltk import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

# Tokenizing (Document to list of sentences. Sentence to list of words.)
def tokenize(str):
    '''Tokenizes into sentences, then strips punctuation/abbr, converts to lowercase and tokenizes words'''
    return [word_tokenize(" ".join(re.findall(r'\w+', t, flags=re.UNICODE | re.LOCALE)).lower())
            for t in sent_tokenize(str.replace("'", ""))]


# Removing stopwords. Takes list of words, outputs list of words.
def remove_stopwords(l_words, lang='english'):
    l_stopwords = stopwords.words(lang)
    content = [w for w in l_words if w.lower() not in l_stopwords]
    return content


# Clean HTML / strip tags TODO: remove page boilerplate (find main content), support email, pdf(?)
def html2text(str):
    soup = BeautifulSoup(str)
    return soup.get_text()


# Stem all words with stemmer of type, return encoded as "encoding"
def stemming(words_l, type="PorterStemmer", lang="english"):
    supported_stemmers = ["PorterStemmer", "SnowballStemmer", "LancasterStemmer", "WordNetLemmatizer"]
    if type is False or type not in supported_stemmers:
        return words_l
    else:
        l = []
        if type == "PorterStemmer":
            stemmer = PorterStemmer()
            for word in words_l:
                l.append(stemmer.stem(word))
        if type == "SnowballStemmer":
            stemmer = SnowballStemmer(lang)
            for word in words_l:
                l.append(stemmer.stem(word))
        if type == "LancasterStemmer":
            stemmer = LancasterStemmer()
            for word in words_l:
                l.append(stemmer.stem(word))
        if type == "WordNetLemmatizer":  # TODO: context
            wnl = WordNetLemmatizer()
            for word in words_l:
                l.append(wnl.lemmatize(word))
        return l


# The preprocess pipeline. Returns as lists of tokens or as string. If stemmer_type = False or not supported then no stemming.
def preprocess_pipeline(str, codeword, lang="english", stemmer_type="PorterStemmer", return_as_str=False,
                        do_remove_stopwords=False, do_clean_html=False):
    l = []
    words = []
    if do_clean_html:
        sentences = tokenize(html2text(str))
    else:
        sentences = tokenize(str)
    for sentence in sentences:
        if do_remove_stopwords:
            # add_words = []
            # if codeword == 1:
            #     add_words = ['BADREVIEW', 'BADREVIEW']
            # elif codeword == 2:
            #     add_words = ['BADREVIEW']
            # elif codeword == 4:
            #     add_words = ['GOODREVIEW']
            # elif codeword == 5:
            #     add_words = ['GOODREVIEW', 'GOODREVIEW']
            # words = remove_stopwords(sentence, lang) + add_words
            words = remove_stopwords(sentence, lang)
        else:
            words = sentence
        words = stemming(words, stemmer_type)
        if return_as_str:
            l.append(" ".join(words))
        else:
            l.append(words)
    if return_as_str:
        return " ".join(l)
    else:
        return [item for sublist in l for item in sublist]


# test_sentence = "Hello world <ab>as ."
# print("\nOriginal:\n", test_sentence)
# print("\nPorter:\n", preprocess_pipeline(test_sentence, "english", "PorterStemmer", True, False, True))
# print("Lancaster:\n", preprocess_pipeline(test_sentence, "english", "LancasterStemmer", True, False, True))
# print "\nWordNet:\n", preprocess_pipeline(test_sentence, "english", "WordNetLemmatizer", True, False, True)
# print("\nStopword Tokenized Lancaster:\n",
      # preprocess_pipeline(test_sentence, "english", "LancasterStemmer", False, True, True))
# print "\nOnly cleaning (HTML+Text):\n", preprocess_pipeline(test_sentence, "english", False, True, False, True)