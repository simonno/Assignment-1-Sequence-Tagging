import sys
from datetime import datetime

import numpy as np

import MLETrain
from DictUtils import DictUtils
from FileUtils import FileUtils
from WordSignature import WordSignatures

START = 'START'
UNK = '*unk*'


def argmax(possible_tags_dict, prev_tag, prev_prev_tag, dict_q, dict_e):
    max_tag = ''
    max_prob = -np.math.inf
    for signature, tags in possible_tags_dict.items():
        for tag in tags:
            prob = MLETrain.get_score(signature, tag, prev_tag, prev_prev_tag, dict_q, dict_e)
            if prob > max_prob:
                max_prob = prob
                max_tag = tag
    return max_tag


def get_word_signatures_tag(word, dict_e, unk_tag_list):
    signatures = WordSignatures.get_word_signatures(word)
    if signatures == [word.lower()]:
        return {UNK: unk_tag_list}
    else:
        signatures_tags = dict()
        for signature in signatures:
            signatures_tags[signature] = DictUtils.possible_tags(signature, dict_e)
        return signatures_tags


def possible_tags(word, dict_e, unk_tag_list):
    words_tags = DictUtils.possible_tags(word, dict_e)
    if len(words_tags) == 0:
        return get_word_signatures_tag(word, dict_e, unk_tag_list)
    else:
        return {word: words_tags}


def get_tags(sentence, dict_q, dict_e, unk_tag_list):
    tagged_sentence = list()
    prev_prev_tag = START
    prev_tag = START

    for word in sentence.split(' '):
        tag = argmax(possible_tags(word, dict_e, unk_tag_list), prev_tag, prev_prev_tag, dict_q, dict_e)
        tagged_sentence.append((word, tag))
        prev_prev_tag = prev_tag
        prev_tag = tag

    print(tagged_sentence)
    return tagged_sentence


def greedy(sentences, dict_q, dict_e, unk_tag_list):
    tags = list()

    for sentence in sentences:
        tags.append(get_tags(sentence, dict_q, dict_e, unk_tag_list))

    return tags


def main(input_file_name, q_mle, e_mle, greedy_hmm_output, extra_file_name):
    start = datetime.now()
    sentences = FileUtils.read_lines(input_file_name)
    dict_q = DictUtils.convert_line_to_dict(FileUtils.read_lines(q_mle))
    dict_e = DictUtils.convert_line_to_dict(FileUtils.read_lines(e_mle))
    unk_tag_list = DictUtils.possible_tags(UNK, dict_e)
    tagged_text = greedy(sentences, dict_q, dict_e, unk_tag_list)
    FileUtils.write_tagged_text(greedy_hmm_output, tagged_text)
    end = datetime.now()
    print('Running Time: {0}'.format(end - start))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
