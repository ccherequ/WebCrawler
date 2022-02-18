
import time
directory = "indices"

from nltk.stem import PorterStemmer


def stem(token):
    stemmer = PorterStemmer()
    return stemmer.stem(token)


def read_token_index()->dict:
    file = open("token_index", "r")
    result = dict()
    for line in file:
        line = line.split(",")
        result[line[0]] = int(line[1])
    return result


def return_docids(token:str, token_index:dict)->set:
    position = token_index[token]
    initial = token[0]
    if initial.isdigit():
        initial = "numeric"
    path = directory + "/" + initial
    file = open(path, "r")
    file.seek(position)
    file.readline()
    temp = file.readline().strip()
    file.close()
    return eval(temp)


def andquery(query):
    listx = list()
    for i in query: 
        word = stem(i)
        listx.append(return_docids(word,index_of_index))

    listx = sorted(listx, key = lambda x: len(x)) 
    if len(listx)==1:
        return listx[0]
    

    set1 = listx[0]
    for i in range(1,len(listx)):
        set2 = listx[i]
        set1 = set1.intersection(set2)

    return set1
    



index_of_index = read_token_index()


query = ""
while query== "":
    query = input("ENTER QUERY: ")
    start_clock = time.time()


query = query.split(" ")
final_doc_ids = andquery(query)
print(final_doc_ids)
print("Search done in", time.time()-start_clock, "seconds")





    



#####first we create a dictionary to hold token: set fo
    











