import sys


def accuracy(algorithm_output, dev_output):
    acc = 0
    diff = []
    total = 0
    with open(algorithm_output, 'r') as algo_output, open(dev_output, 'r') as result_output:
        for algo_line, result_line in zip(algo_output, result_output):
            algo_line = algo_line.split()
            result_line = result_line.split()
            for algo_tuple, result_tuple in zip(algo_line, result_line):
                algo_word, algo_tag = algo_tuple.rsplit('/', 1)
                result_word, result_tag = result_tuple.rsplit('/', 1)
                if algo_tag == result_tag:
                    acc += 1
                else:
                    diff.append((algo_tuple, result_tuple))
                total += 1


def main(algorithm_output, result_output):
    accuracy(algorithm_output, result_output)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
