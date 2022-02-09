import json
#data_struct = {{}}
from nltk.stem import PorterStemmer


def stem(token):
    stemmer = PorterStemmer()
    return stemmer.stem(token)


def read_json():
    with open("0a0056fb9a53ec6f190aa2b5fb1a97c33cd69726c8841f89d24fa5abd84d276c.json"
              , "r") as json_file:
        json_load = json.load(json_file)
    print(json_load)
