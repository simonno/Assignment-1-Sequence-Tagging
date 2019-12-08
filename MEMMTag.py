import sys
from datetime import datetime

import numpy as np
from scipy import sparse

from DictUtils import DictUtils
from FeaturesUtils import FeaturesUtils
from FileUtils import FileUtils

START = 'START'


def get_words(sentence):
    return sentence.split(' ')


def create_features_numeric_format(all_word_features, features_map):
    col = list()
    row = list()
    data = list()
    for i in range(len(all_word_features)):
        word_features = all_word_features[i]
        for feature_key, feature_value in word_features.items():
            feature = '{0}={1}'.format(feature_key, feature_value)
            if feature in features_map.keys():
                row.append(i)
                col.append(features_map[feature])
                data.append(1)
    return sparse.csr_matrix((data, (row, col)), shape=(len(all_word_features), len(features_map.items())))


def get_predict_prob_of_word(all_word_features, clf, feature_map):
    numeric_format_matrix = create_features_numeric_format(all_word_features, feature_map)
    predict_probabilities = clf.predict_proba(numeric_format_matrix)
    return predict_probabilities


def max_prob_and_tag(v_table, i, prev_prediction, prev_prev_predictions, predict_probabilities, prob_index):
    max_prob = -np.inf
    max_tag = prev_prev_predictions[0]
    for prev_prev_prediction, probs in zip(prev_prev_predictions, predict_probabilities):
        prob = v_table[(i - 1, prev_prev_prediction, prev_prediction)] + probs[prob_index]
        if prob > max_prob:
            max_prob = prob
            max_tag = prev_prev_prediction

    return max_prob, max_tag


def calc_v_table_at_i(v_table, bq, i, tuples_dict):
    for key in tuples_dict.keys():
        tag = key[0]
        prev_prediction = key[1]
        prev_prev_prediction = key[2]
        if (i - 1, prev_prev_prediction, prev_prediction) not in v_table:
            continue

        score = v_table[(i - 1, prev_prev_prediction, prev_prediction)] * tuples_dict[key]

        if (i, prev_prediction, tag) not in v_table or v_table[(i, prev_prediction, tag)] < score:
            v_table[(i, prev_prediction, tag)] = score
            bq[(i, prev_prediction, tag)] = prev_prev_prediction


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


def get_tag_list(index, prev_predictions, prev_prev_predictions):
    tags_list = list()
    tags_list.append(prev_prev_predictions)
    tags_list.append(prev_predictions)
    for i in range(index - 1):
        tags_list.insert(0, '')
    return tags_list


def get_word_features_list(i, words, prev_predictions, prev_prev_predictions, counters_dict):
    all_word_features = list()
    prev_list = list()
    for prev_prediction in prev_predictions:
        for prev_prev_prediction in prev_prev_predictions:
            word_features = FeaturesUtils.get_word_features(i, words,
                                                            get_tag_list(i, prev_prediction, prev_prev_prediction),
                                                            DictUtils.is_rare(counters_dict, words[i]))
            all_word_features.append(word_features)
            prev_list.append((prev_prediction, prev_prev_prediction))
    return all_word_features, prev_list


def get_best_tuples(tuples_dict, num_of_best_items=50):
    best_tuples_dict = dict()
    for best_item in sorted(tuples_dict.items(), key=lambda item: item[1], reverse=True)[:num_of_best_items]:
        best_tuples_dict[best_item[0]] = best_item[1]

    return best_tuples_dict


def get_tuples_dict(i, words, prev_predictions, prev_prev_predictions, counters_dict, clf, features_map, classes):
    tuples_dict = dict()
    all_word_features, prev_list = get_word_features_list(i, words, prev_predictions, prev_prev_predictions, counters_dict)
    predict_probabilities = get_predict_prob_of_word(all_word_features, clf, features_map)

    for (prev_prediction, prev_prev_prediction), probs in zip(prev_list, predict_probabilities):
        for tag, prob in zip(classes, probs):
            tuples_dict[(tag, prev_prediction, prev_prev_prediction)] = prob

    return get_best_tuples(tuples_dict, 50)
    # return tuples_dict


def viterbi(sentences, features_map, counters_dict, clf, classes):
    tagged_text = list()
    for sentence in sentences:
        words = get_words(sentence)

        v_table = {(-1, START, START): 1}
        bq = dict()
        prev_predictions = [START]
        prev_prev_predictions = [START]
        start = datetime.now()

        for i in range(len(words)):
            tuples_dict = get_tuples_dict(i, words, prev_predictions, prev_prev_predictions, counters_dict, clf,
                                          features_map, classes)

            calc_v_table_at_i(v_table, bq, i, tuples_dict)

            prev_predictions = list()
            prev_prev_predictions = list()
            for tuple in tuples_dict.keys():
                if tuple[0] not in prev_predictions:
                    prev_predictions.append(tuple[0])
                if tuple[1] not in prev_prev_predictions:
                    prev_prev_predictions.append(tuple[1])

        tagged_line = get_backtrack(v_table, bq, words)

        print(tagged_line)
        end = datetime.now()
        print('{1} - Running Time: {0}'.format(end - start, sentences.index(sentence)))
        print()

        tagged_text.append(tagged_line)
    return tagged_text


def main(input_file_name, model_file_name, feature_map_file, output_file_name):
    start = datetime.now()

    clf, vec = FileUtils.read_logistic_regression_model(model_file_name)
    classes = clf.classes_.tolist()
    sentences = FileUtils.read_lines(input_file_name)
    feature_map_lines = FileUtils.read_lines(feature_map_file)
    features_map, counters_dict = DictUtils.create_features_dicts(feature_map_lines)

    tagged_text = viterbi(sentences, features_map, counters_dict, clf, classes)
    FileUtils.write_tagged_text(output_file_name, tagged_text)

    end = datetime.now()
    print('Running Time: {0}'.format(end - start))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
