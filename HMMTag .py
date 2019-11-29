import dicUtils
import sys
import numpy as np

dic_e = {}
dic_q = {}
START = 'START'
v_table = []
bp = [] # pointers

def getScore(word,tag,prev_tag,prev_prev_tag):
    pass

def argmax(i, word, possible_tags_list, possible_prev_tags_list, possible_prev_prev_tags_list):
    max_tag = possible_tags_list[0]
    max_prob = -np.math.inf
    for tag, prev_tag in possible_tags_list:
        for prev_tag in possible_prev_tags_list:
            for prev_prev_tag in possible_prev_tags_list:
                prob = v_table[i-1][prev_prev_tag][prev_tag]*getScore(word, tag, prev_tag, prev_prev_tag)
                if prob > max_prob:
                    max_prob = prob
                    max_tag = tag
    return max_tag

def viterbi(input_file_name, hmm_viterbi_predictions):
    global v_table
    with open(input_file_name, 'r') as input_file:
        for line in input_file:
            a = START
            b = START
            words = line.split('\n')[0].split(' ')
            i=2
            for i in range(len(words)):
                word = words[i]
                prev_word = words[i-1]
                tags = dicUtils.possible_tags(word.lower(), dic_e)
                prev_tags = dicUtils.possible_tags(prev_tags.lower(), dic_e)
                v_table[line][i][] = argmax(i, word, tags, prev_tags, a)
                bp =



def main(input_file_name, q_mle, e_mle, hmm_viterbi_predictions, extra_file_name):
    global dic_e, dic_q
    dic_e = dicUtils.create_dic(e_mle)
    dic_q = dicUtils.create_dic(q_mle)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
