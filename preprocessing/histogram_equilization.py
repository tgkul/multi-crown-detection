from cv2 import imread, imwrite, IMREAD_GRAYSCALE, createCLAHE, cvtColor, COLOR_BGR2RGB
from PIL import Image
from os import walk, remove
from os.path import join
from numpy import array


def correct_histogram(root_dir_path):
    clahe = createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    for subdir, dirs, files in walk(root_dir_path):
        if subdir != root_dir_path:
            for file in files:
                if 'jpg' in file:
                    img_relative_path = join(subdir, file)
                    try:
                        imwrite(img_relative_path, clahe.apply(imread(img_relative_path, IMREAD_GRAYSCALE)))
                    except:
                        remove(img_relative_path)


def correct_histogram_of_single_image(image):
    clahe = createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cv2_image = array(image)
    cv2_image = cv2_image[:, :, ::-1].copy()
    cv2_image = clahe.apply(cv2_image)
    cv2_image = cvtColor(cv2_image, COLOR_BGR2RGB)
    return Image.fromarray(cv2_image)
