
import time
from collections import defaultdict
#from typing import final
from nltk.stem import PorterStemmer
import json
from collections import Counter
import math
from query_set import return_positions
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
    if token not in token_index.keys():
        return set()
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
        return listx[0]

    set1 = listx[0]
    for i in range(1,len(listx)):
        set2 = listx[i]
        set1 = set1.intersection(set2)
    return set1


def query_tfidf(query, numDocs, doc_set, token_index):
    doc_nliz_list = []
    q_terms = []
    tf_wt = []
    nliz = []
    ls1 = [] 
    final_scores = dict()

    #######query 
    for i in query:  #stems
        word = stem(i)
        if word in token_index.keys():
            q_terms.append(word)

    # Calculate the scaling factor for docs that contain 2-grams
    two_gram_weight_scaling = {}
    for docid in doc_set:
        two_gram_weight_scaling[docid] = 1
    if len(q_terms) > 1:
        two_gram_list = []
        counter = 0
        while counter < len(q_terms) - 1:
            two_gram = q_terms[counter] + q_terms[counter + 1]
            two_gram_list.append(two_gram)
            counter += 1
        two_grams = Counter(two_gram_list)
        two_gram_docs = {}
        for i in two_grams.keys():
            tg_set = return_docids(i, token_index)
            two_gram_docs[i] = tg_set
        for docid in doc_set:
            for k,v in two_gram_docs.items():
                if docid in v:
                    two_gram_weight_scaling[docid] += 0.05  # Sets the weight to +10% for every 2-gram
    # finish 2-gram scaling

    # Relative distance of terms from each other in query
    
    if len(q_terms) > 1:
        query_term_distance = []
        c1 = 0
        while c1 < len(q_terms):
            term = q_terms[c1]
            temp_list = [term]
            c2 = c1 + 1
            while c2 < len(q_terms):
                t2 = q_terms[c2]
                dist = c2 - c1
                temp_tup = (t2, dist)
                temp_list.append(temp_tup)
                c2 += 1
            query_term_distance.append(temp_list)
            c1 += 1
    # finish relative distances

    q_terms = Counter(q_terms) #query frequency dict
    for k, v in q_terms.items():
        tf_wt.append([k, (1 + math.log(v, 10))])
    wt_list = []
    num_docs_containing_term = []
    for k,v in q_terms.items():  #build weight list
        setx = return_docids(k, token_index)
        num_docs_containing_term.append((len(setx), k))
        wt = math.log(numDocs/len(setx)) * q_terms[k]
        wt_list.append(wt)
    for i in wt_list: #build nliz 
        ls1.append(i * i)
    list_sum = 0
    for i in ls1:
        list_sum += i
    sum_root = math.sqrt(list_sum)
    for  i in wt_list:
        nliz.append(i/sum_root)

    num_docs_containing_term = sorted(num_docs_containing_term)
    importance = []
    for i in num_docs_containing_term:
        importance.append(i[1])

    term_positions_list = []
    for t in q_terms.keys():
        l = [t]
        term_positions_list.append(l)

    doc_nlize_dict = defaultdict(list)
    count = 0
    new_doc_set = set()
    importance_count = 0
    while importance_count < len(importance):
        k = importance[importance_count]
        position = token_index[k]
        initial = k[0]
        if initial.isdigit():
            initial = "numeric"
        path = directory + "/" + initial + ".txt"
        file = open(path, "r")
        file.seek(position)
        file.readline()
        file.readline()
        line = file.readline()
        if importance_count == 0:
            while "#@" in line:
                line = line.split('||')
                docid = int(line[0])
                doc_nlize = float(line[1])
                #positions_list = return_positions(k, docid, token_index)
                if len(doc_nlize_dict[k]) >= 100:
                    smallest = doc_nlize_dict[k][0][1]
                    counter = 1
                    while counter < len(doc_nlize_dict[k]):
                        if doc_nlize_dict[k][counter][1] > smallest:
                            smallest = doc_nlize_dict[k][counter][1]
                        counter += 1
                    for i in range(len(doc_nlize_dict[k])):
                        if doc_nlize_dict[k][i][1] > doc_nlize:
                            del doc_nlize_dict[k][i]
                            new_doc_set.remove(doc_nlize_dict[k][i][0])
                            new_doc_set.add(docid)
                            doc_nlize_dict[k].append([docid, doc_nlize])
                            line = file.readline()
                            break
                else:
                    doc_nlize_dict[k].append([docid, doc_nlize])
                    new_doc_set.add(docid)
                    line = file.readline()
        else:
            while '#@' in line:
                if docid in new_doc_set:
                    doc_nlize_dict[k].append([docid, doc_nlize])
                line = file.readline()
        importance_count += 1
                #pos_tup = (docid, positions_list)
                #term_positions_list[count].append(pos_tup)
        count += 1
    print(new_doc_set)
    for k,v in doc_nlize_dict.items():
        print(k, ' : ', v)
    smallest_term = list(doc_nlize_dict.keys())[0]
    small = len(doc_nlize_dict[smallest_term])
    smallest_list = []
    #for i in doc_nlize_dict[smallest_term]:
    counter = 0
    while counter < len(doc_nlize_dict[smallest_term]):
        smallest_list.append(doc_nlize_dict[smallest_term][counter][0])
        counter += 1
    for k,v in doc_nlize_dict.items():
        if len(v) < small:
            small = len(v)
            smallest_term = k
            counter = 0
            while counter < len(doc_nlize_dict[smallest_term]):
                smallest_list.append(doc_nlize_dict[smallest_term][counter][0])
                counter += 1

    intersect = []

    if len(q_terms.keys()) > 1:
        for k,v in doc_nlize_dict.items():
            if k != smallest_term:
                for pair in v:
                    if pair[0] in smallest_list and pair[0] not in intersect:
                        intersect.append(pair[0])
        for k,v in doc_nlize_dict.items():
            c1 = 0
            while c1 < len(doc_nlize_dict[k]):
                if doc_nlize_dict[k][c1][0] not in intersect:
                    del doc_nlize_dict[k][c1]
                c1 += 1
    else:
        for k,v in doc_nlize_dict.items():
            for post in v:
                if post[0] not in intersect:
                    intersect.append(post[0])
    """
    for docid in doc_set:
        for relative_dist in query_term_distance:
            q_rel_dists = []
            q_term = relative_dist[0]
            counter = 1
            while counter < len(relative_dist):
                q_rel_dists.append(relative_dist[counter])
                counter += 1
            if len(q_rel_dists) > 0:
                for doc_dist in term_positions_list:
                    doc_rel_dists = []
                    doc_term = doc_dist[0]
                    if doc_term != q_term:

                # ['car', , ('auto', 1), ('insur', 2), ('car', 3)]
                # query_term_positions = (docid, [pos])
                # t1
                # term_positions = query_term_positions[1]

                # for every other entry
                #   t2
                #   other_qterm_positions = (docid, [pos])
                #   other_positions = other_qterm_positions[1]

                #   [15,33]    [20]

                #   c1 = 0
                #   while c1 < len(term_positions)
                #       c2 = 0
                #       while c2 < len(other_positions)
                #           if term_positions[c1] < other_positions[c2]
                #               for tup in query_term_distance
                #                   if tup[0] == t2:
                #                       dist = tup[1]
                #               if other_position[c2] - term_position[c1] == dist:
                #                   true
                #           c2 += 1
                #       c1 += 1
                for doc_dist in term_positions_list:
                    doc_rel_dists = []
                    doc_term = doc_dist[0]
                    if doc_term == q_term:
                        c = 1
                        while counter < len(doc_dist):
                            doc_rel_dists.append(doc_dist[c])
                """
    
    for docid in new_doc_set:
        doc_nliz_list = []
        sum = 0 
        
        for term in q_terms.keys():
            for x,y in doc_nlize_dict[term]: 
                if x == docid: 
                    doc_nliz_list.append(y)
        
        i = 0 
        #start_timer2 = time.time() #start timer
        while i!= len(nliz):
            sum += nliz[i]* -(doc_nliz_list[i]) 
            i+=1
        final_scores[docid] = sum * two_gram_weight_scaling[docid]
        #print("For done in", time.time()-start_timer2, "seconds")
    
    return final_scores

"""
def rank(doc_set,query,token_index):
    doc_freq = dict()
    for id in doc_set:
        doc_freq[id] = 0
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
            frequency = int(line[1])
            docid = int(line[0])
            if docid in doc_set:
                doc_freq[docid] += frequency
            line = file.readline()
    return doc_freq

"""


if __name__ == "__main__":
    index_of_index = read_token_index()
    with open('book_keeping.txt','r') as file:
        url_docid_dict = json.load(file)
        file.close()

    query = ""
    while query== "":
        query = input("ENTER QUERY: ") 

    start_timer = time.time() #start timer
    query = query.split(" ")
    final_doc_ids = andquery(query)
    rank_dict = query_tfidf(query,len(url_docid_dict),final_doc_ids,index_of_index)
    top_n = 5
    i = 0
    for docid in sorted(rank_dict, key = rank_dict.get, reverse = False):
        if i < top_n:
            print(url_docid_dict[str(docid)])
            i += 1
    print("Search done in", time.time()-start_timer, "seconds")

