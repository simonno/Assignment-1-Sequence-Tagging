class FileUtils:

    @staticmethod
    def read_lines(file_name):
        lines = []
        with open(file_name, 'r') as file:
            for line in file:
                lines.append(line)
        return [line.strip() for line in lines]

    @staticmethod
    def add_new_features(all_tags_features, tag, tag_features):
        if tag not in all_tags_features.keys():
            all_tags_features[tag] = list()
        all_tags_features[tag].append(tag_features)

    @staticmethod
    def read_features(file_name):
        # all_tags_features = dict()
        Y = list()
        new_dic = list()
        with open(file_name, 'r') as file:
            for line in file:
                line = line.strip().split(' ')
                tag = line[0]
                Y.append(tag)
                # tag_features = dict()
                new_tag_features = dict()
                for feature in line[1:]:
                    label, value = feature.split('=', 1)
                    # if ',' in value:
                    #      value = tuple(value.split(','))
                    # tag_features[label] = value
                    new_tag_features[label] = value

                # FileUtils.add_new_features(all_tags_features, tag, tag_features)
                # FileUtils.add_new_features(new_dic, tag, new_tag_features)
                new_dic.append(new_tag_features)

        # return all_tags_features
        return new_dic, Y

    @staticmethod
    def write_events_count(file_name, dictionary):
        with open(file_name, 'w') as mle_file:
            for key, value in dictionary.items():
                if isinstance(key, tuple):
                    mle_file.write('{0}\t{1}\n'.format(' '.join(str(x) for x in key), value))
                else:
                    mle_file.write('{0}\t{1}\n'.format(key, value))

    @staticmethod
    def write_tagged_text(file_name, tagged_text):
        with open(file_name, 'w') as file:
            for tagged_sentence in tagged_text:
                tuples = ['{0}/{1}'.format(tuple[0], tuple[1]) for tuple in tagged_sentence]
                file.write(' '.join(tuples) + '\n')

    @staticmethod
    def write_features(file_name, features):
        with open(file_name, 'w') as file:
            for word_feature_dict in features:
                line = word_feature_dict['tag']
                for feature_key, feature_value in word_feature_dict.items():
                    if feature_key != 'tag':
                        line += ' {0}={1}'.format(feature_key, feature_value)

                file.write(line + '\n')
