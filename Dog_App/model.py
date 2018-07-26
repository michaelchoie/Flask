import numpy as np
import os
import tqdm
import sys
from io import StringIO
from keras.preprocessing import image
from keras.utils import np_utils
from sklearn.datasets import load_files


def load_dataset(path):
    '''Load text files with categories as subfolder names'''
    data = load_files(path)
    dog_files = np.array(data['filenames'])
    num_classes = len(os.listdir(path))
    dog_targets = np_utils.to_categorical(np.array(data['target']),
                                          num_classes)

    return dog_files, dog_targets

def load_datasets(path):
    files, targets = [], []
    for partition in ['train', 'valid', 'test']:



def resize_image(path):
    '''Make an image a 4D tensor and square'''
    img = image.load_img(path, target_size=(224, 224))
    x = image.img_to_array(img)

    return np.expand_dims(x, axis=0)


def resize_images(paths):
    '''Makes all images suitable for CNN input and uniform size'''
    list_of_images = [resize_image(path) for path in tqdm(paths)]

    return np.vstack(list_of_images)


def something():
    bottleneck_features = np.load('DogResnet50Data.npz')
    train_resnet = bottleneck_features['train']
    valid_resnet = bottleneck_features['valid']
    test_resnet = bottleneck_features['test']


def create_model(files, targets):
    '''Use the an established CNN and conduct transfer learning'''

    # Create model
    model = Sequential()
    model.add(GlobalAveragePooling2D(input_shape=train_resnet.shape[1:]))
    model.add(BatchNormalization(axis=1))
    model.add(Dense(num_classes, activation='softmax'))

    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam',
                  metrics=['accuracy'])

    # Train model
    checkpointer = ModelCheckpoint(filepath='best_model.hdf5', verbose=1,
                                   save_best_only=True)

    model.fit(train, pass,
              validation_data=(valid, pass),
              epochs=20, batch_size=16, callbacks=[checkpointer],
              verbose=1)

if __name__ == "__main__":
    pass