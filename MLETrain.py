import sys
from datetime import datetime

from FileUtils import FileUtils

from DictUtils import DictUtils


def create_dicts(sentences):
    dict_q = dict()
    dict_e = dict()
    for sentence in sentences:
        DictUtils.insert_sentence_to_dicts(dict_q, dict_e, sentence)

    dict_e = DictUtils.convert_rare_words(dict_e)
    DictUtils.update_dict(dict_q, 'ALL', sum(dict_e.values()))
    return dict_q, dict_e


# def compute_q(dic, num_words_count, a=' ', b=' ', c=' ', lr1=0, lr2=0, lr3=0):
#     return lr1 * (dic.get((a, b, c), 0) / dic.get((a, b), 1)) + lr2 * (dic.get((b, c), 0) / dic.get(b, 1)) + lr3 * (
#             dic.get(c, 0) / num_words_count)
#
# def compute_e(x, y, dic_e_mle, dic_q_mle):
#     return dic_e_mle.get((x, y), 0) / dic_q_mle.get((y), 1)


def main(input_file_name, q_mle, e_mle):
    start = datetime.now()
    sentences = FileUtils.read_sentences(input_file_name)
    dict_q, dict_e = create_dicts(sentences)
    FileUtils.write_events_count(q_mle, dict_q)
    FileUtils.write_events_count(e_mle, dict_e)
    end = datetime.now()
    print('Running Time: {0}'.format(end - start))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
