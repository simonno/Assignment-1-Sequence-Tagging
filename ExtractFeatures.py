import sys
from datetime import datetime

import MLETrain
from MLETrain import create_dicts
from Utils.DictUtils import DictUtils
from Utils.FeaturesUtils import FeaturesUtils
from Utils.FileUtils import FileUtils


def convert_line_to_lists(line):
    words = list()
    tags = list()
    for tuple in line.split(' '):
        word, tag = DictUtils.split_tuple(tuple)
        words.append(word)
        tags.append(tag)

    return words, tags


def create_features(features_dict, words, tags, dict_e):
    for i in range(len(words)):
        is_rare = DictUtils.is_rare(dict_e, words[i])
        features_dict[tags[i]] = FeaturesUtils.get_word_features(i, words, tags, is_rare)
        print(features_dict[tags[i]])
    return features_dict


def extract_features(lines, dict_e):
    features_dict = dict()
    for line in lines:
        words, tags = convert_line_to_lists(line)
        create_features(features_dict, words, tags, dict_e)

    return features_dict


def main(corpus_file, features_file):
    start = datetime.now()
    lines = FileUtils.read_lines(corpus_file)
    dict_q, dict_e = MLETrain.create_dicts(lines)
    features = extract_features(lines, dict_e)
    FileUtils.write_features(features_file, features)
    end = datetime.now()
    print('Running Time: {0}'.format(end - start))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
