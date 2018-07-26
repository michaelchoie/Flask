

def load_dataset(path):
    '''Load text files with categories as subfolder names'''
    data = load_files(path)
    dog_files = np.array(data['filenames'])
    dog_targets = np_utils.to_categorical(np.array(data['target']),
                                          len(np.unique(os.listdir(path))))

    return dog_files, dog_targets


def resize_image(path):
    '''Make an image a 4D tensor and square'''
    img = image.load_img(path, target_size=(224, 224))
    x = image.img_to_array(img)

    return np.expand_dims(x, axis=0)


def resize_images(paths):
    '''Makes all images suitable for CNN input and uniform size'''
    list_of_images = [resize_image(path) for path in tqdm(paths)]

    return np.vstack(list_of_images)