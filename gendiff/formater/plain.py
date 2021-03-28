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
    filter(bool, diff_lines)
    return '\n'.join(filter(bool, diff_lines))


def process_meta(diff_path: list, diff_meta: dict) -> Optional[str]:
    """Process meta.

    Args:
        diff_path (list): [description]
        diff_meta (dict): [description]

    Returns:
        Optional(str): [description]
    """
    diff_proccessors_chain = [
        process_changed,
        process_added,
        process_removed,
    ]
    for processor in diff_proccessors_chain:
        proccess_result = processor(diff_path, diff_meta)
        if proccess_result:
            return proccess_result


def process_changed(diff_path: list, diff_meta: dict) -> Optional[str]:
    """Process Changed.

    Args:
        diff_path (list): [description]
        diff_meta (dict): [description]

    Returns:
        [type]: [description]
    """
    if (diff_tree_generator.FLAG_ADDED in diff_meta):
        if (diff_tree_generator.FLAG_REMOVED in diff_meta):
            diff_template = "Property '{0}' was updated. From {1} to {2}"
            diff_data = ['.'.join(diff_path)]
            diff_data.append(
                to_simple(diff_meta.get(diff_tree_generator.FLAG_REMOVED)),
            )
            diff_data.append(
                to_simple(diff_meta.get(diff_tree_generator.FLAG_ADDED)),
            )
            return diff_template.format(*diff_data)
    return None


def process_added(diff_path: list, diff_meta: dict) -> Optional[str]:
    """Process Added.

    Args:
        diff_path (list): [description]
        diff_meta (dict): [description]

    Returns:
        [type]: [description]
    """
    if diff_tree_generator.FLAG_ADDED in diff_meta:
        diff_template = "Property '{0}' was added with value: {1}"
        diff_data = ['.'.join(diff_path)]
        diff_data.append(
            to_simple(diff_meta.get(diff_tree_generator.FLAG_ADDED)),
        )
        return diff_template.format(*diff_data)
    return None


def process_removed(diff_path: list, diff_meta: dict) -> Optional[str]:
    """Process Removed.

    Args:
        diff_path (list): [description]
        diff_meta (dict): [description]

    Returns:
        [type]: [description]
    """
    if diff_tree_generator.FLAG_REMOVED in diff_meta:
        diff_template = "Property '{0}' was removed"
        return diff_template.format('.'.join(diff_path))
    return None


def to_simple(subject: Any) -> str:
    """Transofm object to a string.

    Args:
        subject (Any): Object to manupulate

    Returns:
        str: Formated object
    """
    if not isinstance(subject, dict):
        if isinstance(subject, str):
            return "'{0}'".format(subject)
        return to_string(subject)
    return '[complex value]'


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
