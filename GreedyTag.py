import sys
import MLETrain

dic_e = {}
dic_q = {}


def create_dic(mle):
    dic = {}
    with open(mle) as file:
        for line in file:
            key, value = action(line)
            dic[key] = value

    return dic


def action(line):
    keys, value = line.split('\n')[0].split('\t')
    split_keys = keys.split(' ')
    return tuple(split_keys), int(value)


def argmax(index, word, possible_tags, max_tags_array):
    max_tag = possible_tags[0]
    max_prob = 0
    for tag in possible_tags:
        prob = calculate_prob(word, tag, max_tags_array[index - 1][1], max_tags_array[index - 2][1])
        if prob > max_prob:
            max_prob = prob
            max_tag = tag

    return max_tag


def possible_tags(word):
    tags = filter(lambda key: {item[1] for item in key if item[0] == word}, dic_e.keys())
    print(tags)
    return tags


def greedy(input_file_name, greedy_hmm_output):
    with open(input_file_name) as file:
        for line in file:
            max_tags_array = []
            words = line.split(' ')
            for index in range(len(words)):
                word = words[index]
                max = argmax(index, word, possible_tags(words), max_tags_array)


def main(input_file_name, q_mle, e_mle, greedy_hmm_output, extra_file_name):
    dic_e = create_dic(e_mle)
    dic_q = create_dic(q_mle)
    greedy(input_file_name, dic_q, dic_e, greedy_hmm_output)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
