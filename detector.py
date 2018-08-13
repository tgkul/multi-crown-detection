from os import environ
environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from warnings import filterwarnings
from keras.models import load_model
from h5py import File as h5File
from numpy import array as nparray
from os.path import join, isdir, split
from shutil import rmtree
from os import mkdir
from os import system, name

from metric.mse import get_mse
from mlmodel.featureextractor import get_features
from preprocessing.crowndetector import get_crowns
from preprocessing.histogram_equilization import correct_histogram_of_single_image
from save_results.savecollage import save_collage, save_images
from save_results.saveplot import save_plots
from globals import global_variables

filterwarnings("ignore")


def cls():
    system('cls' if name == 'nt' else 'clear')


class Detector:

    def __init__(self):
        if isdir('saved_files'):
            rmtree('saved_files')
        mkdir('saved_files')

        self.resnet = load_model(join('model', 'model-resnet50.h5'))

        cls()
        print('Model loaded\n\n')

    def matcher(self, database_path, img, model):
        predicted_array = get_features(img, model)

        f = h5File(database_path, 'r')
        files = list(f.keys())

        min_mse = 9999999
        afile = ''

        mse_dict = {}

        for file in files:
            crown_id = file.split('_')[0]
            database_image_array = nparray(f.get(file))
            mse = get_mse(database_image_array.reshape(100352), predicted_array.reshape(100352))

            if crown_id in mse_dict:
                if mse < mse_dict[crown_id]:
                    mse_dict[crown_id] = mse
            else:
                mse_dict[crown_id] = mse

            if mse < min_mse:
                min_mse = mse
                afile = file

        return afile, min_mse, mse_dict

    def super_matcher(self, database_path, test_image_path):
        get_crowns(test_image_path)

        images = global_variables.image_array

        crown_dict = {}
        crown_error_dict = {}
        crown_mse_list_dict = {}

        print('\nNumber of crowns: ', len(images))

        for img in images:
            img = correct_histogram_of_single_image(img)
            file, mse, mse_dict = self.matcher(database_path, img, self.resnet)
            crown_dict[file] = img
            crown_error_dict[file] = mse
            crown_mse_list_dict[file] = mse_dict

        return crown_dict, crown_error_dict, crown_mse_list_dict

    def get_ids(self, database_path, image_path):
        global_variables.init()

        crown_images, crown_mse, crown_mse_list = self.super_matcher(database_path, image_path)
        save_collage(split(image_path)[-1].split('.')[0], crown_images, crown_mse)
        save_images(split(image_path)[-1].split('.')[0], crown_images, crown_mse)
        save_plots(split(image_path)[-1].split('.')[0], crown_mse_list)


def main():

    detector = Detector()

    flag = True

    while flag:
        cls()
        img_name = input("\nEnter the path of image [2.jpg]: ") or "2.jpg"
        database_name = input("Enter the database name [database.h5]: ") or "database.h5"

        image_path = join('test_images', img_name)
        database_path = join('database', database_name)

        detector.get_ids(database_path, image_path)

        not_stop = input("\nDo you want to continue? (Y/N): ")

        if not_stop.lower() == 'n':
            flag = False


if __name__ == '__main__':
    main()
    cls()
