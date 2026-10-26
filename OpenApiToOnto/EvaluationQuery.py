import os
import csv
import re
import gensim
import nltk
import codecs
import json
from flask import Flask, render_template, session
from flask import Flask, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from gensim.models import word2vec
import logging
import urllib
import urllib.request
from pandas import read_csv
from bs4 import BeautifulSoup
import bs4 as bs
import spacy
import rdflib
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import gensim.models.keyedvectors as word2vec
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
import gensim.downloader as api
from gensim.models import KeyedVectors

msg = input()
op = []
initialOp = []
toDelete = []

tokens = nltk.word_tokenize(msg)
nlp = spacy.load("en_core_web_sm")
doc = nlp(msg)
for token in doc:

    if token.dep_ == "pobj" and token.head.dep_ == "prep":
        if token.head.lemma_ == "for" or token.head.lemma_ == "with" or token.head.lemma_ == "of":
            # iteml = token.head.lemma_ + " " + token.lemma_ + " " + token.dep_ + " " + str(token.head.head.lemma_) + str(token.head.head.i)

            triple = "&lt" + str(token.head.head.lemma_) + "," + token.head.lemma_ + " " + token.lemma_ + "&gt"

            operation = (triple, token.dep_, str(token.head.head.i), str(token.i))
            initialOp.append(operation)


    elif token.dep_ == "dobj" or token.dep_ == "compound" or token.dep_ == "amod":
        if (
                token.head.text != "need" and token.head.text != "I" and token.head.text != "want" and token.text != "want" and token.text != "need"):
            triple = "&lt" + token.head.lemma_ + ", " + token.lemma_ + "&gt"

            operation = (triple, token.dep_, str(token.head.i), str(token.i))
            initialOp.append(operation)

#print(initialOp)
for op in initialOp:
    if op[1] == "dobj":
        fIndex = op[3]
        for op2 in initialOp:
            if op2[1] == "compound" or op2[1] == "amod":
                if fIndex == op2[2]:
                    compound = op2[0].partition('&gt')
                    compound2 = compound[0].partition(',')
                    newCompound = compound2[2] + " " + compound2[0]
                    newCompound = newCompound.replace("&lt", "")
                    opDobj = op[0]
                    char1 = ','
                    char2 = '&gt'

                    toreplace = opDobj[opDobj.find(char1) + 1:opDobj.find(char2)]
                    opNew = opDobj.replace(toreplace, newCompound)

                    newTriple = (opNew, "dobj", op[2], op[3])
                    initialOp.append(newTriple)
                    toDelete.append(op)
                    initialOp.remove(op2)
                else:
                    toDelete.append(op2)

    elif op[1] == "pobj":
        fIndex = op[3]
        for op2 in initialOp:
            if op2[1] == "compound" or op2[1] == "amod":
                if fIndex == op2[2]:
                    compound = op2[0].partition('&gt')
                    compound2 = compound[0].partition(',')

                    newCompound = compound2[2] + " " + compound2[0]
                    newCompound = newCompound.replace("&lt", "")
                    opPobj = op[0]
                    char1 = ','
                    char2 = '&gt'
                    char3 = ' '

                    toreplace = opPobj[opPobj.find(char1) + 1:opPobj.find(char2)]

                    toreplace2 = toreplace[toreplace.find(char3) + 1:toreplace.find(char2)]

                    opNew = opPobj.replace(toreplace2, newCompound)
                    opNew = opNew.replace('  ', ' ')
                    newTriple = (opNew, "pobj", op[2], op[3])
                    initialOp.append(newTriple)
                    toDelete.append(op)
                    initialOp.remove(op2)

for op in toDelete:
    if op in initialOp: initialOp.remove(op)
toDelete = []

for op in initialOp:
    if op[1] == "dobj":
        fIndex = op[3]
        fIndex2 = op[2]
        for op2 in initialOp:
            if op2[1] == "pobj":
                if fIndex == op2[2]:
                    opDobj = op[0].partition('&gt')

                    opPobj = op2[0]
                    char1 = ','
                    char2 = '&gt'

                    toAdd = opPobj[opPobj.find(char1) + 1:opPobj.find(char2)]
                    newOp = opDobj[0] + ", {" + toAdd + " } &gt"

                    newTriple = (newOp, "dobj, pobj", op2[3])
                    initialOp.append(newTriple)
                    initialOp.remove(op)
                    initialOp.remove(op2)

                elif fIndex2 == op2[2]:

                    opDobj = op[0].partition('&gt')

                    opPobj = op2[0]
                    char1 = ','
                    char2 = '&gt'
                    toAdd = opPobj[opPobj.find(char1) + 1:opPobj.find(char2)]

                    newOp = opDobj[0] + ", {" + toAdd + " } &gt"

                    newTriple = (newOp, "dobj, pobj", op2[3])
                    initialOp.append(newTriple)

                    toDelete.append(op)
                    initialOp.remove(op2)

for op in toDelete:
    if op in initialOp: initialOp.remove(op)

toDelete = []

for op in initialOp:
    if op[1] == "dobj, pobj":
        fIndex = op[2]
        for op2 in initialOp:
            if fIndex == op2[2] and op2[1] == "pobj":
                opdp = op[0].partition('}')
                opPobj = op2[0]
                char1 = ','
                char2 = '&gt'

                toAdd = opPobj[opPobj.find(char1) + 1:opPobj.find(char2)]

                newOp = opdp[0] + ", " + toAdd + " } &gt"

                newTriple = (newOp, "dobj, pobj2", op2[3])
                initialOp.append(newTriple)
                initialOp.remove(op2)
                initialOp.remove(op)

print(initialOp)