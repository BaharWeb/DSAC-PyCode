# f=open('jp3_57.txt','r')
# filedata=f.read()
# f.close()
# newdata=filedata.replace("  "," ")
# f=open('jp3_57.txt','w')
# f.write(newdata)
# f.close()

import io
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))
file1 = open("paper.txt")
line = file1.read()
words = line.split()
for r in words:
	if not r in stop_words:
		appendFile = open('test1.txt','a')
		appendFile.write(" "+r)

# folder = ['/Users/baharehzarei/Desktop/pdftotext 1/1.txt', '/Users/baharehzarei/Desktop/pdftotext 1/2.txt']
# with open('/Users/baharehzarei/Desktop/pdftotext 1/merged.txt', 'a') as outfile:
#     for file in folder:
#         with open(file) as newfile:
#             for line in newfile:
#                 outfile.write(line)
