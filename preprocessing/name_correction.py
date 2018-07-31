from os import rename, listdir
from os.path import join
from re import sub, match, escape


def rename_files(dataset_dir, id_length):
    for file in listdir(dataset_dir):
        rename(join(dataset_dir, file), join(dataset_dir, sub('[^0-9a-zA-Z.]+', '', file)))

    for file in listdir(dataset_dir):
        rename(join(dataset_dir, file), join(dataset_dir, file.lower()))

    for file in listdir(dataset_dir):

        match_regex = '[0-9]{' + escape(str(id_length)) + '}'
        if id_length == 0:
            match_regex = '[0-9]+'

        if 'in' in file:
            rename(join(dataset_dir, file), join(dataset_dir, match(match_regex, file).group(0) + '_in.jpg'))
        elif 'ou' in file:
            rename(join(dataset_dir, file), join(dataset_dir, match(match_regex, file).group(0) + '_out.jpg'))

    for file in listdir(dataset_dir):
        if ' ' in file:
            rename(join(dataset_dir, file), join(dataset_dir, file.replace(' ', '')))
