import abc
import pathlib

import numpy as np
import scipy.io

from mfmtc import CONFIG, LOGGER
from mfmtc.data import MatData
'''
output: dataset shape must be (n_samples, n_regions, n_metrics)
'''


class BaseDataset:

    def __init__(self, X, y):
        self.X = X
        self.y = y

    @abc.abstractclassmethod
    def load(cls, fullpath: pathlib.Path, label_value: int, axes: list):
        pass

    @classmethod
    def merge(cls, instance_a, instance_b):
        X = np.concatenate([instance_a.X, instance_b.X], axis=0)
        y = np.concatenate([instance_a.y, instance_b.y], axis=0)
        return cls(X, y)

    def __repr__(self):
        return f'dataset shape {self.X.shape} with label {set(self.y)}'


class MorphoDataset(BaseDataset):

    def __init__(self, X, y, version=None):
        super(MorphoDataset, self).__init__(X, y)
        self.version = version

    @classmethod
    def load(cls, fullpath: pathlib.Path, label_value: int, axes: list):
        X = scipy.io.loadmat(fullpath)
        LOGGER.debug(fullpath)
        X = X[MatData._select_key(X.keys())].transpose(axes)
        y = np.zeros(X.shape[0]) + label_value
        return cls(X, y)

    def __repr__(self):
        return super(MorphoDataset, self).__repr__() + f', {self.version}'

    def __getitem__(self, ids):
        return self.X[ids, :], self.y[ids]

    def __len__(self):
        return len(self.y)


class FuncDataset(BaseDataset):

    def __init__(self, X, y, version=None):
        super(FuncDataset, self).__init__(X, y)
        self.version = version

    @classmethod
    def load(cls, fullpath: pathlib.Path, label_value: int, axes: list):
        LOGGER.debug(fullpath)
        X = scipy.io.loadmat(fullpath)
        X = X[MatData._select_key(X.keys())].transpose(axes)
        y = np.zeros(X.shape[0]) + label_value
        return cls(X, y)

    def __repr__(self):
        return super(FuncDataset, self).__repr__() + f', {self.version}'


def divide_dataset(X, y, label: int):
    '''
    input-X: shape is [n_samples, n_regions, n_metrics]
    '''
    sub_X_indices = np.where(y == label)
    sub_X = np.squeeze(X[sub_X_indices, :, :])
    return sub_X


if __name__ == "__main__":
    pass
