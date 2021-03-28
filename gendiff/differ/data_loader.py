"""Provides loader base on the file extendios."""
import json
from functools import partial

import yaml

yml_loader = partial(yaml.load, Loader=yaml.SafeLoader)
data_loaders = {
    'json': json.loads,
    'yaml': yml_loader,
    'yml': yml_loader,
}


def load(file_path: str):
    """Load data structure from the provided path.

    Args:
        file_path (str): File path.

    Raises:
        ValueError: [description]

    Returns:
         dict: Data.
    """
    for file_format in data_loaders.keys():
        if file_path.split('.')[-1].lower() == file_format:
            loader = data_loaders[file_format]
            with open(file_path, 'r') as fl:
                return loader(fl.read())
    raise ValueError('Wrong file extension {0}'.format(file_path))
