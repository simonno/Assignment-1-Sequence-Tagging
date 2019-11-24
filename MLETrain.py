import sys

dic_q = {}
dic_e = {}
num_words = 0


def count_first_word(x, b):
    increment_q(b)
    increment_e((x, b))


def count_second_word(x, b, c):
    increment_q((b, c))
    increment_q(c)
    increment_e((x, c))


def increment(params, dic):
    dic[params] = dic.get(params, 0) + 1


def increment_q(params):
    increment(params, dic_q)


def increment_e(params):
    increment(params, dic_e)


def create_dic(input_file_name):
    global num_words

    f = open(input_file_name, "r")
    line = f.readline()

    while len(line) > 0:
        split_line = line.split()
        num_words += len(split_line)

        if len(split_line) > 1:
            x1, y1 = split_line[0].rsplit('/', 1)
            count_first_word(x1, y1)
            if len(split_line) > 2:
                x2, y2 = split_line[1].rsplit('/', 1)
                count_second_word(x1, y1, y2)

        i = 2
        while i < len(split_line):
            x1_a, x2_b, x3_c = split_line[i - 2:i + 1]
            x1, a = x1_a.rsplit('/', 1)
            x2, b = x2_b.rsplit('/', 1)
            x3, c = x3_c.rsplit('/', 1)

            increment_q((a, b, c))
            increment_q((b, c))
            increment_q(c)
            increment_e((x3, c))

            i += 1

        line = f.readline()
    f.close()


def write_to_mpl_file(mle, dic):
    file = open(mle, "w")
    for key, value in dic.items():
        file.write(' '.join(str(x) for x in key) + "\t" + '{}'.format(value) + "\n")
    file.close()


def compute_q(t1=' ', t2=' ', t3=' ', lr1=0, lr2=0, lr3=0):
    return lr1 * (dic_q.get((t1, t2, t3), 0) / dic_q.get((t1, t2), 1)) + lr2 * (
            dic_q.get((t2, t3), 0) / dic_q.get(t2, 1)) + lr3 * (dic_q.get((t1, t2, t3)) / num_words)


def compute_e(x, y):
    return dic_e.get((x, y), 0) / dic_q.get(y, 1)


# def transition_probabilities():
#     pass
#
# def emission_probabilities():
#     pass


def main(input_file_name, q_mle, e_mle):
    create_dic(input_file_name)
    write_to_mpl_file(q_mle, dic_q)
    write_to_mpl_file(e_mle, dic_e)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
