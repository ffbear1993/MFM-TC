from itertools import product

from mfmtc import CONFIG, LOGGER
from mfmtc.data import MatData
from mfmtc.dataset import MorphoDataset

from mfmtc.outlier import Outlier


if __name__ == "__main__":
    for version_item, group_item in product(['old_version', 'new_version'], ['cog', 'gig']):
        fullpath = CONFIG['root'] / CONFIG['morpho'][f'{version_item}'][f'{group_item}']['origin']
        origin_dataset = MorphoDataset.load(fullpath, 0, [2, 0, 1])

        fullpath = CONFIG['root'] / CONFIG['morpho'][f'{version_item}'][f'{group_item}']['origin_outlier_mask']
        outlier_mask = Outlier.checker(origin_dataset.X).tc_mask
        MatData(outlier_mask).save(fullpath)
        LOGGER.debug(outlier_mask.shape)

        fullpath = CONFIG['root'] / CONFIG['morpho'][f'{version_item}'][f'{group_item}']['lrtc_tensor']
        tensor = Outlier.checker(origin_dataset.X).LRTC().tc_data
        MatData(tensor).save(fullpath)
        LOGGER.debug(tensor.shape)

        fullpath = CONFIG['root'] / CONFIG['morpho'][f'{version_item}'][f'{group_item}']['stdc_tensor']
        tensor = Outlier.checker(origin_dataset.X).STDC().tc_data
        MatData(tensor).save(fullpath)
        LOGGER.debug(tensor.shape)