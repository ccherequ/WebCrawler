import json
data_struct = {{}}
from nltk.stem import PorterStemmer


def stem(token):
    stemmer = PorterStemmer()
    return stemmer(token)
