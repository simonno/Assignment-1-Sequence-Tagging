import sys
import numpy as np
import dicUtils
import MLETrain

START = 'START'
dic_e = {}
dic_q = {}
unk_tsg_list = []

def argmax(word, possible_tags_list, b, a):
    max_tag = possible_tags_list[0]
    max_prob = -np.math.inf
    for tag in possible_tags_list:
        prob = dicUtils.get_score(word, tag, b, a)
        if prob > max_prob:
            max_prob = prob
            max_tag = tag
    return max_tag

def greedy(input_file_name, greedy_hmm_output):
    tagged_text = ''

    with open(input_file_name, 'r') as input_file:

        for line in input_file:
            a = START
            b = START
            words = line.split('\n')[0].split(' ')

            for index in range(len(words)):
                word = words[index]
                tags = dicUtils.possible_tags(word.lower(), dic_e)

                if len(tags) == 0:
                    max_tag = argmax('*UNK*', unk_tsg_list, b, a)
                else:
                    max_tag = argmax(word.lower(), tags, b, a)

                a = b
                b = max_tag
                tagged_text += str(word) + '/' + str(max_tag) + ' '

            tagged_text.rstrip()
            tagged_text += '\n'

    with open(greedy_hmm_output, 'w') as output_file:
        output_file.write(tagged_text)


def main(input_file_name, q_mle, e_mle, greedy_hmm_output, extra_file_name):
    global dic_e, dic_q
    dic_e = dicUtils.create_dic(e_mle)
    dic_q = dicUtils.create_dic(q_mle)
    greedy(input_file_name, greedy_hmm_output)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
