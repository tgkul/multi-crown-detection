from h5py import File
from os.path import join


def add_image_features(image_name, features_array, database_name):
    database_dir = join('database', database_name)
    with File(database_dir, 'a') as hdf:
        hdf.create_dataset(image_name, data=features_array)

