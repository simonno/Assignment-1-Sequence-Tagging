import re

from Utils.WordSignature import WordSignatures

START = 'START'
UNK = '*unk*'


class DictUtils:
    @staticmethod
    def is_rare(dictionary, key, rare_factor=5):
        num_of_instances = DictUtils.get_value(dictionary, key)
        return True if num_of_instances <= rare_factor else False

    @staticmethod
    def get_value(dictionary, key):
        return dictionary.get(key, 0)

    @staticmethod
    def update_dict(dictionary, key, value=1):
        if key in dictionary:
            dictionary[key] += value
        else:
            dictionary[key] = value

    @staticmethod
    def split_tuple(tuple):
        return tuple.rsplit('/', 1)

    @staticmethod
    def insert_dict_e(dict_e, word, tag):
        for signature in WordSignatures.get_word_signatures(word):
            DictUtils.update_dict(dict_e, (signature, tag))

    @staticmethod
    def insert_dict_q(dict_q, tag, prev_tag, prev_prev_tag):
        DictUtils.update_dict(dict_q, tag)
        if prev_tag != START:
            DictUtils.update_dict(dict_q, (tag, prev_tag))
            if prev_tag != START:
                DictUtils.update_dict(dict_q, (tag, prev_tag, prev_prev_tag))

    @staticmethod
    def insert_sentence_to_dicts(dict_q, dict_e, sentence):
        prev_tag = START
        prev_prev_tag = START
        for tuple in sentence.split(' '):
            word, tag = DictUtils.split_tuple(tuple)
            DictUtils.insert_dict_e(dict_e, word, tag)
            DictUtils.insert_dict_q(dict_q, tag, prev_tag, prev_prev_tag)
            prev_prev_tag = prev_tag
            prev_tag = tag

    @staticmethod
    def convert_rare_words(dict_e, rare_value=5):
        converted_dict = dict()
        for tuple, value in dict_e.items():
            if value <= rare_value:
                DictUtils.update_dict(converted_dict, (UNK, tuple[1]), value)
            else:
                converted_dict[tuple] = value
        return converted_dict

    @staticmethod
    def convert_line_to_dict(lines):
        dictionary = dict()
        for line in lines:
            key, value = line.split('\t')
            if ' ' in key:
                key = tuple(key.split(' '))
            dictionary[key] = int(value)
        return dictionary

    @staticmethod
    def possible_tags(word, dict_e):
        tags = list()
        for tuple, value in dict_e.items():
            if word.lower() == tuple[0]:
                tags.append(tuple[1])
        return tags

    @staticmethod
    def add_word_tag(word_tag_dict, word, tag):
        if word not in word_tag_dict.keys():
            word_tag_dict[word] = list()
        if tag not in word_tag_dict[word]:
            word_tag_dict[word].append(tag)

    @staticmethod
    def extract_features(all_features, labels):
        counters_dict = dict()
        word_tag_dict = dict()
        unk_tag_dict = dict()
        for features_dict, tag in zip(all_features, labels):
            if 'form' in features_dict.keys():  # not a rare word
                word = features_dict['form']
                DictUtils.add_word_tag(word_tag_dict, word, tag)
                DictUtils.update_dict(counters_dict, word)
            else:  # a rare word
                DictUtils.update_dict(unk_tag_dict, tag)

        return counters_dict, word_tag_dict, unk_tag_dict

    @staticmethod
    def create_features_dicts(feature_map_lines):
        features = dict()
        counters_dict = dict()
        word_tag_dict = dict()
        for line in feature_map_lines:
            if re.match(r'.*=.* : \d', line):
                feature, index = line.split(' : ')
                features[feature] = int(index)
            # elif re.match(r'.*=\d', line):
            else:
                word, count = line.split('=')
                counters_dict[word] = int(count)
        return features, counters_dict
