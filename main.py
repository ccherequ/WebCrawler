import json
import nltk
from nltk.stem import PorterStemmer
bp = 'ANALYST/'
import os
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from collections import Counter
from writeBack2File import writeBack2File

unique_links_dict = dict()
unique_links_set = set()
counter = 0
def stem(token):
    stemmer = PorterStemmer()
    return stemmer.stem(token)

def tokenize(content):
    Tokenizer = RegexpTokenizer('[a-zA-Z\']{2,}') 
    tokens = Tokenizer.tokenize(content)
    return tokens


def make_json_dict(file):
    with open(file,'r') as f:
        return json.load(f)


def writeURLDict():
    with open('book_keeping.txt', 'a') as file:
        for key, val in unique_links_dict.items():
            file.write(key, ' , ', val)
            file.write("\n")


inverted_index = writeBack2File()

for entry in os.listdir(bp):
    x = os.path.join(bp, entry)
    for entry2 in os.listdir(x):
        final = os.path.join(x, entry2)  # file
        json_dict = make_json_dict(final)
        url = json_dict['url']
        if url not in unique_links_set:
            unique_links_set.add(url)
            unique_links_dict[counter] = url
            counter += 1
        content = json_dict['content']
        encoding = json_dict['encoding']
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()
        tokens = tokenize(text)
        for i in range(len(tokens)):
            tokens[i] = stem(tokens[i])
        tokens_freq = Counter(tokens)
        for k,v in tokens_freq.items():
            inverted_index.addUrlToToken(k,counter,v)


print("NUMBER OF INDEXED DOCUMENTS: "+ str(len(unique_links_set)))
print("NUMBER OF UNIQUE WORDS: "+str(len(inverted_index.data.keys())))

inverted_index.write()


        

        












