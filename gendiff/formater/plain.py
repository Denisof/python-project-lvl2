"""Format differce between two data structures as plain text."""

from itertools import starmap
from typing import Any, Optional, Union

import gendiff.differ.diff_tree_generator as diff_tree_generator
import gendiff.formater.iterator as formater_iter

SELF_NAME = 'plain'


def format_diff(diff_result: dict) -> str:
    """
    Make string representation of difference result.

    Args:
        diff_result (dict): File path.

    Returns:
        str: Converted to sting difference result.
    """
    diff_lines = starmap(
        process_meta,
        formater_iter.iter_node(diff_result, []),
    )
    return '\n'.join(filter(bool, diff_lines))


def process_meta(diff_path: list, diff_meta: dict) -> Optional[str]:
    """Process meta.

    Args:
        diff_path (list): [description]
        diff_meta (dict): [description]

    Returns:
        Optional(str): [description]
    """
    diff_template = "Property '{0}' was "
    diff_data = ['.'.join(diff_path)]
    status = diff_meta[diff_tree_generator.STATUS_COLUMN]
    if status == diff_tree_generator.STATUS_REMOVED:
        diff_template += 'removed'  # noqa: WPS336
        return diff_template.format(*diff_data)

    if status == diff_tree_generator.STATUS_ADDED:
        diff_template += 'added with value: {1}'  # noqa: WPS336
        diff_data.append(
            to_simple(diff_meta[diff_tree_generator.VALUE_IS]),
        )
        return diff_template.format(*diff_data)

    if status == diff_tree_generator.STATUS_CHANGED:
        diff_template += 'updated. From {1} to {2}'  # noqa: WPS336
        diff_data.extend(
            [
                to_simple(diff_meta[diff_tree_generator.VALUE_WAS]),
                to_simple(diff_meta[diff_tree_generator.VALUE_IS]),
            ],
        )
        return diff_template.format(*diff_data)


def to_simple(subject: Any) -> str:
    """Transofm object to a string.

    Args:
        subject (Any): Object to manupulate

    Returns:
        str: Formated object
    """
    if isinstance(subject, (dict, list)):
        return '[complex value]'
    if isinstance(subject, str):
        return "'{0}'".format(subject)
    return to_string(subject)


def to_string(subject: Union[str, int, bool, None, float]):
    """Convert value to string.

    Args:
        subject (Union[str, int, bool, None, float]): Subject to convert

    Returns:
        str: Converted string representation.
    """
    if isinstance(subject, bool):
        return str(subject).lower()
    elif subject == None:  # noqa:E711
        return 'null'
    return str(subject)
