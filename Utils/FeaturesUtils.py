from Utils.DictUtils import DictUtils


class FeaturesUtils:
    @staticmethod
    def num_of_instaces(word, dict_e):
        return DictUtils.get_value(dict_e, word)

    @staticmethod
    def suffix(word, num=4):
        if num > len(word):
            num = len(word)
        return [word[-i:] for i in range(1, num + 1)]

    @staticmethod
    def prefix(word, num=4):
        if num > len(word):
            num = len(word)
        return [word[:i] for i in range(num)]
