import json

class writeBack2File:
    def __init__(self):
        self.data = dict()
    def addUrlToToken(self, token, url, frequency):
        if token in self.data:
            self.data[token][url] = frequency
        else:
            self.data[token] = dict()
            self.data[token][url] = frequency

    def write(self):
        with open('report.txt', 'a') as file:
            file.write(json.dumps(self.data))
            file.write("\n")

