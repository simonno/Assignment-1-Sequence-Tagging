import sys
from datetime import datetime

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression

from Utils.DictUtils import DictUtils
from Utils.FileUtils import FileUtils


def create_features_format(all_features, labels):
    vec = DictVectorizer()

    transform_of_features = vec.fit_transform(all_features)
    features_map = vec.get_feature_names()

    clf = LogisticRegression(tol=0.01, solver='saga', multi_class='multinomial').fit(transform_of_features, labels)

    return transform_of_features, features_map, (clf, vec)


def main(features_file, model_file):
    feature_map_file = 'Files/feature_map_file.txt'
    start = datetime.now()
    all_features, labels = FileUtils.read_features(features_file)
    counters_dict, word_tag_dict, unk_tad_dict = DictUtils.extract_features(all_features, labels)
    transform_of_features, features_map, model = create_features_format(all_features, labels)
    FileUtils.write_feature_map(feature_map_file, features_map, counters_dict)
    FileUtils.write_logistic_regression_model(model_file, model)
    end = datetime.now()
    print('Running Time: {0}'.format(end - start))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
