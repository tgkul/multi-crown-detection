from keras.preprocessing import image as kimage
from keras.applications.resnet50 import preprocess_input

from keras.models import load_model, Model
from os.path import join
import numpy as np
import h5py
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import cv2
from skimage import measure

from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

from math import ceil

import warnings
warnings.filterwarnings("ignore")


def rgb2gray(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def gray2rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)


def gray2bgr(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


def initial_crop(img):
    height, width = img.shape
    new_width = width * 0.8
    new_height = height

    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2

    return np.array(Image.fromarray(img).crop((left, top, right, bottom)))


def crop(img, locx, locy, w, h):
    margin = 25
    if h > w:
        c = int((h - w) / 2)
        return img[locy - margin: locy + h + margin, locx - c - margin: locx + w + c + margin]
    if w > h:
        c = int((w - h) / 2)
        return img[locy - c - margin: locy + h + c + margin, locx - margin: locx + w + margin]


def erode(img):
    print('eroding...')
    kernel = np.ones((2, 2), np.uint8)
    return cv2.erode(img, kernel, iterations=1)


def recursive_mask_and_crop(img):
    print('\nRecursive Call')
    for contour in measure.find_contours(img, 55):
        if (len(contour) > 900):
            print(len(contour.astype(int)))

            cv2_contour = []

            for point in contour.astype(int):
                cv2_contour.append([point[1], point[0]])

            stencil = np.zeros(img.shape).astype(img.dtype)
            color = [255, 255, 255]
            cv2.fillPoly(stencil, [np.array(cv2_contour)], color)
            x, y, w, h = cv2.boundingRect(np.array(cv2_contour))

            cropped_image = crop(cv2.bitwise_and(img, stencil), x, y, w, h)

            if len(contour) < 1900:
                cv2.imwrite('dataset/crowns_extraction/test' + '_' + str(len(contour)) + '_crop.jpg',
                            gray2bgr(cropped_image))
                image_array.append(Image.fromarray(gray2rgb(cropped_image)))
            else:
                eroded_image = erode(cropped_image)
                recursive_mask_and_crop(eroded_image)


def crowns_detection(img_relative_path):
    img = Image.open(img_relative_path)
    img = img.point(lambda x: x * 0.95)

    img = rgb2gray(np.array(img))

    #     img = erode(initial_crop(img))

    recursive_mask_and_crop(img)


def feature_extractor(img1):
    img_data = kimage.img_to_array(img1.resize((224, 224)))
    img_data = np.expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    return model.predict(img_data)


def similarity_rank(arr1, arr2):
    mae = mean_absolute_error(arr1, arr2)
    mse = mean_squared_error(arr1, arr2)
    return mae, mse


def correct_histogram_of_single_image(image):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cv2_image = np.array(image.convert('L'))
    # cv2_image = cv2_image[:, :, ::-1].copy()
    cv2_image = clahe.apply(cv2_image)
    # cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(cv2_image).convert('RGB')


def matcher(database_path, img1, model):
    predicted_array = feature_extractor(img1)

    f = h5py.File(database_path, 'r')
    files = list(f.keys())

    min_mae = 9999999
    min_mse = 9999999
    afile = ''

    mse_list = []
    mae_list = []

    for file in files:
        database_image_array = np.array(f.get(file))
        mae, mse = similarity_rank(predicted_array.reshape(100352), database_image_array.reshape(100352))

        mae_list.append(mae)
        mse_list.append(mse)

        #         print (file, '-->', mse)

        if mae < min_mae and mse < min_mse:
            min_mae, min_mse = mae, mse
            afile = file

    return afile, min_mse, mse_list


def super_matcher(database_dir, test_image_path, model):
    crowns_detection(test_image_path)

    print('image_array: ' + str(len(image_array)))

    crown_dict1 = {}
    crown_error_dict1 = {}
    crown_mse_list_dict1 = {}

    for img in image_array:
        img1 = correct_histogram_of_single_image(img)
        file, mse, mse_list = matcher(database_dir, img1, model)
        crown_dict1[file] = img1
        crown_error_dict1[file] = mse
        crown_mse_list_dict1[file] = mse_list

    return crown_dict1, crown_error_dict1, crown_mse_list_dict1


model = load_model('model/model-resnet50.h5')


image_name = '1.jpg'
database = 'database_new.h5'


test_image_path = join('test_images', image_name)
database_dir = join('database', database)


image_array = []
crown_dict, crown_mse_dict, crown_mse_list_dict = super_matcher(database_dir, test_image_path, model)


number_of_crowns = len(crown_dict)
rows = ceil(number_of_crowns/4)
collage = Image.new('RGB', (1200, 300*rows))

i = 1
crowns = crown_dict.keys()
hoffset = 0
voffset = 0
for crown in crowns:
    img = crown_dict[crown].resize((300,300))
    ImageDraw.Draw(img).text((30,5), crown+' with error: '+str(crown_mse_dict[crown]), fill=(255,255,255))
    collage.paste(img, (hoffset, voffset))
    hoffset += 300
    if i%4==0:
        voffset += 300
        hoffset = 0
    i += 1

collage.save('saved_files/result.jpg')


crowns = crown_mse_list_dict.keys()

# for crown in crowns:
#     fig = plt.figure(figsize=(50, 25))
#     ax = fig.add_subplot(1,1,1)
#     plt.title(crown, fontsize=40)
#     plt.ylabel("Error", fontsize=40)
#     plt.xlabel("Files", fontsize=40)
#     ax.plot(list(range(len(crown_mse_list_dict[crown]))), crown_mse_list_dict[crown], linewidth=0.5)
#     plt.savefig('dataset/crowns_extraction/'+crown+'.pdf', format='pdf', dpi = 1200)



