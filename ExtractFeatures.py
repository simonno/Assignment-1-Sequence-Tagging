import sys
from datetime import datetime
from MLETrain import create_dicts
from Utils.DictUtils import DictUtils
from Utils.FeaturesUtils import FeaturesUtils
from Utils.FileUtils import FileUtils

MIN_NUM_OF_INSTANCES = 5

def create_features_to_word(word, tag, features_dict, sentence):
    all_features = (("form", word))
    if FeaturesUtils.num_of_instaces() < MIN_NUM_OF_INSTANCES:
        all_features += FeaturesUtils.add_all_features(word)


def create_features(sentence, features_dict):
    for tuple in sentence.split(' '):
        word, tag = DictUtils.split_tuple(tuple)
        features_dict[tag] = create_features(word, tag, features_dict, sentence)

def extract_features(sentences):
    features_dict = dict()
    for sentence in sentences:
        create_features(sentence, features_dict)


def main(corpus_file, features_file):
    start = datetime.now()
    sentences = FileUtils.read_lines(corpus_file)
    dict_q, dict_e = create_dicts(sentences)
    features = extract_features(sentences)

    FileUtils.write_features(features_file, features)

    end = datetime.now()
    print('Running Time: {0}'.format(end - start))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])