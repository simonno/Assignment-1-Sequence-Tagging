import sys
from datetime import datetime

from sklearn.feature_extraction import DictVectorizer

from Utils.FileUtils import FileUtils


def create_features_format(dic):

    vec = DictVectorizer()
    vec.fit_transform(dic['NN']).toarray()
    print(vec.get_feature_names())


def main(features_file, model_file):
    start = datetime.now()
    all_features = FileUtils.read_features(features_file)
    print(all_features)
    create_features_format(all_features)
    # X_train, y_train = load_svmlight_file(features_file)
    end = datetime.now()
    print('Running Time: {0}'.format(end - start))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
