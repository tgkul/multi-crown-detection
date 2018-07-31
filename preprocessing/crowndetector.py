from cv2 import COLOR_RGB2GRAY, COLOR_GRAY2RGB, COLOR_GRAY2BGR, IMREAD_GRAYSCALE
from cv2 import erode as cv2erode
import cv2
from cv2 import fillPoly, boundingRect, bitwise_and, imread, imwrite, cvtColor
from PIL.Image import fromarray
from PIL.Image import open as imgopen
from skimage.measure import find_contours
from numpy import array, uint8, ones, zeros
from os import walk
from os.path import join
from globals import global_variables


def rgb2gray(img):
    return cvtColor(img, COLOR_RGB2GRAY)


def gray2rgb(img):
    return cvtColor(img, COLOR_GRAY2RGB)


def gray2bgr(img):
    return cvtColor(img, COLOR_GRAY2BGR)


def initial_crop(img):
    height, width = img.shape
    new_width = width * 0.7
    new_height = height

    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2

    return array(fromarray(img).crop((left, top, right, bottom)))


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
    kernel = ones((2, 2), uint8)
    return cv2.erode(img, kernel, iterations=1)


def recursive_mask_and_crop(img):
    print('\nRecursive Call')
    for contour in find_contours(img, 55):
        if len(contour) > 900:
            print(len(contour.astype(int)))

            cv2_contour = []

            for point in contour.astype(int):
                cv2_contour.append([point[1], point[0]])

            stencil = zeros(img.shape).astype(img.dtype)
            color = [255, 255, 255]
            fillPoly(stencil, [array(cv2_contour)], color)
            x, y, w, h = boundingRect(array(cv2_contour))

            cropped_image = crop(bitwise_and(img, stencil), x, y, w, h)

            if len(contour) < 1900:
                # imwrite(join('saved_files', 'test'+'_'+str(len(contour))+'_crop.jpg'), gray2bgr(cropped_image))
                global_variables.image_array.append(fromarray(gray2rgb(cropped_image)))
            else:
                eroded_image = erode(cropped_image)
                recursive_mask_and_crop(eroded_image)


def get_crowns(img_relative_path):
    img = imgopen(img_relative_path)
    img = img.point(lambda x: x * 0.95)
    img = rgb2gray(array(img))

    recursive_mask_and_crop(img)


def crop_to_crown(root_file_path):
    for subdir, dirs, files in walk(root_file_path):
        if subdir != root_file_path:
            for file in files:
                if 'jpg' in file:

                    img_relative_path = join(subdir, file)

                    image = imread(img_relative_path, IMREAD_GRAYSCALE)

                    image = initial_crop(image)

                    contours = find_contours(image, 80)

                    contour = max(contours, key=len).astype(int)

                    cv2_contour = []

                    for point in contour:
                        cv2_contour.append([point[1], point[0]])

                    contour = array(cv2_contour)

                    stencil = zeros(image.shape).astype(image.dtype)
                    color = [255, 255, 255]
                    fillPoly(stencil, [contour], color)
                    image = bitwise_and(image, stencil)

                    x, y, w, h = boundingRect(contour)
                    #                 print(x,y,w,h)
                    cropped_image = crop(image, x, y, w, h)
                    final_image = gray2bgr(cropped_image)

                    imwrite(img_relative_path.split('.')[0] + '.jpg', final_image)
