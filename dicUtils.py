import numpy as np
import MLETrain

START = 'START'
dic_e = {}
dic_q = {}
num_word_count = 0
unk_tsg_list = []


def create_dic(mle):
    dic = {}

    with open(mle) as file:
        for line in file:
            try:
                key, value = action(line)
                dic[key] = value
            except:
                continue

    return dic


def action(line):
    keys, value = line.split('\n')[0].split('\t')
    if keys == 'ALL':
        global num_word_count
        num_word_count = int(value)
        return
    elif '*UNK* ' in keys:
        split_keys = keys.split(' ')
        global unk_tsg_list
        unk_tsg_list.append(split_keys[1])
        return tuple(split_keys), int(value)

    elif ' ' in keys:
        split_keys = keys.split(' ')
        return tuple(split_keys), int(value)
    else:
        return keys, int(value)

def possible_tags(word, dic_e):
    tags = []
    word = word.lower()
    for key in dic_e.keys():
        w = key[0]
        if w == word:
            tags.append(key[1])

    return tags

def get_score(x, c, b, a):
    return np.log(MLETrain.compute_e(x, c, dic_e, dic_q)) + np.log(
        MLETrain.compute_q(dic_q, num_word_count, a, b, c, 0.9, 0.09, 0.001))
