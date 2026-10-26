import json
import networkx as nx
import nltk
import rdflib
from gensim.models import KeyedVectors, word2vec
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from owlready2 import *

directory = './onto1'
filename2 = "VisualCrossingWeatherAPI.owl"
file2 = os.path.join(directory, filename2)

secondInstanse = rdflib.Graph()
secondInstanse.parse(file2)
ns1 = rdflib.Namespace('http://www.semanticweb.org/baharehzarei/ontologies/2023/0/untitled-ontology-100#')
secondInstanse.bind('api', ns1)

instanceQuery = """
SELECT ?paramType ?paramName ?paramDescription ?o ?propName ?propType
WHERE {
    ?ap api:hasOperations ?o .
    ?o api:hasParameter ?param .
    ?param api:parameterType ?paramType.
    ?param api:parameterName ?paramName.
    OPTIONAL { ?param api:parameterDescription ?paramDescription}.


}
"""

for row in secondInstanse.query(instanceQuery):
    print(row)
