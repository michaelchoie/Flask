import os
import re
import shutil
import warnings
from sklearn.model_selection import train_test_split
from os.path import abspath
from PIL import Image


def _clean_dirnames(path, dl_folder):
    '''Clean the names of dog breed directories'''
    path = f"{path}/{dl_folder}"
    for file in os.listdir(path):
        new_file = re.sub(" dog$", "", file).replace(' ', '_')
        os.rename(f"{path}/{file}",
                  f"{path}/{new_file}")


def _clean_files(path, dl_folder):
    '''Remove spaces, corrupted files, and files that are .ash'''
    warnings.filterwarnings('error', message='Corrupt EXIF data.', category=UserWarning)

    path = f"{path}/{dl_folder}"
    for directory in os.listdir(path):
        for file in os.listdir(f"{path}/{directory}"):
            try:
                Image.open(f"{path}/{directory}/{file}")
            except:
                os.remove(f"{path}/{directory}/{file}")
                continue

            if re.search(".ash$", file) is not None:
                os.remove(f"{path}/{directory}/{file}")
                continue

            new_file = re.sub("^\d*\. ", '', file)
            os.rename(f"{path}/{directory}/{file}",
                      f"{path}/{directory}/{new_file}")


def _create_partition_dirs(path):
    '''Create the train/valid/test folders'''
    for directory in ["train", "valid", "test"]:
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
        valid, test = train_test_split(test, train_size=0.5,
                                            random_state=23)

        for directory in ["train", "valid", "test"]:
            _move_files(eval(directory), breed,
                        f"{path}/{breed}", f"{orig_path}/{directory}")


def setup_data(path, dl_folder):
    '''Public function to handle setting data up'''
    if os.path.exists('dog_images'):
        raise Exception('dog images folder already exists!')
    else:
        os.mkdir("dog_images")

    _clean_dirnames(path, dl_folder)
    _clean_files(path, dl_folder)
    _create_partition_dirs(path)
    _partition_data(path, dl_folder)

    for directory in ["train", "valid", "test"]:
        os.rename(directory, f"dog_images/{directory}")

    # Remove empty directory
    shutil.rmtree(f"{path}/{dl_folder}")

    print("Data prep complete")


if __name__ == "__main__":
    setup_data(os.getcwd(), dl_folder="downloads")
