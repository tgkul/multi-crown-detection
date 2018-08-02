from warnings import filterwarnings
from keras.models import load_model
from h5py import File as h5File
from numpy import array as nparray
from os.path import join, isdir
from shutil import rmtree
from os import mkdir

from metric.mse import get_mse
from mlmodel.featureextractor import get_features
from preprocessing.crowndetector import get_crowns
from preprocessing.histogram_equilization import correct_histogram_of_single_image
from save_results.savecollage import save_collage, get_collage
from save_results.saveplot import save_plots
from globals import global_variables


filterwarnings("ignore")


class Model:
    def __init__(self, base_dir, context):
        self.base_dir = base_dir
        self.context = context
        self.log = context['logger']

        self.resnet = load_model(join(base_dir, 'model-resnet50.h5'))
        self.log.info('model initialization completed')

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
            mse = get_mse(predicted_array.reshape(100352), database_image_array.reshape(100352))

            if crown_id in mse_dict:
                if mse < mse_dict[crown_id]:
                    mse_dict[crown_id] = mse
            else:
                mse_dict[crown_id] = mse

            if mse < min_mse:
                min_mse = mse
                afile = file

        return afile, min_mse, mse_dict

    def super_matcher(self, database_dir, test_image_path, model):
        get_crowns(test_image_path)

        images = global_variables.image_array

        crown_dict = {}
        crown_error_dict = {}
        crown_mse_list_dict = {}

        for img in images:
            img = correct_histogram_of_single_image(img)
            file, mse, mse_dict = self.matcher(database_dir, img, model)
            crown_dict[file] = img
            crown_error_dict[file] = mse
            crown_mse_list_dict[file] = mse_dict

        return crown_dict, crown_error_dict, crown_mse_list_dict

    def inference(self, filename, context):
        global_variables.init()

        resnet = load_model(join('model', 'model-resnet50.h5'))

        test_image_path = join('test_images', filename)
        database_dir = join('database', 'database_new.h5')

        crown_images, crown_mse, crown_mse_list = self.super_matcher(database_dir, test_image_path, resnet)

        save_collage(crown_images, crown_mse)
        save_plots(crown_mse_list)
        return get_collage(crown_images, crown_mse)