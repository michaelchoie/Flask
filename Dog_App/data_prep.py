import numpy as np
import os
import re
import shutil
import tqdm
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from keras.preprocessing import image
from keras.utils import np_utils
from os.path import abspath


def _clean_dirnames(path, dl_folder):
    '''Clean the names of dog breed directories'''
    path = f"{path}/{dl_folder}"
    for file in os.listdir(path):
        new_file = re.sub(" dog$", "", file)
        os.rename(f"{path}/{file}",
                  f"{path}/{new_file}")


def _clean_files(path, dl_folder):
    '''Remove image files that are .ash'''
    path = f"{path}/{dl_folder}"
    for directory in os.listdir(path):
        ash_files = list(filter(lambda x: re.search(".ash$", x),
                                os.listdir(f"{path}/{directory}")))
        for file in ash_files:
            os.remove(f"{path}/{directory}/{file}")


def _create_partition_dirs(path):
    '''Create the train/valid/test folders'''
    for directory in ["train", "validation", "test"]:
        os.mkdir(f"{path}/{directory}")


def _move_files(files, breed, start, end):
    '''Create breed directory and move images to partition folder'''
    path = f"{end}/{breed}"
    os.mkdir(path)
    for file in files:
        os.rename(f"{start}/{file}", f"{path}/{file}")


def _partition_data(path, dl_folder):
    '''Partition data and move files to appropriate dirs'''
    orig_path = path
    path = f"{path}/{dl_folder}"
    for breed in os.listdir(path):
        pictures = os.listdir(abspath(f"{path}/{breed}"))
        train, test = train_test_split(pictures, train_size=0.8,
                                       random_state=23)
        validation, test = train_test_split(test, train_size=0.5,
                                            random_state=23)

        for directory in ["train", "validation", "test"]:
            _move_files(eval(directory), breed,
                        f"{path}/{breed}", f"{orig_path}/{directory}")

    # Remove empty directory
    shutil.rmtree(path)


def setup_data(path, dl_folder):
    '''Public function to handle setting data up'''
    _clean_dirnames(path, dl_folder)
    _clean_files(path, dl_folder)
    _create_partition_dirs(path)
    _partition_data(path, dl_folder)

    os.mkdir("dog_images")

    for directory in ["train", "validation", "test"]:
        os.rename(directory, f"dog_images/{directory}")

    print("Data prep complete")


if __name__ == "__main__":
    setup_data(os.getcwd(), dl_folder="downloads")
