from nltk.parse.stanford import StanfordParser
from nltk.tree import ParentedTree, Tree
from nltk.parse.stanford import StanfordDependencyParser
from nltk.parse.corenlp import CoreNLPDependencyParser
from nltk.parse.corenlp import CoreNLPParser

parser = StanfordParser()

# Parse the example sentence
#sent = 'A rare black squirrel has become a regular visitor to a suburban garden'
#t = list(parser.raw_parse(sent))[0]
#t = ParentedTree.convert(t)

#t.pretty_print()

pathJar= '/Users/baharehzarei/Desktop/Stanford Parser/stanford-parser-full-2015-12-09/stanford-parser.jar'
pathModels= '/Users/baharehzarei/Desktop/Stanford Parser/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar'
dependency_parser = StanfordDependencyParser(pathJar,pathModels)
result = dependency_parser.raw_parse('Autocomplete enables you to correct misspellings and get better suggestions for your address search with fewer keystrokes by enabling access to a high-performance REST API available worldwide. For your address search requests you can receives a list of suggested matches to the search text with the label and individual address elements containing highlights showing matches for the search text. HERE Technologies provides location services based on one of the HERE mapping platform.')
dep = result.__next__()

the_triples = list(dep.triples())
# for l in the_triples:
#     print(l)
#     print('\n')


#depparser = CoreNLPParser('http://localhost:9000')
#sent = 'this api which developed by Hasan, distributes the products'
#depparser.parse(sent)
#next(parser.raw_parse(sent)).pretty_print()



def find_subject(t):    
    for s in t.subtrees(lambda t: t.label() == 'NP'):
        for n in s.subtrees(lambda n: n.label().startswith('NN')):
            return (n[0], find_attrs(n))
            
def find_predicate(t):    
    v = None
    
    for s in t.subtrees(lambda t: t.label() == 'VP'):
        for n in s.subtrees(lambda n: n.label().startswith('VB')):
            v = n
        return (v[0], find_attrs(v))
    
def find_object(t):    
    for s in t.subtrees(lambda t: t.label() == 'VP'):
        for n in s.subtrees(lambda n: n.label() in ['NP', 'PP', 'ADJP']):
            if n.label() in ['NP', 'PP']:
                for c in n.subtrees(lambda c: c.label().startswith('NN')):
                    return (c[0], find_attrs(c))
            else:
                for c in n.subtrees(lambda c: c.label().startswith('JJ')):
                    return (c[0], find_attrs(c))
                
def find_attrs(node):
    attrs = []
    p = node.parent()

    # Search siblings
    if node.label().startswith('JJ'):
        for s in p:
            if s.label() == 'RB':
                attrs.append(s[0])
                
    elif node.label().startswith('NN'):
        for s in p:
            if s.label() in ['DT','PRP$','POS','JJ','CD','ADJP','QP','NP']:
                attrs.append(' '.join(s.flatten()))
    
    elif node.label().startswith('VB'):
        for s in p:
            if s.label() == 'ADVP':
                attrs.append(' '.join(s.flatten()))
                
    # Search uncles
    if node.label().startswith('JJ') or node.label().startswith('NN'):
        for s in p.parent():
            if s != p and s.label() == 'PP':
                attrs.append(' '.join(s.flatten()))
                
    elif node.label().startswith('VB'):
        for s in p.parent():
            if s != p and s.label().startswith('VB'):
                attrs.append(s[0])
                
    return attrs	
    
#sent = 'Autocomplete enables you to correct misspellings '
sent='web sevice has a name'
t = list(parser.raw_parse(sent))[0]
t = ParentedTree.convert(t)

print(find_subject(t))
print (find_predicate(t))
print (find_object(t))