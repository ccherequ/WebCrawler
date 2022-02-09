import json
data_struct = {{}}
from nltk.stem import PorterStemmer
import json


def stem(token):
    stemmer = PorterStemmer()
    return stemmer.stem(token)

