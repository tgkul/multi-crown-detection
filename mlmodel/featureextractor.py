from keras.preprocessing.image import img_to_array
from keras.applications.resnet50 import preprocess_input
from numpy import expand_dims


def get_features(img, model):
    img_data = img_to_array(img.resize((224, 224)))
    img_data = expand_dims(img_data, axis=0)
    img_data = preprocess_input(img_data)
    return model.predict(img_data)
