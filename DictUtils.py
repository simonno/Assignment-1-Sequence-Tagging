from WordSignature import WordSignatures

START = 'START'
UNK = '*UNK*'


class DictUtils:
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
