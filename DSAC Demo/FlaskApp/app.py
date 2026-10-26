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

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

app = Flask(__name__)
app.secret_key = 'any random string'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def main():
    session['sequence'] = "ext1"
    session['number'] = 1
    session['domain'] = ""
    session['initialDes'] = ""

    return render_template('index.html')


@app.route("/query")
def query():
    return render_template('query.html')


@app.route("/dsource")
def Dsources():
    return render_template('dsource.html')


@app.route("/resOnt")
def resOnt():
    return render_template('resOnt.html')


@app.route("/danalysis")
def danalysis():
    return render_template('danalysis.html')


@app.route("/keyWords2")
def keyWords2():
    return render_template('keyWords2.html')


@app.route("/nlanlayse")
def nlanlayse():
    # create a table data to send to template
    result = ["first", "second", "third"]
    return render_template('nlanlayse.html')


@app.route("/keyWords")
def keyWords():
    return render_template('keyWords.html')


@app.route("/apiCompose")
def apiCompose():
    return render_template('apiCompose.html')


@app.route("/ontologygen")
def ontologygen():
    # create model from already uploaded files.
    f = open('./model/merged.txt', 'r')
    filedata = f.read()
    f.close()
    newdata = re.sub(r'[$|.|!|,]', r' ', filedata)
    f = open('./model/merged.txt', 'w')
    f.write(newdata)
    f.close()

    # removing the stop words
    words = ['for', 'in', 'of', 'and', 'the', 'is', 'The', 'an']
    f = open('./model/merged.txt', 'r')
    filedata = f.read()
    f.close()
    for word in words:
        filedata = filedata.replace(word, "")
    f = open('./model/merged.txt', 'w')
    f.write(filedata)
    f.close()

    with open('./model/merged.txt', "r") as fp:
        with open('./model/merged1.txt', 'a') as newfile:
            for line in fp:
                line = line.strip()
                line = line.decode('utf-8', 'ignore').encode("utf-8")
                newfile.write(line)
    # training the Word2vec model based on the uploaded data
    sen = gensim.models.word2vec.LineSentence('./model/merged1.txt')
    model = word2vec.Word2Vec(sen, size=300, min_count=3)
    model.save('./model/newmodel.model')
    return render_template('ontologygen.html')


# In this step domain expert can upload domain related files to creat domain ontology
@app.route("/ontofinal")
def ontofinal():
    with open('./model/concepts.csv', 'r') as ft:
        with open('./model/ontoloogy.owl', 'a') as newfile:
            for word in ft:
                newfile.write('<owl:Class rdf:ID="' + word.strip() + '"/>')
                newfile.write('\n')
    return render_template('ontofinal.html')


@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'Files/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
        with open('./model/merged.txt', 'a') as outfile:
            with open(destination) as newfile:
                for line in newfile:
                    outfile.write(line)
    return render_template("complete.html")


# NLP
@app.route("/nl", methods=['POST'])
def nl():
    if request.method == 'POST':
        nl_text = request.form['word']

    def recursion(tupl):
        if (type(tupl[1]) is str):
            print(tupl)
        elif type(tupl[1]) is tuple:
            foo(tupl)

    def tree_to_pos_tagged_list(tree):
        pos_tagged_words = []
        for tupl in tree.pos():
            pos_tagged_words.append(tupl[0])
        return pos_tagged_words


# tokenize the input
def analyze_nl_input(nl_input):
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = nltk.word_tokenize(nl_input)
    filtered_input = [w for w in tokens if not w in stop_words]
    filtered_input = [lemmatizer.lemmatize(w) for w in filtered_input]
    tagged = nltk.pos_tag(filtered_input)
    return tagged


# extracting target domain
def domainExtraction(msg):
    session['number'] += 1
    open("/Users/baharehzarei/Desktop/Mashup-demo/requestFiles/requestTemp" + str(session['number']) + ".txt",
         "w").close()

    # the domains are comming from the web service registry.
    transportation = ['Transportation', 'car', 'train', 'departure', 'transport', 'arrival']
    weather = ['Weather', 'weather', 'rain', 'forcast']
    finance = ['Finance', 'tax', 'ecommerce', 'money', 'pay', 'banking']

    travel = ['Travel', 'trip', 'travel', 'hotel', 'flight', 'room']
    mobile = ['Mobile', 'music', 'Facebook', 'social']
    mapping = ['Mapping', 'vehicle', 'navigate', 'routing', 'GPS', 'longitude', 'latitude', 'map', 'location',
               'coordinates']

    domains = [transportation, weather, travel, mapping, mobile, finance]

    # this one takes 2 minites to load the model
    # model = word2vec.KeyedVectors.load_word2vec_format('/Users/baharehzarei/gensim-data/word2vec-google-news-300/word2vec-google-news-300.gz', binary=True)

    # create and saves minimal version of the model
    # model = word2vec.KeyedVectors.load_word2vec_format('/Users/baharehzarei/gensim-data/word2vec-google-news-300/word2vec-google-news-300.gz',binary=True)
    # model.init_sims(replace=True)
    # model.save('/Users/baharehzarei/Desktop/Mashup-demo/bio_word')

    model = KeyedVectors.load('/Users/baharehzarei/Desktop/Mashup-demo/bio_word', mmap='r')

    lemmatizer = WordNetLemmatizer()

    input_taggs = analyze_nl_input(msg)

    nouns = [word for word, pos in input_taggs \
             if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    verbs = [verb for verb, pos in input_taggs \
             if (pos == 'VB' or pos == 'VBD' or pos == 'VBG')]

    lemmatized_verbs = [lemmatizer.lemmatize(w, wordnet.VERB) for w in verbs]

    # calculate the similarity for each domain
    similarity_values = {}
    for domain in domains:
        similarity_values[domain[0]] = (model.n_similarity(nouns, domain))

    # identify the target domain
    max_similarity = max(similarity_values.values())
    if max_similarity < 0.4:
        target_domain = "Domain is not found"
    else:
        target_domain = [k for k, v in similarity_values.items() if v == max_similarity]
        target_domain = str(target_domain)

    target_domain = re.sub(r'\[\'', '', (target_domain))
    target_domain = re.sub(r'\'\]', '', (target_domain))

    return target_domain + "&" + str(max_similarity)


# extracting operations
def operationExt(msg):
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

    print(initialOp)
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

    return initialOp


# generating responces for general questions
def generateRes(msg):
    # building the dataset
    raw_data = urllib.request.urlopen('https://www.w3.org/TR/wsdl.html')
    raw_data = raw_data.read()
    html_data = bs.BeautifulSoup(raw_data, 'lxml')
    all_paragraphs = html_data.find_all('p')
    article_content = ""

    for p in all_paragraphs:
        article_content += p.text

    article_content = article_content.lower()
    sentence_list = nltk.sent_tokenize(article_content)
    remove_punctuation = dict((ord(punctuation), None) for punctuation in string.punctuation)

    chatbot_response = ''
    sentence_list.append(msg)
    word_vectors = TfidfVectorizer(tokenizer=RemovePunctuations, stop_words='english')
    vecrorized_words = word_vectors.fit_transform(sentence_list)
    similarity_values = cosine_similarity(vecrorized_words[-1], vecrorized_words)
    similar_sentence_number = similarity_values.argsort()[0][-2]
    similar_vectors = similarity_values.flatten()
    similar_vectors.sort()
    matched_vector = similar_vectors[-2]
    if (matched_vector == 0):
        chatbot_response = chatbot_response + "I am sorry! I don't understand you"
        return chatbot_response
    else:
        chatbot_response = chatbot_response + sentence_list[similar_sentence_number]
        return chatbot_response


def LemmatizeWords(words):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in words]


def RemovePunctuations(text):
    remove_punctuation = dict((ord(punctuation), None) for punctuation in string.punctuation)
    return LemmatizeWords(nltk.word_tokenize(text.lower().translate(remove_punctuation)))


@app.route("/getinput", methods=['GET', 'POST'])
def getinput():
    msg = request.form["msg"]

    if (msg == 'thanks' or msg == 'thank you very much' or msg == 'thank you'):
        output = "Most welcome"
        session['sequence'] = "end"

    elif (msg == "bye" or msg == "done"):
        output = "take care, Bye .."
        session['sequence'] = "end"
    # else:
    #     output = generateRes(msg)
    #     session['sequence'] = "finish"

    if session["sequence"] == "ext1":
        res = domainExtraction(msg)

        session['initialDes'] = msg
        if res == "Domain is not found":
            session['sequence'] = "ext2"
            output = "I could not find the domain. Please choose one from the following categories."

            return output
        else:
            session['domain'] = res
            Domain = res.partition("&")

            output = "Your target domain is " + Domain[0] + "(yes/no)"

            session['sequence'] = "askDomainconfirm"

    elif session['sequence'] == "ext2":
        session['domain'] = domainExtraction(msg)
        with open("/Users/baharehzarei/Desktop/Mashup-demo/requestFiles/requestTemp" + str(session['number']) + ".txt",
                  "w") as f:
            data = "Domain: " + session['domain']
            f.write(data)
            f.close
        session['sequence'] = "operationExt"


    elif session['sequence'] == "askDomainconfirm":
        if (msg == "yes" or msg == "Yes"):
            with open("/Users/baharehzarei/Desktop/Mashup-demo/requestFiles/requestTemp" + str(
                    session['number']) + ".txt", "w") as f:
                data = "Domain: " + session['domain']
                f.write(data)
                f.close
            session['sequence'] = "operationExt"

        elif msg == "no":
            output = "my bad, tell me the target domain"
            session['sequence'] = "ext2"
            return output

    if session['sequence'] == "operationExt":
        operationList = operationExt(session['initialDes'])

        if len(operationList) == 0:
            output = "ops! Could not find any operation. Tell me what you need from a web service?"
            session['sequence'] = "finish"
        else:
            session['sequence'] = "finish"
            output0 = ''.join(map(str, operationList))
            return output0 + ":" + "check the following table. Wanna add more operations? if yes enter your description." + ";" + \
                session['domain']

    if session['sequence'] == "finish":
        operationList = operationExt(msg)
        if len(operationList) == 0:
            output = "Oops! Could not find any operation. Tell me what you need from a web service?"

        else:
            output0 = ''.join(map(str, operationList))

            return output0 + ":" + "here are the new extraction"

    elif session['sequence'] == 2:
        output = "ok, this is the second time" + msg
        session['sequence'] += 1

    return output

    # #run the NLP tagging
    # def analyze_nl_input(nl_text):
    #     tokens = nltk.word_tokenize(nl_text)
    #     tagged = nltk.pos_tag(tokens)
    #     parse_tree = nltk.chunk.ne_chunk(tagged)
    #     return parse_tree

    # def check_known_pattern(parse_tree):
    #     #the patterns should probably be defined in the domain-independent goal model, as properties of specific subtypes like ObjectQuestion
    #     patterns = [
    #         ('NonsenseTestBla', 'WP', 'VBZ', 'JJ', 'PERSON'),
    #         ('ObjectQuestion1', 'WP', 'VBZ', 'IN', 'PERSON'),
    #     ]
    #     matching_patterns = []

    #     for pattern in patterns:
    #         cursor = 1
    #         for node in parse_tree:
    #             check = ''
    #             if isinstance(node, nltk.tree.Tree):
    #                 check = node._label
    #             elif isinstance(node, tuple):
    #                 check = node[1]
    #             else:
    #                 raise ValueError
    #             if check == pattern[cursor]:
    #                 cursor += 1
    #                 if cursor == len(pattern):
    #                     matching_patterns.append(pattern)
    #                     break

    #     return matching_patterns

    # parse_tree = analyze_nl_input(nl_text)
    # pos_tagged_words = tree_to_pos_tagged_list(parse_tree)
    # pos_tagged_words_json = jsonify(pos_tagged_words)

    # f= filter(lambda t:(t[1]=='VBP') or (t[1]=='NN') , pos_tagged_words)
    # tags = map(lambda t: t[0], f)

    # #IMPORTANT MODIFICATION: for each domain the most similar word to that domain should be added to the list 
    # #UPDATE: following list will be filled by the result of word2vec algorithm
    # travel=['transit','trip', 'plan','flight','vacation','travel']
    # business = ['marketing', 'bank']
    # academic = ['university','course']

    # for word in tags:
    #     if word in travel:
    #         domain ='Travel'
    #     elif word in business:
    #         domain = 'Business'
    #     elif word in academic:
    #         domain= 'Academic'
    #     else:
    #         domain = 'Domain is Not Recognised, Generate the Domain Ontology'

    # patterns = check_known_pattern(parse_tree)
    # if domain=='Domain is Not Recognised, Generate the Domain Ontology':
    #     return render_template('keyWords2.html', value=domain)
    # else:
    #     return render_template('keyWords.html', value=domain)


@app.route("/ontogen", methods=['POST'])
def ontogen():
    if request.method == 'POST':
        word_list = []
        w1 = request.form['word1']
        word_list += [w1]
        w2 = request.form['word2']
        word_list += [w2]
        w3 = request.form['word3']
        word_list += [w3]
        w4 = request.form['word4']
        word_list += [w4]
        w5 = request.form['word5']
        word_list += [w5]

    model1 = word2vec.Word2Vec.load('./Files/ewmodel.model')
    with open('./model/concepts.csv', 'w+') as outfile:
        for word in word_list:
            for row in (model1.most_similar([word], topn=10)):
                for column in row:
                    outfile.write('%s;' % column)
                outfile.write('\n')
        outfile.close()

    df = read_csv('./model/concepts.csv', sep=';')
    df.columns = ['word', 'no', 'emp']
    df.drop(['no'], axis=1, inplace=True)
    df.drop(['emp'], axis=1, inplace=True)
    df
    df.to_csv('./model/concepts.csv')

    f = open('./model/concepts.csv', 'r')
    filedata = f.read()
    f.close()
    newdata = re.sub(r'[1|2|3|4|5|6|7|8|9|0|,]', r'', filedata)
    f = open('./model/concepts.csv', 'w')
    f.write(newdata)
    f.close()

    return render_template('resOnt.html', value=word_list)


@app.route('/parse', methods=['POST'])
def parseurl():
    if request.method == 'POST':
        url = request.form['url']
    conn = urllib2.urlopen(url)
    html = conn.read()

    soup = BeautifulSoup(html)
    links = soup.find_all('a')

    for tag in links:
        link = tag.get('href', None)
        if link is not None:
            print(link)
    return render_template("dsource.html")


@app.route('/similar', methods=['POST'])
def similar_words():
    if request.method == 'POST':
        word = request.form['word']
    n = request.args.get('topn')
    if not n:
        n = 10
    else:
        n = int(n)

    model1 = word2vec.Word2Vec.load('./Files/newmodel.model')
    # saving result vectors in Coma Seprated values to create the graph in d3
    out = open('./Files/csv.csv', 'w')
    for row in (model1.most_similar([word], topn=n)):
        for column in row:
            out.write('%s;' % column)
        out.write('\n')
    out.close()

    return jsonify(model1.most_similar([word], topn=n))


@app.route('/modelc', methods=['POST'])
def model_creation():
    # create model from already uploaded files
    f = open('./model/merged.txt', 'r')
    filedata = f.read()
    f.close()
    newdata = re.sub(r'[$|.|!|,]', r' ', filedata)
    f = open('./model/merged.txt', 'w')
    f.write(newdata)
    f.close()

    words = ['for', 'in', 'of', 'and', 'the', 'is', 'The', 'an']
    f = open('./model/merged.txt', 'r')
    filedata = f.read()
    f.close()
    for word in words:
        filedata = filedata.replace(word, "")
    f = open('./model/merged.txt', 'w')
    f.write(filedata)
    f.close()

    with open('./model/merged.txt', "r") as fp:
        with open('./model/merged1.txt', 'a') as newfile:
            for line in fp:
                line = line.strip()
                line = line.decode('utf-8', 'ignore').encode("utf-8")
                newfile.write(line)

    sen = gensim.models.word2vec.LineSentence('./model/merged1.txt')
    model = word2vec.Word2Vec(sen, size=300, min_count=3)
    model.save('./Files/newmodel.model')
    return render_template("danalysis2.html")


if __name__ == '__main__': app.run(host='0.0.0.0', port='8000')
app.run(debug=True)
