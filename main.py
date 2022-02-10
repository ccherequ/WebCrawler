import json
#data_struct = {{}}
import nltk
from nltk.stem import PorterStemmer
bp = 'TEST/'
import os
from bs4 import BeautifulSoup


def stem(token):
    stemmer = PorterStemmer()
    return stemmer.stem(token)


def read_json():
    with open("0a0056fb9a53ec6f190aa2b5fb1a97c33cd69726c8841f89d24fa5abd84d276c.json"
              , "r") as json_file:
        json_load = json.load(json_file)
    print(json_load)


def make_json_dict(file):
    with open(file,'r') as f:
        return json.load(f)


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


for entry in os.listdir(bp):
    x = os.path.join(bp, entry)
    for entry2 in os.listdir(x):
        final = os.path.join(x, entry2)  # file
        json_dict = make_json_dict(final)
        url = json_dict['url']
        content = json_dict['content']
        encoding = json_dict['encoding']
        soup = BeautifulSoup(content, 'html.parser')
        












