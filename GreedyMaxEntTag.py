import sys
from datetime import datetime

from scipy import sparse

from Utils.DictUtils import DictUtils
from Utils.FeaturesUtils import FeaturesUtils
from Utils.FileUtils import FileUtils


def create_features_numeric_format(all_words_features, features_map):
    col = list()
    row = list()
    data = list()
    for i in range(len(all_words_features)):
        word_features = all_words_features[i]
        for feature_key, feature_value in word_features.items():
            feature = '{0}={1}'.format(feature_key, feature_value)
            if feature in features_map.keys():
                row.append(i)
                col.append(features_map[feature])
                data.append(1)
    return sparse.csr_matrix((data, (row, col)), shape=(len(all_words_features), len(features_map.items())))


def get_prediction_of_all_words(all_words_features, clf, feature_map):
    numeric_format_matrix = create_features_numeric_format(all_words_features, feature_map)
    predict = clf.predict(numeric_format_matrix)
    return predict


def memm_greedy(sentences, max_sentence_len, features_map, counters_dict, clf):
    all_words_features = list()
    sentences_predictions = list()
    for j in range(len(sentences)):
        sentences_predictions.append(list())

    for i in range(max_sentence_len):
        start = datetime.now()
        for j in range(len(sentences)):
            sentence = sentences[j]
            if i < len(sentence):
                word = sentence[i]
                word_features = FeaturesUtils.get_word_features(i, sentence, sentences_predictions[j],
                                                                DictUtils.is_rare(counters_dict, word))
                all_words_features.append(word_features)
            else:
                all_words_features.append(dict())

        all_prediction_word_i = get_prediction_of_all_words(all_words_features, clf, features_map)

        end = datetime.now()
        print('word i={1} Running Time: {0}'.format(end - start, i))

        for j in range(len(all_prediction_word_i)):
            sentences_predictions[j].append(all_prediction_word_i[j])
        all_words_features = list()

    return sentences_predictions


def main(input_file_name, model_file_name, feature_map_file, output_file_name):
    start = datetime.now()

    clf, vec = FileUtils.read_logistic_regression_model(model_file_name)
    sentences, max_sentence_len = FileUtils.read_sentences(input_file_name)
    feature_map_lines = FileUtils.read_lines(feature_map_file)
    features_map, counters_dict, word_tag_dict, unk_tag_list = DictUtils.create_features_dicts(feature_map_lines)

    sentences_predictions = memm_greedy(sentences, max_sentence_len, features_map, counters_dict, clf)
    FileUtils.write_prediction(output_file_name, sentences, sentences_predictions)

    end = datetime.now()
    print('Running Time: {0}'.format(end - start))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
