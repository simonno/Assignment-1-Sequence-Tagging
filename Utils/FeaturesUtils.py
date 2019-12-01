import re


class FeaturesUtils:
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

    @staticmethod
    def add_prefixes_features(feature_dict, word):
        prefixes = FeaturesUtils.all_prefixes(word)
        for prefix in prefixes:
            feature_dict['pref'] = prefix

    @staticmethod
    def add_suffixes_features(feature_dict, word):
        suffixes = FeaturesUtils.all_suffixes(word)
        for suffix in suffixes:
            feature_dict['suff'] = suffix

    @staticmethod
    def is_contains_number(word):
        re.match(r'.*\d.*', word)

    @staticmethod
    def is_contains_uppercase(word):
        re.match(r'.*[A-Z].*', word)

    @staticmethod
    def is_contains_hyphen(word):
        re.match(r'.*-.*', word)

    @staticmethod
    def add_rare_word_features(feature_dict, word):
        FeaturesUtils.add_prefixes_features(feature_dict, word)
        FeaturesUtils.add_suffixes_features(feature_dict, word)
        if FeaturesUtils.is_contains_number(word):
            feature_dict['contains_number'] = 'true'
        if FeaturesUtils.is_contains_uppercase(word):
            feature_dict['contains_uppercase'] = 'true'
        if FeaturesUtils.is_contains_hyphen(word):
            feature_dict['contains_hyphen'] = 'true'

    @staticmethod
    def add_prev_tags_features(feature_dict, i, tags_list):
        if i > 0:
            prev_tag = tags_list[i - 1]
            feature_dict['pt'] = prev_tag
            if i > 1:
                prev_prev_tag = tags_list[i - 2]
                feature_dict['ppt'] = prev_prev_tag
                feature_dict['ppt_pt'] = '{0} {1}'.format(prev_prev_tag, prev_tag)

    @staticmethod
    def add_prev_next_words(feature_dict, i, words_list):
        if i + 1 < len(words_list):
            feature_dict['nw'] = words_list[i + 1]
            if i + 2 < len(words_list):
                feature_dict['nnw'] = words_list[i + 2]

        if i > 0:
            feature_dict['pw'] = words_list[i - 1]
            if i > 1:
                feature_dict['ppw'] = words_list[i - 2]

    @staticmethod
    def add_any_word_features(feature_dict, i, tags_list, words_list):
        FeaturesUtils.add_prev_tags_features(feature_dict, i, tags_list)
        FeaturesUtils.add_prev_next_words(feature_dict, i, words_list)

    @staticmethod
    def get_word_features(i, words_list, tags_list, is_rare):
        feature_dict = dict()
        if is_rare:
            FeaturesUtils.add_rare_word_features(feature_dict, words_list[i])
        else:
            feature_dict['form'] = words_list[i]

        FeaturesUtils.add_any_word_features(feature_dict, i, tags_list, words_list)

        return feature_dict
