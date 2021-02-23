"""Diff Entry point."""
import gendiff.module.data_loader as data_loader
from itertools import chain


def generate_diff(first_file, second_file):
    """
    Return difference in between two json files.

    Args:
        first_file (str): File path.
        second_file (str): File path.

    Returns:
        string: Difference in string representation.
    """
    source_ = data_loader.load(first_file)
    compare_ = data_loader.load(second_file)
    diff = get_diff(source_, compare_)
    return '\n'.join(chain('{', diff, '}'))




def get_diff(source_, compare_):
    """
    Return difference in between two json files.

    Args:
        source_json (dict): Source dict.
        compare_json (dict): Compare dict.

    Returns:
        list: Return List  of strings.
    """
    diff = []
    for key in sorted(source_.keys() | compare_.keys()):
        if key not in source_:
            diff.append(f' + {key}: {compare_[key]}')
        elif key not in compare_:
            diff.append(f' - {key}: {source_[key]}')
        elif source_[key] == compare_[key]:
            diff.append(f'   {key}: {source_[key]}')
        else:
            diff.append(f' - {key}: {source_[key]}')
            diff.append(f' + {key}: {compare_[key]}')
    return diff
