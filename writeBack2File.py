import json

class writeBack2File:
    def __init__(self):
        self.data = dict(dict())
    def addUrlToToken(self, token, url, frequency):
        if token in self.data:
            self.data[token][url] = frequency
        else:
            self.data[token] = dict()
            self.data[token][url] = frequency

    def write(self, dict):
        with open('report.txt', 'a') as file:
            file.write(json.dumps(dict))
            file.write("\n")

