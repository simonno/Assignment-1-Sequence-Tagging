import sys
import MLETrain

START = 'START'
dic_e = {}
dic_q = {}
num_word_count = 0


def create_dic(mle):
    dic = {}

    with open(mle) as file:
        for line in file:
            try:
                key, value = action(line)
                dic[key] = value
            except:
                continue

    return dic


def action(line):
    keys, value = line.split('\n')[0].split('\t')
    if keys == 'ALL':
        global num_word_count
        num_word_count = int(value)
        return
    split_keys = keys.split(' ')
    return tuple(split_keys), int(value)


def calculate_prob(x, c, b, a):
    return MLETrain.compute_e(x, c, dic_e, dic_q) * MLETrain.compute_q(dic_q, num_word_count, a, b, c, 0.6, 0.3, 0.1)


def argmax(index, word, possible_tags_list, max_tags_array):
    max_tag = possible_tags_list[0]
    max_prob = 0
    for tag in possible_tags_list:
        prob = calculate_prob(word, tag, max_tags_array[index - 1], max_tags_array[index - 2])
        if prob > max_prob:
            max_prob = prob
            max_tag = tag
    return max_tag


def possible_tags(word):
    tags = []
    for key in dic_e.keys():
        w = key[0]
        if w == word:
            tags.append(key[1])

    return tags



def greedy(input_file_name, greedy_hmm_output):
    tagged_text = ''

    with open(input_file_name, 'r') as input_file:

        for line in input_file:
            max_tags_array = [START, START]
            words = line.split(' ')

            for index in range(len(words)):
                word = words[index]
                max_tag = argmax(index, word, possible_tags(word), max_tags_array)
                max_tags_array.append(max_tag)
                tagged_text += str(word) + '/' + str(max_tag) + ' '

            tagged_text += '\n'

    with open(greedy_hmm_output, 'w') as output_file:
        output_file.write(tagged_text)


def main(input_file_name, q_mle, e_mle, greedy_hmm_output, extra_file_name):
    global dic_e, dic_q
    dic_e = create_dic(e_mle)
    dic_q = create_dic(q_mle)
    greedy(input_file_name, greedy_hmm_output)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
