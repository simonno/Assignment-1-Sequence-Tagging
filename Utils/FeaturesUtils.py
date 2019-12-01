from Utils.DictUtils import DictUtils
import re

from Utils.WordSignature import WordSignatures


class FeaturesUtils:
    @staticmethod
    def num_of_instaces(word, dict_e):
        return DictUtils.get_value(dict_e, word)

    @staticmethod
    def all_suffixes(word, num=4):
        if num > len(word):
            num = len(word)
        return [word[-i:] for i in range(1, num + 1)]

    @staticmethod
    def all_prefixes(word, num=4):
        if num > len(word):
            num = len(word)
        return [word[:i] for i in range(num)]
    #
    # @staticmethod
    # def contains_number(word):
    #     return re.compile('.*[0-9].*').search(word)
    @staticmethod
    def add_all_features(word):
        all_features = ''
        for suff in FeaturesUtils.all_suffixes(word):
            all_features += (("suff", suff))
        for pref in FeaturesUtils.all_prefixes(word):
            all_features += (("pref", pref))
        for signeture in WordSignatures.get_word_signatures(word):
            all_features += (("signature", signeture))
        return all_features


