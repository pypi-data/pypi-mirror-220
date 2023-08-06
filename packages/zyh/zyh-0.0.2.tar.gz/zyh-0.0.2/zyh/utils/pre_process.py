def word2id(dictionary)->dict:
    dic = dict()
    for i in dictionary:
        dic[dictionary[i]] = i
    return dic
