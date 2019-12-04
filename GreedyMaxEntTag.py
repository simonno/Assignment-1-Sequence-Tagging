import pickle
import sys
from datetime import datetime

from Utils.DictUtils import DictUtils
from Utils.FileUtils import FileUtils


def get_tags(sentence, w, feature_extractor):
    y = []
    for i in len(sentence):
        y[i] = argmax()


def hmm_greedy(sentences, feature_map, model_file):
    tags = list()

    for sentence in sentences:
        tags.append(get_tags(sentence))

    return tags


def main(input_file_name, model_file, feature_map_file, out_file_name):
    start = datetime.now()
    sentences = FileUtils.read_lines(input_file_name)
    feature_map_lines = FileUtils.read_lines(feature_map_file)
    features_map, counters_dict, word_tag_dict, unk_tad_dict = DictUtils.create_features_dicts(feature_map_lines)
    model_file = open(model_file, 'rb')
    (clf, vec) = pickle.load(model_file)

    tagged_text = hmm_greedy(sentences, feature_map, model_file)
    FileUtils.write_tagged_text(out_file_name, tagged_text)
    end = datetime.now()
    print('Running Time: {0}'.format(end - start))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
