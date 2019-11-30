class FileUtils:
    @staticmethod
    def read_lines(file_name):
        lines = []
        with open(file_name, 'r') as file:
            for line in file:
                lines.append(line)
        return [line.strip() for line in lines]

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
            for tag, tag_features_dict in features.items():
                line = tag
                for feature_key , feature_value in tag_features_dict.items():
                    line += ' {0}={1}'.format(feature_key,feature_value)

                file.write(line + '\n')
