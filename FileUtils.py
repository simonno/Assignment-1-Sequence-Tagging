class FileUtils:
    @staticmethod
    def read_sentences(file_name):
        lines = []
        with open(file_name, 'r') as f:
            for line in f:
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
