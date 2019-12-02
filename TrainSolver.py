import sys
from datetime import datetime

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression

from Utils.FileUtils import FileUtils


def create_features_format(dic, Y, model_file):
    vec = DictVectorizer()

    transform_of_features = vec.fit_transform(dic)
    features_map = vec.get_feature_names()

    clf = LogisticRegression(tol=0.01, solver='saga', multi_class='multinomial').fit(transform_of_features, Y)

    return transform_of_features, features_map, (clf, vec)



def main(features_file, model_file):
    feature_map_file = 'Files/feature_map_file.txt'
    start = datetime.now()
    all_features, labels = FileUtils.read_features(features_file)
    transform_of_features, features_map, model = create_features_format(all_features, labels, model_file)
    FileUtils.write_feature_map(feature_map_file, features_map)
    FileUtils.write_logistic_regression_model(model_file, model)
    end = datetime.now()
    print('Running Time: {0}'.format(end - start))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
