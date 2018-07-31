=====================
Multi Crown Detection
=====================

Introduction
============

This project contains 2 main files. db_creator.py and detector.py

db_creator.py
^^^^^^^^^^^^^

This file create a database of crown features from the provided images.
For creating or adding images to the database, the files should be present in **db_images/** directory. The naming of the images should be the crowns' IDs followed by the type of image i.e. in or out. The code is tested for jpg files.
If the ID has specific length, then the *id_length* parameter in *rename_files* function call in *db_creator* should be changed. Otherwise keep it *0*.

pass the correct path to images in main function.

db_creator.py will then

1. Rename the files to specific format
2. Restructure the directory tree
3. Detect crowns in the images and crop to these crowns.
4. Extract crowns and make the background black and replace the original image.
5. Apply data augmentation to the crown images to cover all rotations possible.
6. Equalize histogram of images to get correct contrast.
7. Extract features from these crowns and create a database of dictionary with **Key = id** and **value = feature array**