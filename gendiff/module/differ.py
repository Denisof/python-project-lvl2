"""Diff Entry point."""
from itertools import chain

import gendiff.module.data_loader as data_loader  # noqa:WPS301


def generate_diff(first_file, second_file):
    """
    Return difference in between two json files.

    Args:
        first_file (str): File path.
        second_file (str): File path.

    Returns:
        string: Difference in string representation.
    """
    source = data_loader.load(first_file)
    compare = data_loader.load(second_file)
    diff = get_diff(source, compare)
    return '\n'.join(chain('{', diff, '}'))


def get_diff(source, compare):
    """
    Return difference in between two json files.

    Args:
        source (dict): Source dict.
        compare (dict): Compare dict.

    Returns:
        list: Return List  of strings.
    """
    diff = []
    for key in sorted(source.keys() | compare.keys()):
        if key not in source:
            diff.append(f' + {key}: {compare[key]}')
        elif key not in compare:
            diff.append(f' - {key}: {source[key]}')
        elif source[key] == compare[key]:
            diff.append(f'   {key}: {source[key]}')
        else:
            diff.append(f' - {key}: {source[key]}')
            diff.append(f' + {key}: {compare[key]}')
    return diff
