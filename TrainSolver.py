import sys
from datetime import datetime
from sklearn.datasets import load_svmlight_file


def main(features_file, model_file):
    start = datetime.now()
    X_train, y_train = load_svmlight_file("/path/to/train_dataset.txt")
    end = datetime.now()
    print('Running Time: {0}'.format(end - start))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])