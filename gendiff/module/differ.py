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
    source_json = json.load(open(first_file))
    compare_json = json.load(open(second_file))
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
    return '\n'.join(chain('{', diff, '}'))
