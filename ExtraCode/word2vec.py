import gensim
from gensim.models import word2vec
import logging
import pprint


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sen=gensim.models.word2vec.LineSentence('./test1.txt')
model = word2vec.Word2Vec(sen, size=300, min_count=3)
model.save('./newmodel.model')