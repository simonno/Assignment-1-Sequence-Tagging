import sys
from datetime import datetime

import numpy as np

from DictUtils import DictUtils
from FileUtils import FileUtils
from MathUtils import MathUtils


def create_dicts(sentences):
    dict_q = dict()
    dict_e = dict()
    for sentence in sentences:
        DictUtils.insert_sentence_to_dicts(dict_q, dict_e, sentence)

    dict_e = DictUtils.convert_rare_words(dict_e)
    DictUtils.update_dict(dict_q, 'ALL', sum(dict_e.values()))
    return dict_q, dict_e


def compute_q(dict_q, tag, prev_tag, prev_prev_tag, lr1=0.90, lr2=0.09, lr3=0.01):
    if lr1 + lr2 + lr3 != 1.0:
        raise Exception('summing factors should be 1 !!!')

    prob1 = MathUtils.calc_fraction(DictUtils.get_value(dict_q, (tag, prev_tag, prev_prev_tag)),
                                    DictUtils.get_value(dict_q, (prev_tag, prev_prev_tag)))
    prob2 = MathUtils.calc_fraction(DictUtils.get_value(dict_q, (tag, prev_tag)),
                                    DictUtils.get_value(dict_q, prev_tag))
    prob3 = MathUtils.calc_fraction(DictUtils.get_value(dict_q, tag),
                                    DictUtils.get_value(dict_q, 'ALL'))

    return lr1 * prob1 + lr2 * prob2 + lr3 * prob3


def compute_e(word, tag, dict_q, dict_e):
    counter = DictUtils.get_value(dict_e, (word, tag))
    denominator = DictUtils.get_value(dict_q, tag)
    return MathUtils.calc_fraction(counter, denominator)


def get_score(word, tag, prev_tag, prev_prev_tag, dict_q, dict_e):
    return np.log(compute_q(dict_q, tag, prev_tag, prev_prev_tag)) + np.log(compute_e(word, tag, dict_q, dict_e))


def main(input_file_name, q_mle, e_mle):
    start = datetime.now()
    sentences = FileUtils.read_lines(input_file_name)
    dict_q, dict_e = create_dicts(sentences)
    FileUtils.write_events_count(q_mle, dict_q)
    FileUtils.write_events_count(e_mle, dict_e)
    end = datetime.now()
    print('Running Time: {0}'.format(end - start))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
