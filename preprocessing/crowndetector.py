from cv2 import COLOR_RGB2GRAY, COLOR_GRAY2RGB, COLOR_GRAY2BGR
from cv2 import erode as cv2erode
from cv2 import fillPoly, boundingRect, bitwise_and, imwrite, cvtColor
from PIL.Image import fromarray
from PIL.Image import open as imgopen
from skimage.measure import find_contours
from numpy import array, uint8, ones, zeros
from os.path import join


def rgb2gray(img):
    return cvtColor(img, COLOR_RGB2GRAY)


def gray2rgb(img):
    return cvtColor(img, COLOR_GRAY2RGB)


def gray2bgr(img):
    return cvtColor(img, COLOR_GRAY2BGR)


def initial_crop(img):
    height, width = img.shape
    new_width = width * 0.8
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
    return cv2erode(img, kernel, iterations=1)


def recursive_mask_and_crop(img, image_array):
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
                image_array.append(fromarray(gray2rgb(cropped_image)))
            else:
                eroded_image = erode(cropped_image)
                image_array = recursive_mask_and_crop(eroded_image, image_array)
    return image_array


def get_crowns(img_relative_path):
    image_array = []
    img = imgopen(img_relative_path)
    img = img.point(lambda x: x * 0.95)

    img = rgb2gray(array(img))

    image_array = recursive_mask_and_crop(img, image_array)

    return image_array
