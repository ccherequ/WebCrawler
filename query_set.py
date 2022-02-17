
directory = "indices"

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
    print(temp)
    file.close()
    return set(temp)


if __name__ == "__main__":
    d = read_token_index()
    print(return_docids("bren", d))
    