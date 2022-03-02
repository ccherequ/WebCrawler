import json
from Posting import Posting
directory = "indices"
class writeBack2File:
    def __init__(self):
        self.data = dict()
        self.token_docid = dict()
    def addUrlToToken(self, token, docid, fre, positions):
        P = Posting(docid, fre, positions)
        if token in self.data:
            self.data[token].append(P)
            self.token_docid[token].add(docid)
        else:
            self.data[token] = list()
            self.data[token].append(P)
            self.token_docid[token] = set()
            self.token_docid[token].add(docid)

    def write(self):
        for token,lists in self.data.items():
            initial = token[0]
            if initial.isdigit():
                initial = "numeric"
            path = directory + "/" + initial + ".txt"

            with open(path, 'a') as file:
                token_file = open("token_index.txt", "a")
                token_file.write(token + "," + repr(file.tell()) + "\n")
                token_file.close()

                file.write(token + "\n") 
                file.write(str(self.token_docid[token]))
                file.write("\n")
                for posting in lists:
                    file.write(str(posting.docid))
                    file.write(",")
                    file.write(str(posting.tfidf))
                    file.write(",")
                    file.write(str(posting.fields))
                    file.write(",#@\n")
                file.close()





if __name__ == "__main__":
    w = writeBack2File()
    w.addUrlToToken("you", "356", "63")
    w.addUrlToToken("you", "123", "7")
    w.addUrlToToken("he", "356", "56")
    w.write()
