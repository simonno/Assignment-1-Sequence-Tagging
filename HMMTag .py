import sys

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

    with open(input_file_name, 'r') as input_file:
        for line in input_file:
            words = line.split('\n')[0].split(' ')
            prev_tags = [START]
            prev_prev_tags = [START]
            v_table = {(0, START, START): 1}
            bq = {}
            for i in range(len(words)):
                w_i = words[i]
                possible_tags_w_i = dicUtils.possible_tags(dic_e, w_i)
                for r in possible_tags_w_i:
                    for t1 in prev_tags:
                        max_prob = 0
                        # max_prob = -np.math.inf
                        max_tag = t1
                        for t2 in prev_prev_tags:
                            prob = v_table.get((i, t2, t1)) * get_score(w_i, r, t1, t2)
                            if prob > max_prob:
                                max_prob = prob
                                max_tag = t2

                        v_table[(i + 1, t1, r)] = max_prob
                        bq[(i + 1, t1, r)] = max_tag

                prev_prev_tags = prev_tags
                prev_tags = possible_tags_w_i

            print(v_table)
            # for i in reversed(range(len(words))):
            #     for [r,t] in v_table[i]:
            #         for r in v_table[i][t]:


def main(input_file_name, q_mle, e_mle, hmm_viterbi_predictions, extra_file_name):
    global dic_q, dic_e, num_word_count, unk_tsg_list
    dic_e, num_word_count, unk_tsg_list = dicUtils.create_dic(e_mle)
    dic_q, _, _ = dicUtils.create_dic(q_mle)
    viterbi(input_file_name, hmm_viterbi_predictions)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
