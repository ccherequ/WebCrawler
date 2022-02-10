import json
import nltk
from nltk.stem import PorterStemmer
bp = 'ANALYST/'
import os
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from collections import Counter
from writeBack2File import writeBack2File

unique_links = set()
def stem(token):
    stemmer = PorterStemmer()
    return stemmer.stem(token)


def read_in(str_path):
    list_of_files = list()
    for entry in os.listdir(str_path):
        x = os.path.join(str_path,entry)
        for entry2 in os.listdir(x):
            final = os.path.join(x,entry2)
            list_of_files.append(final)
    return list_of_files


def tokenize(content):
    Tokenizer = RegexpTokenizer('[a-zA-Z\']{2,}') 
    tokens = Tokenizer.tokenize(content)
    return tokens


inverted_index = writeBack2File()

for entry in os.listdir(bp):
    x = os.path.join(bp, entry)
    for entry2 in os.listdir(x):
        final = os.path.join(x, entry2)  # file
        json_dict = make_json_dict(final)
        url = json_dict['url']
        unique_links.add(url)
        content = json_dict['content']
        encoding = json_dict['encoding']
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()
        tokens = tokenize(text)
        for i in range(len(tokens)):
            tokens[i] = stem(tokens[i])
        tokens_freq = Counter(tokens)
        for k,v in tokens_freq.items():
            inverted_index.addUrlToToken(k,url,v)

print("NUMBER OF INDEXED DOCUMENTS: "+ str(len(unique_links)))
print("NUMBER OF UNIQUE WORDS: "+str(len(inverted_index.data.keys())))
inverted_index.write()


        

        












