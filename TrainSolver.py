import sys
from datetime import datetime

import pickle
from sklearn.datasets import load_iris
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression

from Utils.FileUtils import FileUtils


def create_features_format(dic, Y, model_file):

    vec = DictVectorizer()

    transform_of_features = vec.fit_transform(dic)
    features_map = vec.get_feature_names()

    clf = LogisticRegression(tol=0.01, solver='saga',multi_class = 'multinomial').fit(transform_of_features, Y)

    #  print to model_file
    with open(model_file, "wb") as f:
        pickle.dump((clf, vec), f, fix_imports=True)
    return transform_of_features, features_map, clf

# need to get also counter
def write_to_feature_map_file(map_features):
    features_to_indexes = ""
    with open("feature_map_file.txt", "w") as f:
        for feature in map_features:
            features_to_indexes += '{0} : {1}\n'.format(feature, map_features.index(feature))
        f.write(features_to_indexes)
        f.write("counter")
        f.write("\n")



def main(features_file, model_file):
    start = datetime.now()
    all_features, Y = FileUtils.read_features(features_file)
    vec = DictVectorizer()
    transform_of_features, features_map, clf = create_features_format(all_features, Y, model_file)
    write_to_feature_map_file(features_map)
    end = datetime.now()
    print('Running Time: {0}'.format(end - start))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
