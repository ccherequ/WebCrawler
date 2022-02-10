import json
from collections import defaultdict

class writeBack2File:
    def __init__(self):
        self.data = defaultdict(list)
    def addUrlToToken(self, token, url, frequency):
        # posting = Posting(token, url, frequency)
        #self.data[token].append(posting)
        if token in self.data:
            self.data[token][url] = frequency
        else:
            self.data[token] = dict()
            self.data[token][url] = frequency

    def write(self):
        with open('report.txt', 'a') as file:
            file.write(json.dumps(self.data))
            file.write("\n")

