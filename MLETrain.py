import sys

START = 'START'
dic_q = {}
dic_e = {}
num_words = 0


# def count_first_word(x, b):
#     increment_q(b)
#     increment_e((x, b))
#
#
# def count_second_word(x, b, c):
#     increment_q((b, c))
#     increment_q(c)
#     increment_e((x, c))


def increment(params, dic):
    dic[params] = dic.get(params, 0) + 1


def increment_q(params):
    increment(params, dic_q)


def increment_e(params):
    increment(params, dic_e)


def calculation(x3, c, b, a):
    increment_q((a, b, c))
    increment_q((b, c))
    increment_q(c)
    increment_e((x3, c))


def create_dic(input_file_name):
    global num_words

    with open(input_file_name, 'r') as input_file:
        for line in input_file:
            split_line = line.split()
            num_words_in_line = len(split_line)
            num_words += num_words_in_line

            if num_words_in_line >= 1:
                x1, y1 = split_line[0].rsplit('/', 1)
                calculation(x1.lower(), y1, START, START)
                increment_q((START, START))
                increment_q(START)
                if num_words_in_line >= 2:
                    x2, y2 = split_line[1].rsplit('/', 1)
                    calculation(x2.lower(), y2, y1, START)
                    increment_q(START)

            i = 2
            while i < num_words_in_line:
                x1_a, x2_b, x3_c = split_line[i - 2:i + 1]
                x1, a = x1_a.rsplit('/', 1)
                x2, b = x2_b.rsplit('/', 1)
                x3, c = x3_c.rsplit('/', 1)

                calculation(x3.lower(), c, b, a)

                i += 1


def write_to_e_mle(output_file):
    unk_dic = {}
    with open(output_file, 'w') as mle_file:
        for key, value in dic_e.items():
            if value <= 5:
                unk_dic[key[1]] = dic_e.get(key, 0) + value
                continue
            mle_file.write(' '.join(str(x) for x in key) + '\t' + '{}'.format(value) + '\n')

        for key, value in unk_dic.items():
            mle_file.write('*UNK* ' + key + '\t' + '{}'.format(value) + '\n')

        mle_file.write('ALL' + '\t' + '{}'.format(num_words) + "\n")


def write_to_q_mle(output_file):
    with open(output_file, 'w') as mle_file:
        for key, value in dic_q.items():
            if isinstance(key, tuple):
                mle_file.write(' '.join(str(x) for x in key) + '\t' + '{}'.format(value) + '\n')
            else:
                mle_file.write(key + '\t' + '{}'.format(value) + '\n')
        mle_file.write('ALL' + '\t' + '{}'.format(num_words) + '\n')


# def compute_q(dic, num_words_count, a=' ', b=' ', c=' ', lr1=0, lr2=0, lr3=0):
#     return lr1 * (dic.get((a, b, c), 0) / dic.get((a, b), 1)) + lr2 * (dic.get((b, c), 0) / dic.get(b, 1)) + lr3 * (
#             dic.get(c, 0) / num_words_count)
#
#
# def compute_e(x, y, dic_e_mle, dic_q_mle):
#     return dic_e_mle.get((x, y), 0) / dic_q_mle.get((y), 1)


def main(input_file_name, q_mle, e_mle):
    create_dic(input_file_name)
    write_to_q_mle(q_mle)
    write_to_e_mle(e_mle)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
