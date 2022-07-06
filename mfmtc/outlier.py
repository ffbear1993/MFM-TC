import matlab
import numpy as np
from numpy.core.numeric import full

from mfmtc import CONFIG, LIB_LRTC, LIB_STDC, LOGGER
from mfmtc.data import MatData
from mfmtc.dataset import MorphoDataset

from itertools import product


class Outlier:

    def __init__(self, X: np.ndarray, tc_mask: np.ndarray):
        self.X = X
        self.Y = X * tc_mask

        self.tc_mask = tc_mask
        self.tc_data = None

    @classmethod
    def checker(cls, X: np.ndarray):
        '''
        X: shape is [n_samples, n_regions, n_metrics]
        tc_mask: 0 missing, 1 valued
        '''
        coef = 1.5

        q = np.percentile(X, [25, 75], axis=0)
        q_lower = q[0, :, :]
        q_upper = q[1, :, :]

        iqr = q_upper - q_lower

        upper = q_upper + iqr * coef
        lower = q_lower - iqr * coef

        outlier_indices = np.where((X > upper) | (X < lower))

        tc_mask = np.ones_like(X)
        tc_mask[outlier_indices] = 0

        return cls(X, tc_mask)

    # def save(self, data_fullpath, mask_fullpath):
    #     data = self.tc_data
    #     mask = self.tc_mask

    #     MatData(data).save(data_fullpath)
    #     MatData(mask).save(mask_fullpath)

    def LRTC(self):
        '''
        Noted the input of X: shape should be tranposed from [n_samples, n_regions, n_metrics] to [n_regions, n_metrics, n_samples] same as the mask.
        merge the code with references/repositories/MainTensorCompletion_2015.m
        input and output: [n_samples, n_regions, n_metrics]
        '''
        rho = 1e0
        max_iter = 500
        epsilon = 1e-5

        X = self.X
        Y = self.Y
        M = self.tc_mask.astype(np.bool)

        X = np.transpose(X, [1, 2, 0])
        Y = np.transpose(Y, [1, 2, 0])
        M = np.transpose(M, [1, 2, 0])
        T = Y / np.sqrt(np.sum(np.square(Y.flatten())))

        # IMPORTANCE! LRTC 0 misssing 1 valued
        M_lrtc = M

        alpha = np.array([1, 1, 1])
        alpha = alpha / np.sum(alpha)

        T_matlab = matlab.double(T.tolist())
        M_matlab = matlab.logical(M_lrtc.tolist())
        alpha_matlab = matlab.double(alpha.tolist())

        X_comp, _ = LIB_LRTC.HaLRTC(T_matlab,
                                    M_matlab,
                                    alpha_matlab,
                                    rho,
                                    max_iter,
                                    epsilon,
                                    nargout=2)

        X_comp = np.array(X_comp)
        X_comp = X_comp * np.sqrt(np.sum(np.square(Y.flatten())))

        self.tc_data = X * M + X_comp * ~M
        self.tc_data = np.transpose(self.tc_data, [2, 0, 1])

        return self

    def STDC(self):
        '''
        Noted the input of X: shape should be tranposed from [n_samples, n_regions, n_metrics] to [n_regions, n_metrics, n_samples] same as the mask.
        merge the code with references/repositories/MainTensorCompletion_2015.m
        input and output: [n_samples, n_regions, n_metrics]
        '''
        para_Lx = {}
        para_Lx['print_mode'] = 0
        para_Lx['maxitr'] = 100
        para_Lx['tau'] = 0.1
        para_Lx['omega'] = float(np.power(10, 0.4))

        X = self.X
        Y = self.Y
        M = self.tc_mask.astype(np.bool)

        X = np.transpose(X, [1, 2, 0])
        Y = np.transpose(Y, [1, 2, 0])
        M = np.transpose(M, [1, 2, 0])

        # IMPORTANCE! STDC 1 misssing 0 valued
        M_stdc = ~M

        Y_matlab = matlab.double(Y.tolist())
        M_matlab = matlab.logical(M_stdc.tolist())

        _, _, _, X_comp = LIB_STDC.STDC(Y_matlab,
                                        M_matlab,
                                        para_Lx,
                                        0,
                                        Y_matlab,
                                        nargout=4)

        X_comp = np.array(X_comp)

        self.tc_data = X * M + X_comp * ~M
        self.tc_data = np.transpose(self.tc_data, [2, 0, 1])

        return self


if __name__ == "__main__":
    pass
