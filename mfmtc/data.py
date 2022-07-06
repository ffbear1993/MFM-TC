import abc
import pathlib

import numpy as np
import scipy.io

from mfmtc import LOGGER
'''
output: data
'''


class BaseData:

    def __init__(self, data):
        self.data = data

    @abc.abstractclassmethod
    def load(cls):
        pass

    @abc.abstractmethod
    def save(self):
        pass


class MatData(BaseData):

    @staticmethod
    def _select_key(keys: list, spec_key=None):
        key = filter(lambda str: not str.startswith('__'), keys)
        return list(key)[0] if spec_key is None else spec_key

    @classmethod
    def load(cls, fullpath: pathlib.Path, axes: list = None, spec_key=None):
        # LOGGER.debug(fullpath)
        data = scipy.io.loadmat(fullpath)
        data = data[cls._select_key(data.keys(), spec_key)]
        data = np.squeeze(data)
        data = np.transpose(data, axes) if axes else data
        return cls(data)

    def save(self, fullpath: pathlib.Path):
        # LOGGER.debug(fullpath)
        parent = fullpath.parent
        parent.mkdir(parents=True, exist_ok=True)
        scipy.io.savemat(fullpath, {'data': self.data})

    def __repr__(self):
        return f'data shape {self.data.shape}'


class NpyData(BaseData):

    @classmethod
    def load(cls, fullpath: pathlib.Path):
        LOGGER.debug(fullpath)
        data = np.load(fullpath)
        return cls(data)

    def save(self, fullpath: pathlib.Path):
        LOGGER.debug(fullpath)
        parent = fullpath.parent
        parent.mkdir(parents=True, exist_ok=True)
        np.save(fullpath, self.data)
