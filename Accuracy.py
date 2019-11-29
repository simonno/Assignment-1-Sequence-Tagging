import sys

list_greedy = (())
list_dev = (())

def create_dic(input_file_name):
    list = [[]]
    with open(input_file_name, 'r') as input_file:
        l =0
        for line in input_file:
            split_line = line.split()
            i=0
            row = []
            while i < len(split_line):
                word, tag = split_line[i].rsplit('/', 1)
                row.append((word, tag))
            list.append(row)
            ++l
    return list

def accuracy(list_greedy, list_dev):
    acc =0
    diff = [[]]
    total = 0
    for i in len(list_greedy):
        for j in len(list_greedy[i]):
            if (list_greedy[i][j] == list_dev[i][j]):
                ++acc
            else:
                diff[i][j] = ((list_greedy[i][j], list_dev[i][j]))
            ++total

    print("accuracy:" + acc/total)
    print("acc:" + acc)
    print(diff)

def main(greedy_hmm_output, dev_output):
    global list_greedy, list_dev
    list_greedy = create_dic(greedy_hmm_output)
    list_dev = create_dic(dev_output)
    accuracy(list_greedy, list_dev)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
