=====================
Multi Crown Detection
=====================

|

Introduction
------------

Purpose of this project is to identify dental crowns by taking photographs.
As an added functionality, a photograph may contain multiple crowns.
The code is written to detect all crowns and identify them separately.

The detection happens by comparing features of dental crowns. These features are stored in a database/ file.
Since the data is all numerical, this database is formatted as HDF5 file for fast retrieval and efficient, secure storage.

This project contains 2 main files. db_creator.py and detector.py

|

Description
-----------

|

**1. db_creator.py**

This file create a database of crown features from the provided images.

For creating or adding images to the database,
the files should be present in **db_images/** directory.
The naming of the images should be the crowns' IDs followed by the type of image i.e. in or out. The code is tested for jpg files.

If the ID has specific length, then the *id_length* parameter in *rename_files* function call in *db_creator* should be changed.
Otherwise keep it 0.

pass the correct path to images in main function.

db_creator.py will then

1. Rename the files to specific format
2. Restructure the directory tree
3. Detect crowns in the images and crop to these crowns.
4. Extract crowns and make the background black and replace the original image.
5. Apply data augmentation to the crown images to cover all rotations possible.
6. Equalize histogram of images to get correct contrast.
7. Extract features from these crowns and create a database of dictionary with **Key = id** and **value = feature array**

|

**2. detector.py**

This file will be used for testing and crown detection.
The images should be kept in **test_images/** directory. Name of the file does not matter.
The detector is capable of detecting multiple crowns from a single image. Keep all crowns together and pass the photo to the function. (*Recommendation: crowns should not touch each other. Although the image processing is capable of detecting light contacts between crowns, this might reduce the detection accuracy*)

detector.py will then

1. Detect crowns in the image
2. Extract crowns and make the background black removing all background noise.
3. Equalize histogram of images to get correct contrast.
4. Get crown features from the images using Keras model for each crown.
5. Get database from the memory and search the closest feature array by calculating MSE.
6. Return the image as well as the crown ID with lowest MSE in dictionaries.
7. Get collage of all crowns and their ID in the database by stacking the crowns' images in order.
8. Plot the MSE graphs and save them along with the collage.

|

**Note**

1. test_detector.py is a working detector while remaining completely independent of other local packages. But this makes the code hard to maintain and makes it less readable.
2. Requirements.txt file provides all the dependencies for this project.
3. **Model/** contains the Keras Model for feature extraction