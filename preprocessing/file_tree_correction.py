from os import listdir, makedirs
from os.path import join
from shutil import move


def correct_tree(dataset_path, mode=0):
    """
    Mode 1: Files will be arranged in their ID folders separately
    Mode 0: Files will be arranged according to crowns In/ Out placement in the photos
    """

    if mode == 1:
        for file in listdir(dataset_path):
            dest = join(dataset_path, file.split('_')[0])
            makedirs(dest, exist_ok=True)
            move(join(dataset_path, file), dest)
    else:
        for file in listdir(dataset_path):
            try:
                dest = join(dataset_path, file.split('_')[1].split(".")[0])
                makedirs(dest, exist_ok=True)
                move(join(dataset_path, file), dest)
            except:
                print('Error for: ', file)
