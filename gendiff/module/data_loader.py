"""Provides loader base on the file extendios."""
import collections
import json
from functools import partial

import yaml

DataLoader = collections.namedtuple('DataLoader', ['json', 'yaml', 'yml'])
yml_loader = partial(yaml.load, Loader=yaml.SafeLoader)
FORMATS_TO_LOADER_MAP = DataLoader(
    json.loads,
    yml_loader,
    yml_loader,
)


def load(file_path: str):
    """
    Load data structure from the provided path.

    Args:
        file_path (str): File path.

    Returns:
        dict: Data.
    """
    for file_format in FORMATS_TO_LOADER_MAP._fields:  # noqa:WPS437
        if file_path.endswith(file_format):
            loader = getattr(FORMATS_TO_LOADER_MAP, file_format)
            return loader(open_file(file_path))
    return {}


def open_file(file_path):
    """
    Return difference in between two json files.

    Args:
        file_path (str): File path.

    Returns:
        string: File full content.
    """
    with open(file_path, 'r') as fl:
        return fl.read()
