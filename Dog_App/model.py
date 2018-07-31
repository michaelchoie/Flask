import numpy as np
import os
import warnings
from keras import applications
from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.callbacks import ModelCheckpoint
from keras.models import load_model, Model
from keras.layers import GlobalAveragePooling2D, BatchNormalization, Dense, Dropout, Flatten
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


def _preprocess_image(path):
    img = image.load_img(path, target_size=(224, 224))
    x = image.img_to_array(img)

    return np.expand_dims(x, axis=0)


def _preprocess_images(paths):
    '''Make all images a 4D tensor and normalized'''
    warnings.filterwarnings('error', message='Palette images with Transparency', category=UserWarning)

    list_of_images = []

    for path in paths:

        try:
            tensor = _preprocess_image(path)
        except:
            print(f"Removing {path}")
            os.remove(path)
            continue

        list_of_images.append(tensor)

    return np.vstack(list_of_images)


def _create_model(path):
    '''Use an established CNN to conduct transfer learning'''

    num_classes = len(os.listdir(f"{path}/train"))

    # Create model
    base_model = ResNet50(weights='imagenet', include_top=False,
                          input_shape=(224,224,3))

    for layer in base_model.layers[:-3]:
        layer.trainable = False

    x = base_model.output
    x = GlobalAveragePooling2D(input_shape=base_model.output_shape[1:])(x)
    x = BatchNormalization(axis=1)(x)
    x = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=x)

    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam',
                  metrics=['accuracy'])

    return model


def _train_model(model, files, targets):
    '''Train the model'''

    checkpointer = ModelCheckpoint(filepath='best_model.hdf5', verbose=1,
                                   save_best_only=True)

    model.fit(files[0], targets[0],
              validation_data=(files[1], targets[1]),
              epochs=3, batch_size=256, callbacks=[checkpointer],
              verbose=1)

    print("Model trained and saved.")


def _test_model(model, test, targets):
    '''Test the model'''

    pred = [np.argmax(model.predict(np.expand_dims(file, axis=0))) for file in test]
    test_accuracy = np.round(100 * np.sum(np.equal(np.array(pred), np.argmax(targets, axis=1))) / len(pred), 2)

    print(f"This model has a test accuracy of {test_accuracy}%")


def output_result(path, img_folder):
    '''Public function to handle creating and saving the CNN'''
    path = f"{path}/{img_folder}"
    files, targets = _load_datasets(path)

    for x in range(3):
        files[x] = _preprocess_images(files[x])

    model = _create_model(path)
    _train_model(model, files, targets)
    _test_model(model, files[2], targets[2])


if __name__ == "__main__":
    output_result(os.getcwd(), 'dog_images')
