import numpy as np

START = 'START'
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

    return dic, num_word_count, unk_tsg_list


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


def possible_tags(dic_e, word):
    tags = []
    word = word.lower()
    for key in dic_e.keys():
        w = key[0]
        if w == word:
            tags.append(key[1])

    return tags


def get_score(dic_e, dic_q, words_count, x, c, b, a):
    return np.log(compute_e(dic_e, dic_q, x, c)) + np.log(compute_q(dic_q, words_count, a, b, c, 0.9, 0.09, 0.01))


def compute_q(dic_q, words_count, a=' ', b=' ', c=' ', lr1=0.0, lr2=0.0, lr3=0.0):
    return lr1 * (dic_q.get((a, b, c), 0) / dic_q.get((a, b), 1)) + lr2 * (
            dic_q.get((b, c), 0) / dic_q.get(b, 1)) + lr3 * (dic_q.get(c, 0) / words_count)


def compute_e(dic_e, dic_q, x, y):
    return dic_e.get((x, y), 0) / dic_q.get(y, 1)
