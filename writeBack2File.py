import json
from Posting import Posting

class writeBack2File:
    def __init__(self):
        self.data = dict()
    def addUrlToToken(self, token, docid, fre):
        P = Posting(docid, fre, 0)
        if token in self.data:
            self.data[token].append(P)
        else:
            self.data[token] = list()
            self.data[token].append(P)

    def write(self):
        with open('report.txt', 'a') as file:
            for token,lists in self.data.items():
                file.write(token + ",")
                for posting in lists:
                    file.write(str(posting.docid))
                    file.write(", ")
                    file.write(str(posting.tfidf))
                    file.write(", ")
                    file.write(str(posting.fields))
                    file.write("\n")
                #file.write("\n")


if __name__ == "__main__":
    w = writeBack2File()
    w.addUrlToToken("you", "356", "63")
    w.addUrlToToken("you", "123", "7")
    w.addUrlToToken("he", "356", "56")
    w.write()
