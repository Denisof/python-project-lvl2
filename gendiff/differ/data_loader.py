"""Provides loader base on the file extendios."""
import json
import os
from functools import partial

import yaml

yml_loader = partial(yaml.load, Loader=yaml.SafeLoader)
GET_LOADER = {
    '.json': json.loads,
    '.yaml': yml_loader,
    '.yml': yml_loader,
}.get


def load(file_path: str):
    """Load data structure from the provided path.

    Args:
        file_path (str): File path.

    Raises:
        ValueError: [description]

    Returns:
         dict: Data.
    """
    file_format = os.path.splitext(file_path)[1].lower()
    loader = GET_LOADER(file_format)
    if loader:
        with open(file_path, 'r') as fl:
            return loader(fl.read())
    raise ValueError('Wrong file extension {0}'.format(file_path))
