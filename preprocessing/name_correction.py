from os import rename, listdir
from os.path import join
from re import sub, match


def rename_files(dataset_dir, id_ength):
    for file in listdir(dataset_dir):
        rename(join(dataset_dir, file), join(dataset_dir, sub('[^0-9a-zA-Z.]+', '', file)))

    for file in listdir(dataset_dir):
        rename(join(dataset_dir, file), join(dataset_dir, file.lower()))

    for file in listdir(dataset_dir):
        if 'in' in file:
            rename(join(dataset_dir, file), join(dataset_dir, match('[0-9]', file).group(0) + '_in.jpg'))
        elif 'ou' in file:
            rename(join(dataset_dir, file), join(dataset_dir, match('[0-9]', file).group(0) + '_out.jpg'))

    for file in listdir(dataset_dir):
        if ' ' in file:
            rename(join(dataset_dir, file), join(dataset_dir, file.replace(' ', '')))
