"""Format differce between two data structures in json like format."""


import itertools
from typing import Any, Tuple, Union

import gendiff.differ.diff_tree_generator as diff_tree_generator

REPLACER = ' '
SPACE_COUNT = 4
SELF_NAME = 'stylish'


def format_diff(diff_result: dict):
    """
    Make string representation of difference result.

    Args:
        diff_result (dict): Comparasion result.

    Returns:
        string: Converted to sting difference result.
    """

    def iter_node(childen, depth):  # noqa:WPS430
        lines = []
        for node in childen:
            deep_indent_size, deep_indent, current_indent = get_intends(depth)
            if not node.get(diff_tree_generator.NODE_ATTRIBUTE_CHILDREN):
                lines.extend(
                    process_diff(
                        node.get(diff_tree_generator.NODE_ATTRIBUTE_VALUE),
                        node.get(diff_tree_generator.NODE_ATTRIBUTE_KEY),
                        deep_indent,
                        deep_indent_size,
                    ),
                )
                continue
            lines.append(
                format_line(
                    deep_indent,
                    node.get(diff_tree_generator.NODE_ATTRIBUTE_KEY),
                    iter_node(
                        node.get(diff_tree_generator.NODE_ATTRIBUTE_CHILDREN),
                        deep_indent_size,
                    ),
                ),
            )
        return '\n'.join(
            itertools.chain('{', lines, [current_indent + '}']),  # noqa:WPS336
        )

    return iter_node(diff_result, 0)


def process_diff(
    diff: dict,
    key: str,
    deep_indent: str,
    deep_indent_size: int,
) -> list:
    """Process diff.

    Args:
        diff (dict): [description]
        key (str): [description]
        deep_indent (str): [description]
        deep_indent_size (int): [description]

    Returns:
        list: List of diff lines
    """
    diff_lines = []
    for sign, node_value in diff.items():
        diff_lines.append(
            format_line(
                get_formated_intend(deep_indent, sign),
                key,
                stringify(node_value, deep_indent_size),
            ),
        )
    return diff_lines


def format_line(indent: str, key: str, value: str) -> str:  # noqa:WPS110
    """Format line.

    Args:
        indent (str): [description]
        key (str): [description]
        value (str): [description]

    Returns:
        str: [description]
    """
    return f'{indent}{key}: {value}'  # noqa:WPS305, WPS110


def stringify(current_value: Any, depth: int) -> str:  # noqa:WPS210
    """Convert passed value to a string.

    Args:
        current_value (Any): Value to stringify
        depth (int): Depth of the value in the tree

    Returns:
        str: String representation of the value
    """
    if not isinstance(current_value, dict):
        if not isinstance(current_value, list):
            return to_string(current_value)
    deep_indent_size, deep_indent, current_indent = get_intends(depth)
    lines = []
    for key, value in current_value.items():  # noqa:WPS110
        lines.append(
            format_line(deep_indent, key, stringify(value, deep_indent_size)),
        )
    return '\n'.join(
        itertools.chain('{', lines, [current_indent + '}']),  # noqa:WPS336
    )


def get_formated_intend(char_seq, sign=None):
    """
    Convert intend char list to string and puts sign if provided.

    Args:
        char_seq (list): List of intend chars.
        sign (str): Sign char to replace intend char.

    Returns:
        string: intend as as a sting.
    """
    cur_deep_indent = list(char_seq)
    if sign:
        cur_deep_indent[-2] = sign
    return ''.join(cur_deep_indent)


def get_intends(depth) -> Tuple:
    """Colculate intends base on the depth.

    Args:
        depth (int): Depth

    Returns:
        Tuple: Tuple of calculated intends
    """
    deep_indent_size = depth + SPACE_COUNT
    deep_indent = REPLACER * deep_indent_size
    current_indent = REPLACER * depth
    return (deep_indent_size, deep_indent, current_indent)


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
