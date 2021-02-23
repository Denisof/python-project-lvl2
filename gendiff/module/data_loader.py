"""Provides loader base on the file extendios."""
import json
import yaml
from functools import partial

FORMATS_TO_LOADER_MAP = {'.json': json.loads, '.yaml': partial(yaml.load, Loader=yaml.SafeLoader)}

def load(file_path:str):
    """
    Loads data structure from the provided path

    Args:
        file_path (str): File path.

    Returns:
        dict: Data.
    """
    for format, loader in FORMATS_TO_LOADER_MAP.items():
        if file_path.endswith(format):
            return loader(open_file(file_path))
    return {}

def open_file(file_path):
    """
    Return difference in between two json files.

    Args:
        file_name (str): File path.

    Returns:
        string: File full content.
    """
    with open(file_path, 'r') as fl:
        return fl.read()
