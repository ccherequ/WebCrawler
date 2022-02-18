
import time
from collections import defaultdict
from nltk.stem import PorterStemmer
directory = "indices"

def stem(token):
    stemmer = PorterStemmer()
    return stemmer.stem(token)


def read_token_index()->dict:
    file = open("token_index.txt", "r")
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
    path = directory + "/" + initial + ".txt"
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
        return listx
    

    set1 = listx[0]
    for i in range(1,len(listx)):
        set2 = listx[i]
        set1 = set1.intersection(set2)
    return set1


def rank(doc_set,query,token_index):
    doc_freq = defaultdict(int)
    for word in query: 
        position = token_index[stem(word)]
        initial = word[0]
        if initial.isdigit():
            initial = "numeric"
        path = directory + "/" + initial + ".txt"
        file = open(path, "r")
        file.seek(position)
        file.readline()
        file.readline() 
        line = file.readline()
        while "#@" in line:
            line = line.split(',')
            if line[0] in doc_set:
                frequency = int(line[1])
                doc_freq[line[0]] += frequency
            line = file.readline()
    return doc_freq

def get


if __name__ == "__main__":
    index_of_index = read_token_index()


    query = ""
    while query== "":
        query = input("ENTER QUERY: ") 

    start_timer = time.time() #start timer
    query = query.split(" ")
    final_doc_ids = andquery(query)
    rank_dict = rank(final_doc_ids,query, index_of_index)
    top_n = 5
    i = 0
    for docid in sorted(rank_dict, key = rank_dict.get, reverse = True): 
        if i <= top_n:
            print(docid)
            i += 1
        
        

    i = 0 
    r = 5
    if r> len(rank_dict):
        r = len(rank_dict)


    with open('book_keeping.txt', 'a') as file:
            listx = file.readline()
    while i< r:
        doc = rank_dict[i][0] 
        line = listx[doc] 
        line = line.split(',')
        print(line[1])
        i+=1

    print("Search done in", time.time()-start_timer, "seconds")

