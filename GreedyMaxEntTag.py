import pickle
import sys
from datetime import datetime

import numpy as np

from Utils.DictUtils import DictUtils
from Utils.FeaturesUtils import FeaturesUtils
from Utils.FileUtils import FileUtils


def create_features_numeric_format(word_features, features_map):
    numeric_format_vector = np.zeros(len(features_map.items()))
    for feature_key, feature_value in word_features.items():
        feature = '{0}={1}'.format(feature_key, feature_value)
        if feature in features_map.keys():
            numeric_format_vector[features_map[feature]] = 1
    return numeric_format_vector


def get_prediction_of_word(word_features, clf, feature_map):
    # clf works only on numbers format
    features_numeric_format = create_features_numeric_format(word_features, feature_map)
    predict = clf.predict([features_numeric_format.tolist()])[0]
    return predict


def get_tags_of_sentence(sentence, features_map, counters_dict, clf):
    predictions = list()
    words_list = sentence.split()
    for i in range(len(words_list)):
        word_features = FeaturesUtils.get_word_features(i, words_list, predictions,
                                                        DictUtils.is_rare(counters_dict, words_list[i]))
        predictions.append(get_prediction_of_word(word_features, clf, features_map))

    return [(word, prediction) for word, prediction in zip(words_list, predictions)]


def memm_greedy(sentences, features_map, counters_dict, clf):
    tags = list()

    for sentence in sentences:
        start = datetime.now()
        predictions = get_tags_of_sentence(sentence, features_map, counters_dict, clf)
        tags.append(predictions)
        end = datetime.now()
        print(predictions)
        print('Sentence Running Time: {0}'.format(end - start))
    return tags


def main(input_file_name, model_file, feature_map_file, out_file_name):
    start = datetime.now()
    sentences = FileUtils.read_lines(input_file_name)
    feature_map_lines = FileUtils.read_lines(feature_map_file)
    features_map, counters_dict = DictUtils.create_features_dicts(feature_map_lines)

    model_file = open(model_file, 'rb')
    (clf, vec) = pickle.load(model_file)

    tagged_text = memm_greedy(sentences, features_map, counters_dict, clf)
    FileUtils.write_tagged_text(out_file_name, tagged_text)
    end = datetime.now()
    print('Running Time: {0}'.format(end - start))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
