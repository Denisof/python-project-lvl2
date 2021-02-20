"""Diff Entry point."""
import json
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
    source_json = json.loads(read_file(first_file))
    compare_json = json.load(read_file(second_file))
    diff = get_diff(source_json, compare_json)
    return '\n'.join(chain('{', diff, '}'))


def read_file(file_name):
    """
    Return difference in between two json files.

    Args:
        file_name (str): File path.

    Returns:
        string: File full content.
    """
    with open(file_name) as fl:
        return fl.read()


def get_diff(source_json, compare_json):
    """
    Return difference in between two json files.

    Args:
        source_json (dict): Source dict.
        compare_json (dict): Compare dict.

    Returns:
        list: Return List  of strings.
    """
    diff = []
    for key in sorted(source_json.keys() | compare_json.keys()):
        if key not in source_json:
            diff.append(f' + {key}: {compare_json[key]}')
        elif key not in compare_json:
            diff.append(f' - {key}: {source_json[key]}')
        elif source_json[key] == compare_json[key]:
            diff.append(f'   {key}: {source_json[key]}')
        else:
            diff.append(f' - {key}: {source_json[key]}')
            diff.append(f' + {key}: {compare_json[key]}')
    return diff
