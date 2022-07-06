import sys
from pathlib import Path

import LRTC
import STDC
import yaml
from loguru import logger


def initialize():
    root = Path(__file__).parent.parent

    fullpath = root / 'config.yml'
    with open(fullpath, 'r') as config_file:
        config = yaml.safe_load(config_file)
    with open(fullpath, 'w') as config_file:
        config['version'] += 1
        yaml.safe_dump(config, config_file, sort_keys=False)

    config['root'] = root

    logger.remove()
    logger.add(sys.stdout, colorize=True, level=config['logger_level'])
    logger.info('initializing...')
    logger.info(f'config is loaded with version {config["version"]}')

    
    if config['matlab_level']:
        lrtc = LRTC.initialize()
        stdc = STDC.initialize()
    else:
        lrtc = None
        stdc = None

    return config, logger, lrtc, stdc


try:
    CONFIG
except NameError:
    CONFIG, LOGGER, LIB_LRTC, LIB_STDC = initialize()
