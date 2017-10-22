import numpy as np
from skimage import io
from skimage.transform import resize

import matplotlib.pyplot as plt
import glob
import h5py


class MoleImages():
    def __init__(self, dir=None):
        self.dir = dir
        self.size = None

    def resize_bulk(self, size=(128,128)):
        '''
        Resize Images and create matrix
        Input: size of the images (128,128)
        Output: Numpy array of (size,num_images)
        '''
        self.size = size
        X = []
        image_list = glob.glob(self.dir)
        n_images = len(image_list)
        print('Resizing {} images:'.format(n_images))
        for i, imgfile in enumerate(image_list):
            print('Resizing image {} of {}'.format(i+1, n_images))
            img = io.imread(imgfile)
            img = resize(img, self.size)
            X.append(img)
        return np.array(X)

    def save_h5(self, X, filename, dataset):
        '''
        Save a numpy array to a data.h5 file specified.
        Input:
        X: Numpy array to save
        filename: name of h5 file
        dataset: label for the dataset
        '''
        with h5py.File(filename, 'w') as hf:
            hf.create_dataset(dataset, data=X)
        print('File {} saved'.format(filename))

    def load_h5(self, filename, dataset):
        '''
        Load a data.h5 file specified.
        Input: filename, dataset
        Output: Data
        '''
        with h5py.File(filename, 'r') as hf:
            return hf[dataset][:]


if __name__ == '__main__':
    benign = MoleImages('data/benign/*.jpg')
    ben_images = benign.resize_bulk()
    print('Shape of benign images: ', ben_images.shape)
    benign.save_h5(ben_images, 'benigns.h5', 'benign')
