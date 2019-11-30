import sys

import numpy as np

import dicUtils

START = 'START'
dic_e = {}
dic_q = {}
num_word_count = 0
unk_tsg_list = []


def get_score(word, tag, prev_tag, prev_prev_tag):
    return dicUtils.compute_e(dic_e, dic_q, word, tag) * dicUtils.compute_q(dic_q, num_word_count, prev_prev_tag,
                                                                            prev_tag, tag, 0.9, 0.09, 0.01)


def viterbi(input_file_name, hmm_viterbi_predictions):
    # Y = []

    with open(input_file_name, 'r') as input_file, open(hmm_viterbi_predictions, 'w') as output_file:
        for line in input_file:
            words = line.split('\n')[0].split(' ')
            prev_tags = [START]
            prev_prev_tags = [START]
            v_table = {(0, START, START): 1}
            bq = {}
            for i in range(1, len(words) + 1):
                w_i = words[i - 1]
                possible_tags_w_i = dicUtils.possible_tags(dic_e, w_i)
                for r in possible_tags_w_i:
                    for t1 in prev_tags:
                        max_prob = -np.math.inf
                        max_tag = t1
                        for t2 in prev_prev_tags:
                            if i == 1 and t1 == START and t2 == START:
                                prob = 1
                            else:
                                prob = v_table.get((i - 1, t2, t1)) * get_score(w_i, r, t1, t2)
                            if prob > max_prob:
                                max_prob = prob
                                max_tag = t2

                        v_table[(i, t1, r)] = max_prob
                        bq[(i, t1, r)] = max_tag

                prev_prev_tags = prev_tags
                prev_tags = possible_tags_w_i

            n = len(words)
            possible_tags_w_i = dicUtils.possible_tags(dic_e, words[-1])
            prev_tags = dicUtils.possible_tags(dic_e, words[-2])
            y_n = ''
            y_n_1 = ''
            max_prob = -np.math.inf
            for r in possible_tags_w_i:
                for t in prev_tags:
                    prob = v_table.get((n, t, r))
                    if max_prob < prob:
                        max_prob = prob
                        y_n = r
                        y_n_1 = t

            tagged_line = '{0}/{1} {2}/{3}\n'.format(words[-2], y_n_1, words[-1], y_n)
            for i in reversed(range(1, n - 1)):
                y_i = bq[(i + 2, y_n_1, y_n)]
                tagged_line = '{0}/{1} {2}'.format(words[i], y_i, tagged_line)
                y_n = y_n_1
                y_n_1 = y_i

            print(tagged_line)
            output_file.write(tagged_line)


def main(input_file_name, q_mle, e_mle, hmm_viterbi_predictions, extra_file_name):
    global dic_q, dic_e, num_word_count, unk_tsg_list
    dic_e, num_word_count, unk_tsg_list = dicUtils.create_dic(e_mle)
    dic_q, _, _ = dicUtils.create_dic(q_mle)
    viterbi(input_file_name, hmm_viterbi_predictions)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
