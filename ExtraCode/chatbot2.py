from chatterbot import ChatBot
import re
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import nltk
from nltk.corpus import stopwords

def analyze_nl_input(nl_input):
    stop_words = set(stopwords.words('english')) 
    tokens = nltk.word_tokenize(nl_input)
    filtered_input =[w for w in tokens if not w in stop_words]
    tagged = nltk.pos_tag(filtered_input)
    parse_tree = nltk.chunk.ne_chunk(tagged)
    return parse_tree


def check_known_pattern(parse_tree):
    #the patterns should probably be defined in the domain-independent goal model, as properties of specific subtypes like ObjectQuestion
    patterns = [
        ('NonsenseTestBla', 'WP', 'VBZ', 'JJ', 'PERSON'),
        ('ObjectQuestion1', 'WP', 'VBZ', 'IN', 'PERSON'),
    ]
    matching_patterns = []

    for pattern in patterns:
        cursor = 1
        for node in parse_tree:
            check = ''
            if isinstance(node, nltk.tree.Tree):
                check = node._label
            elif isinstance(node, tuple):
                check = node[1]
            else:
                raise ValueError
            if check == pattern[cursor]:
                cursor += 1
                if cursor == len(pattern):
                    matching_patterns.append(pattern)
                    break

    return matching_patterns

WSD_bot = ChatBot(name='PyBot', read_only=False, logic_adapters=['chatterbot.logic.MathematicalEvaluation', 'chatterbot.logic.BestMatch'])
list_trainer = ListTrainer(WSD_bot)
corpus_trainer = ChatterBotCorpusTrainer(WSD_bot)
corpus_trainer.train('chatterbot.corpus.english')

list_trainer.train(
	["Hi, can I help you?",
    "I need to search for a Web Service",
    "What kind of web service?"
	])

while True:
	request = input('You: ')
	response = WSD_bot.get_response(request)
	parse_tree = analyze_nl_input(request)
	patterns = check_known_pattern(parse_tree)
	print (patterns)
	print('Bot: ',response)
#WSD_bot.get_response(input())