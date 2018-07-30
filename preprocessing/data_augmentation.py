from os import walk
from os.path import join
from cv2 import imread, imwrite
from numpy import arange
from imutils import rotate


def augment(root_dir_path, degree_rotation=10):
    for subdir, dirs, files in walk(root_dir_path):
        if subdir != root_dir_path:
            for file in files:
                if 'jpg' in file:
                    idir = join(subdir, file)
                    image = imread(idir)
                    i = 0
                    for angle in arange(0, 360, degree_rotation):
                        rotated = rotate(image, angle)
                        imwrite(idir.split('.')[0] + '_' + str(i) + '.jpg', rotated)
                        i += 1
