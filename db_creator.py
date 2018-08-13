from warnings import filterwarnings
from os import walk, remove
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
from errno import ENOENT

filterwarnings("ignore")


class DatabaseCreator:
    def __init__(self):
        self.resnet = load_model(join('model', 'model-resnet50.h5'))
        print('Model Loaded')

    def file_remove(self, filename):
        try:
            remove(filename)
        except OSError as e:
            if e.errno != ENOENT:
                raise

    def main(self, dir_path, id_length, database_name):
        rename_files(dataset_dir=dir_path, id_length=id_length)
        print('Rename Done')

        correct_tree(dataset_path=dir_path)
        print('Tree Corrected')

        crop_to_crown(root_file_path=dir_path)
        print('cropped')

        augment(root_dir_path=dir_path)
        print('augmented')

        correct_histogram(root_dir_path=dir_path)
        print('Histogram Corrected')

        self.file_remove(join('database', database_name))

        for subdir, dirs, files in walk(dir_path):
            if subdir != dir_path:
                for file in files:
                    if 'jpg' in file:
                        img_relative_path = join(subdir, file)
                        image = open(img_relative_path).convert('RGB')
                        features = get_features(image, self.resnet)
                        add_image_features(file.split('.')[0], features, database_name)

        print('Database Created')


if __name__ == '__main__':

    creator = DatabaseCreator()

    flag = True

    while flag:

        root_path = input("\n\nEnter the root path of images [db_images]: ") or "db_images"
        database_name = input("Enter the database name [database]: ") or "database"
        id_length = input("Enter the ID length [any]: ") or '0'

        creator.main(root_path, int(id_length), database_name+'.h5')

        not_stop = input("\nDo you want to continue? (Y/N): ")

        if not_stop.lower() == 'n':
            flag = False
