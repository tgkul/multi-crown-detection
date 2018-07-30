from warnings import filterwarnings
from os import walk
from os.path import join
from PIL.Image import open
from keras.models import load_model

from preprocessing.name_correction import rename_files
from preprocessing.file_tree_correction import correct_tree
from preprocessing.crowndetector import crop_to_crown
from mlmodel.featureextractor import get_features
from preprocessing.data_augmentation import augment
from preprocessing.histogram_equilization import correct_histogram
from preprocessing.database_creator import add_image_features

filterwarnings("ignore")


def main(dir_path):
    rename_files(dir_path)
    print('Rename Done')

    correct_tree(dir_path)
    print('Tree Corrected')

    crop_to_crown(dir_path)
    print('cropped')

    augment(dir_path)
    print('augmented')

    correct_histogram(dir_path)
    print('Histogram Corrected')

    resnet = load_model(join('model', 'model-resnet50.h5'))

    for subdir, dirs, files in walk(dir_path):
        if subdir != dir_path:
            for file in files:
                if 'jpg' in file:
                    img_relative_path = join(subdir, file)
                    image = open(img_relative_path).convert('RGB')
                    features = get_features(image, resnet)
                    add_image_features(file.split('.')[0], features, 'database_1.h5')

    print('Database Created')

if __name__ == '__main__':
    main('db_images_1')
