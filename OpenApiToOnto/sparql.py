import json
import networkx as nx
import nltk
import rdflib
from gensim.models import KeyedVectors, word2vec
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from owlready2 import *
from networkx.readwrite import json_graph
from pygraphviz import AGraph
import tracemalloc

tracemalloc.start()

#from networkx.drawing.nx_agraph import graphviz_layout, to_agraph
#import pygraphviz as pgv

def analyze_nl_input(nl_input):
    Lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    stop_words.add('.')
    stop_words.add('(')
    stop_words.add(')')
    stop_words.add(',')
    tokens = nltk.word_tokenize(nl_input)
    filtered_input = [w for w in tokens if not w in stop_words]
    filtered_input = [Lemmatizer.lemmatize(w) for w in filtered_input]
    return filtered_input

#model = word2vec.KeyedVectors.load_word2vec_format('/Users/baharehzarei/gensim-data/word2vec-google-news-300/word2vec-google-news-300.gz', binary=True)
model = KeyedVectors.load('/Users/baharehzarei/Desktop/Mashup-demo/bio_word', mmap='r')

directory = './onto'
compatibilityGraph = nx.DiGraph()
# iterate over files
query = {'input': 'Ip', 'output': 'weather'}
for filename1 in os.listdir(directory):
    f = os.path.join(directory, filename1)
    compatibilityGraph.add_node(filename1)
    if os.path.isfile(f) and filename1 != ".DS_Store":
        for filename2 in os.listdir(directory):
            file2 = os.path.join(directory, filename2)
            if file2 != f and filename2 != ".DS_Store":
                weight = 0
                firstInstanse = rdflib.Graph()
                firstInstanse.parse(f) 
                #ns1 = rdflib.Namespace('http://www.semanticweb.org/baharehzarei/ontologies/2023/0/untitled-ontology-100#')
                ns1 = rdflib.Namespace('https://vsr.informatik.tu-chemnitz.de/ontologies/Reference_ontology')
                firstInstanse.bind('api', ns1)

                secondInstanse = rdflib.Graph()
                secondInstanse.parse(file2)
                ns1 = rdflib.Namespace('https://vsr.informatik.tu-chemnitz.de/ontologies/Reference_ontology')
                secondInstanse.bind('api', ns1)

                instanceQuery = """
                SELECT ?paramType ?paramName ?paramDescription ?o ?propName ?propType
                WHERE {{
                    ?ap api:hasOperations ?o .
                    ?o api:hasParameter ?param .
                    ?param api:parameterType ?paramType.
                    ?param api:parameterName ?paramName.
                    OPTIONAL { ?param api:parameterDescription ?paramDescription}.
                }
                UNION{
                    ?ap api:hasOperations ?o .
                    ?o api:hasRequestBody ?rb.
                    ?rb api:hasRequestBodyContent ?rqC.
                    ?rqC api:hasRBSchema ?rbSchema.
                    ?rbSchema api:hasProperties ?prop.
                    ?prop api:propertyName ?propName.
                    ?prop api:propertyType ?propType. 
                }
                }
                """

                parameter = []
                paramDescription = ''
                opParam = {}

                for row in secondInstanse.query(instanceQuery):
                    opname = row.o
                    paramDescription += f"{row.paramDescription} "
                    values = {}
                    for row2 in secondInstanse.query(instanceQuery):
                        if opname == row2.o:
                            if row2.propName and row2.propType:
                                values[f"{row2.propName}"] = f"{row2.propType}"
                            elif row2.paramName and row2.paramType:
                                values[f"{row2.paramName}"] = f"{row2.paramType}"
                    opParam[f"{row.o}".rsplit('#', 2)[1]] = values

                json_input = json.dumps(opParam)

                instanceQueryOutput = """
                SELECT ?pName ?o ?pType ?odes 
                WHERE {
                {
                    ?ap api:hasOperations ?o .
                    ?o api:hasOutput ?output.
                    ?o api:hasDescription ?odes.
                    ?output api:hasOutputContent ?oC.
                    ?oC api:hasOoutputSchema ?oSchema.
                    ?oSchema api:hasProperties ?prop.
                    ?prop api:propertyName ?pName.
                    ?prop api:propertyType ?pType.
                }
                UNION{
                    ?ap api:hasOperations ?o .
                    ?o api:hasOutput ?output.
                    ?o api:hasDescription ?odes.
                    ?output api:hasOutputContent ?oC.
                    ?oC api:hasOoutputSchema ?oSchema.
                    ?oSchema api:referesToSchema ?schemaRef.
                    ?schemaRef api:hasProperties ?prop.
                    ?prop api:propertyName ?pName.
                    ?prop api:propertyType ?pType.
                }
                }
                """
                outputDescription = ""
                apiOutput = firstInstanse.query(instanceQueryOutput)
                opOutput = {}

                for row in apiOutput:
                    putputName = row.o
                    outputDescription += f"{row.odes} "
                    values = {}
                    for row2 in firstInstanse.query(instanceQueryOutput):
                        if putputName == row2.o:
                            values[f"{row2.pName}"] = f"{row2.pType}"
                    opOutput[f"{row.o}".rsplit('#', 2)[1]] = values

                json_output = json.dumps(opOutput)
                inputs = {}
                outputs = {}

                for inputparam in opParam.keys():
                    inputs = opParam[inputparam]
                for keyOutput in opOutput.keys():
                    outputs = opOutput[keyOutput]

                for key in inputs.keys():
                    if key != "license" and key != "api-key":
                        inputName = key
                        #if inputName in model.key_to_index:
                            #print(inputName)
                            #print(model.most_similar(inputName, topn=10))
                            #print("------")
                        # FIRST CASE: if the input is in the output list and their types are compatible then an edge
                        # will be added directly to the graph
                        if inputName in outputs.keys():
                            if inputs[inputName] == outputs[inputName]:
                                #compatibilityGraph.add_edge(filename1, filename2, weight=4)
                                weight += 3
                        # SECOND CASE: if the exact parameter does not exist then we calculate the semantic similarity
                        #else:
                        op_similarity_values = 0
                        if inputs.keys() and outputs.keys():
                            term_similarity_values = (model.n_similarity(inputs.keys(), outputs.keys()))
                        else:
                            term_similarity_values= 0
                        inputDes = analyze_nl_input(paramDescription)
                        outputDes = analyze_nl_input(outputDescription)
                        if inputDes and outputDes:
                            op_similarity_values = (model.n_similarity(inputDes, outputDes))

                        if op_similarity_values > 0.65 and term_similarity_values != 0:
                            #compatibilityGraph.add_edge(filename1, filename2, weight=2)
                            weight += 2
                        if term_similarity_values > 0.5:
                            #compatibilityGraph.add_edge(filename1, filename2, weight=3)
                            weight += 1
                        if weight > 0:
                            compatibilityGraph.add_edge(filename1, filename2, weight=weight)


for u,v,d in compatibilityGraph.edges(data=True):
    d['label'] = d.get('weight','')
A = nx.nx_agraph.to_agraph(compatibilityGraph)
A.layout(prog='dot')
A.draw('test.png')


#print(compatibilityGraph);
print(compatibilityGraph.edges.data()._adjdict)

# current, peak = tracemalloc.get_traced_memory()
# tracemalloc.stop()
#
# print(f"Current memory usage: {current / 1024 / 1024:.2f} MB")
# print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")

#paths = nx.all_simple_paths(compatibilityGraph, source='IPToLocation.owl', target='GeoLocationTime.owl')
#print(list(paths))
