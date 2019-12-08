import re


class WordSignatures:
    @staticmethod
    def get_word_signatures(word):
        signatures = list()
        if re.match(r'^-?\d+(?:-\.\d+)?$', word) is not None:
            signatures.append("^" + "num")
        elif re.compile('.*[0-9].*').search(word) is not None:
            signatures.append("^" + "cnum")
        elif re.match(r"^[A-Z][a-z]+$", word):  # special cases
            signatures.append("^" + "aa")
        elif re.compile('.*ing$').search(word) is not None:
            signatures.append("^" + "ing")
        elif re.compile('.*ons$').search(word) is not None:
            signatures.append("^" + "ons")
        elif re.compile('.*es$').search(word) is not None:
            signatures.append("^" + "es")
        elif re.compile('.*ly$').search(word) is not None:
            signatures.append("^" + "ly")
        elif re.compile('.*ion$').search(word) is not None:
            signatures.append("^" + "ion")
        elif re.compile('.*ed$').search(word) is not None:
            signatures.append("^" + "ed")
        elif re.compile('^[A-Z]').search(word) is not None:
            signatures.append("^" + "capital")
        elif re.compile('.*[-].*').search(word) is not None:
            signatures.append("^" + "hyp")
        elif re.compile('^.{1,2}$').search(word) is not None:
            signatures.append("^" + "unk2")
        elif re.compile('^.{3,4}$').search(word) is not None:
            signatures.append("^" + "unk4")
        elif re.compile('^.{5,6}$').search(word) is not None or re.compile('^.{7,8}$').search(word) is not None:
            signatures.append("^" + "unk8")
        signatures.append(word.lower())
        return signatures
