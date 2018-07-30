from warnings import filterwarnings
from keras.models import load_model
from h5py import File as h5File
from numpy import array as nparray
from os.path import join

from metric.mse import get_mse
from mlmodel.featureextractor import get_features
from preprocessing.crowndetector import get_crowns
from preprocessing.histogram_equilization import correct_histogram_of_single_image
from save_results.savecollage import save_collage, get_collage
from save_results.saveplot import save_plots


filterwarnings("ignore")


class Model():
    def __init__(self, base_dir, context):
        self.base_dir = base_dir
        self.context = context
        self.log = context['logger']

        self.resnet = load_model(join(base_dir, 'model-resnet50.h5'))

    def matcher(self, database_path, img, model):
        predicted_array = get_features(img, model)

        f = h5File(database_path, 'r')
        files = list(f.keys())

        min_mse = 9999999
        afile = ''

        mse_list = []

        for file in files:
            database_image_array = nparray(f.get(file))
            mse = get_mse(predicted_array.reshape(100352), database_image_array.reshape(100352))

            mse_list.append(mse)

            if mse < min_mse:
                min_mse = mse
                afile = file

        return afile, min_mse, mse_list

    def super_matcher(self, database_dir, test_image_path, model):
        images = get_crowns(test_image_path)

        print('image_array: ' + str(len(images)))

        crown_dict = {}
        crown_error_dict = {}
        crown_mse_list_dict = {}

        for img in images:
            img = correct_histogram_of_single_image(img)
            file, mse, mse_list = self.matcher(database_dir, img, model)
            crown_dict[file] = img
            crown_error_dict[file] = mse
            crown_mse_list_dict[file] = mse_list

        return crown_dict, crown_error_dict, crown_mse_list_dict

    def inference(self, filename, context):
        test_image_path = join('test_images', filename)
        database_dir = join('database', 'database.h5')

        crown_images, crown_mse, crown_mse_list = self.super_matcher(database_dir, test_image_path, self.resnet)

        # save_collage(crown_images, crown_mse)
        save_plots(crown_mse_list)
        return get_collage(crown_images, crown_mse)





# def matcher(database_path, img, model):
#     predicted_array = get_features(img, model)
#
#     f = h5File(database_path, 'r')
#     files = list(f.keys())
#
#     min_mse = 9999999
#     afile = ''
#
#     mse_list = []
#
#     for file in files:
#         database_image_array = nparray(f.get(file))
#         mse = get_mse(predicted_array.reshape(100352), database_image_array.reshape(100352))
#
#         mse_list.append(mse)
#
#         if mse < min_mse:
#             min_mse = mse
#             afile = file
#
#     return afile, min_mse, mse_list
#
#
# def super_matcher(database_dir, test_image_path, model):
#     images = get_crowns(test_image_path)
#
#     print('image_array: ' + str(len(images)))
#
#     crown_dict = {}
#     crown_error_dict = {}
#     crown_mse_list_dict = {}
#
#     for img in images:
#         img = correct_histogram_of_single_image(img)
#         file, mse, mse_list = matcher(database_dir, img, model)
#         crown_dict[file] = img
#         crown_error_dict[file] = mse
#         crown_mse_list_dict[file] = mse_list
#
#     return crown_dict, crown_error_dict, crown_mse_list_dict
#
#
# def main():
#     resnet = load_model(join('model', 'model-resnet50.h5'))
#
#     test_image_path = join('test_images', '4.jpg')
#     database_dir = join('database', 'database.h5')
#
#     crown_images, crown_mse, crown_mse_list = super_matcher(database_dir, test_image_path, resnet)
#
#     save_collage(crown_images, crown_mse)
#     save_plots(crown_mse_list)
#
#
# if __name__ == '__main__':
#     main()
