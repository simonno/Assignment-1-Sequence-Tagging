import pickle
import sys
from datetime import datetime

import numpy as np

from Utils.DictUtils import DictUtils
from Utils.FeaturesUtils import FeaturesUtils
from Utils.FileUtils import FileUtils
from Utils.WordSignature import WordSignatures

START = 'START'
UNK = '*unk*'


def get_words(sentence):
    return sentence.split(' ')


def create_features_numeric_format(word_features, features_map):
    numeric_format_vector = np.zeros(len(features_map.items()))
    for feature_key, feature_value in word_features.items():
        feature = '{0}={1}'.format(feature_key, feature_value)
        if feature in features_map.keys():
            numeric_format_vector[features_map[feature]] = 1
    return numeric_format_vector


def get_predict_prob_of_word(word_features, clf, feature_map):
    # clf works only on numbers format
    features_numeric_format = create_features_numeric_format(word_features, feature_map)
    predict_prob = clf.predict_log_prob([features_numeric_format.tolist()])[0]
    return predict_prob


def max_prob_and_tag(v_table, i, words_list, prev_prediction, prev_prev_predictions, counters_dict, clf, features_map):
    max_prob = -np.inf
    max_tag = prev_prev_predictions[0]
    for prev_prev_prediction in prev_prev_predictions:
        word_features = FeaturesUtils.get_word_features(i, words_list, [prev_prev_prediction, prev_prediction],
                                                        DictUtils.is_rare(counters_dict, words_list[i]))

        predict_prob = get_predict_prob_of_word(word_features, clf, features_map)
        prob = v_table[(i - 1, prev_prev_prediction, prev_prediction)] + predict_prob
        if prob > max_prob:
            max_prob = prob
            max_tag = prev_prev_prediction

    return max_prob, max_tag


def calc_v_table_at_i(v_table, bq, i, words_list, possible_prediction_dict, prev_predictions, prev_prev_predictions,
                      counters_dict, clf, features_map):
    for word, tags in possible_prediction_dict.items():
        for tag in tags:
            for prev_prediction in prev_predictions:
                max_prob, max_tag = max_prob_and_tag(v_table, i, words_list, prev_prediction, prev_prev_predictions,
                                                     counters_dict, clf, features_map)
                v_table[(i, prev_prediction, tag)] = max_prob
                bq[(i, prev_prediction, tag)] = max_tag


def get_backtrack(v_table, bq, words):
    n = len(words) - 1
    y_n = ''
    y_n_1 = ''
    max_prob = -np.math.inf

    for key, value in v_table.items():
        if key[0] == n and max_prob < value:
            max_prob = value
            y_n = key[2]
            y_n_1 = key[1]

    if n == 0:
        tagged_line = [(words[-1], y_n)]
    else:
        tagged_line = [(words[-2], y_n_1), (words[-1], y_n)]
        for i in reversed(range(n - 1)):
            y_i = bq[(i + 2, y_n_1, y_n)]
            tagged_line.insert(0, (words[i], y_i))
            y_n = y_n_1
            y_n_1 = y_i

    return tagged_line


def get_word_signatures_tag(word, dict_e, unk_tag_list):
    signatures = WordSignatures.get_word_signatures(word)
    if signatures == [word.lower()]:
        return {UNK: unk_tag_list}
    else:
        signatures_tags = dict()
        for signature in signatures:
            signatures_tags[signature] = DictUtils.possible_tags(signature, dict_e)
        return signatures_tags


def possible_tags(word, word_tag_dict, unk_tag_list):
    words_tags = word_tag_dict[word.lower()]
    words_tags = DictUtils.possible_tags(word, dict_e)

    if len(words_tags) == 0:
        return get_word_signatures_tag(word, word_tag_dict, unk_tag_list)
    else:
        return {word: words_tags}


def viterbi(sentences, features_map, counters_dict, word_tag_dict, unk_tag_list, clf):
    tagged_text = list()
    for sentence in sentences:
        words = get_words(sentence)

        v_table = {(-1, START, START): 1}
        bq = dict()
        prev_predictions = [START]
        prev_prev_predictions = [START]
        for i in range(len(words)):
            possible_prediction_dict = possible_tags(words[i], word_tag_dict, unk_tag_list)
            calc_v_table_at_i(v_table, bq, i, words, possible_prediction_dict, prev_predictions, prev_prev_predictions,
                              counters_dict, clf, features_map)

            prev_prev_predictions = prev_predictions
            prev_predictions = []
            for list_tags in possible_prediction_dict.values():
                prev_predictions += list_tags

        tagged_line = get_backtrack(v_table, bq, words)

        print(tagged_line)
        tagged_text.append(tagged_line)
    return tagged_text


def main(input_file_name, model_file_name, feature_map_file, output_file_name):
    start = datetime.now()

    sentences = FileUtils.read_lines(input_file_name)
    feature_map_lines = FileUtils.read_lines(feature_map_file)
    features_map, counters_dict, word_tag_dict, unk_tag_list = DictUtils.create_features_dicts(feature_map_lines)

    model_file = open(model_file_name, 'rb')
    (clf, vec) = pickle.load(model_file)
    tagged_text = viterbi(sentences, features_map, counters_dict, word_tag_dict, unk_tag_list, clf)
    FileUtils.write_tagged_text(output_file_name, tagged_text)
    end = datetime.now()
    print('Running Time: {0}'.format(end - start))

    end = datetime.now()
    print('Running Time: {0}'.format(end - start))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
