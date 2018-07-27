import numpy as np
import os
import sys
import warnings
from io import StringIO
from keras import applications
from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.callbacks import ModelCheckpoint
from keras.models import Model
from keras.layers import GlobalAveragePooling2D, BatchNormalization, Dense, Dropout
from keras.preprocessing import image
from keras.utils import np_utils
from sklearn.datasets import load_files


def _load_dataset(path):
    '''Load text files with categories as subfolder names'''
    data = load_files(path)
    dog_files = np.array(data['filenames'])
    num_classes = len(os.listdir(path))
    dog_targets = np_utils.to_categorical(np.array(data['target']),
                                          num_classes)

    return dog_files, dog_targets


def _load_datasets(path):
    all_files, all_targets = [], []
    for partition in ['train', 'valid', 'test']:
        files, targets = _load_dataset(f"{path}/{partition}")
        all_files.append(files)
        all_targets.append(targets)

    return all_files, all_targets


def _preprocess_images(paths):
    '''Make all images a 4D tensor and normalized'''
    warnings.filterwarnings('error', message='Palette images with Transparency', category=UserWarning)

    list_of_images = []

    for path in paths:

        try:
            img = image.load_img(path, target_size=(224, 224))
            x = image.img_to_array(img)
        except:
            os.remove(path)
            continue

        list_of_images.append(preprocess_input(np.expand_dims(x, axis=0)))

    return np.vstack(list_of_images)


"""
def _bottleneck_features(path):
    '''Retrieve frozen trained layers from established CNN'''
    bottleneck_features = np.load('DogResnet50Data.npz')
    resnet = []
    for partition in ['train', 'valid', 'test']:
        resnet.append(bottleneck_features[partition])

    return resnet
"""


def _create_model():

    num_classes = len(os.listdir(f"{path}/train"))

    # Create model
    base_model = ResNet50(weights='imagenet', include_top=False)
    x = base_model.output
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.2)(x)
    x = GlobalAveragePooling2D()(x)
    x = BatchNormalization(axis=1)(x)
    predictions = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)

    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam',
                  metrics=['accuracy'])


# TODO: epochs
def _train_model(files, targets, path):
    '''Use an established CNN to conduct transfer learning'''

    num_classes = len(os.listdir(f"{path}/train"))

    # Create model
    base_model = ResNet50(weights='imagenet', include_top=False)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.2)(x)
    x = BatchNormalization(axis=1)(x)
    predictions = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)

    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam',
                  metrics=['accuracy'])

    # Train model
    checkpointer = ModelCheckpoint(filepath='best_model.hdf5', verbose=1,
                                   save_best_only=True)

    model.fit(files[0], targets[0],
              validation_data=(files[1], targets[1]),
              epochs=1, batch_size=32, callbacks=[checkpointer],
              verbose=1)

    predictions = [np.argmax(model.predict(file)) for file in files[2]]

    test_accuracy = round(100 * np.sum(np.array(predictions) == np.argmax(targets[2], axis=1)) / len(predictions), 2)

    print('''
            Model trained and saved.
            This model has a test accuracy of {test_accuracy}%
          ''')


def create_model(path, img_folder):
    '''Public function to handle creating and saving the CNN'''
    files, targets = _load_datasets(f"{path}/{img_folder}")
    # bottleneck_features = _bottleneck_features(path)
    for x in range(3):
        files[x] = _preprocess_images(files[x])

    _train_model(files, targets, f"{path}/{img_folder}")


if __name__ == "__main__":
    create_model(os.getcwd(), 'dog_images')
