"""Format differce between two data structures in json like format."""

import itertools
from typing import Any, Callable

import gendiff.module.flag as flag
import gendiff.module.formater.helper as helper
import gendiff.module.formater.iterator as formater_iter

REPLACER = (' ')
SPACE_COUNT = 4


def format_diff(source: dict, compare: dict, diff_result: dict):
    """
    Make string representation of difference result.

    Args:
        source (dict): Dict which is compared.
        compare (dict): Dict which is compared with.
        diff_result (dict): File path.

    Returns:
        string: Converted to sting difference result.
    """
    iterator = formater_iter.get_iterator(get_flag_processor(source, compare))
    iterator = get_result_decorator()(iterator)

    return iterator(diff_result, [])


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


def format_line(cur_deep_indent: str, key: str, foramted_val: str) -> str:
    """Wrap strings.

    Args:
        cur_deep_indent (str): Intend
        key (str): key
        foramted_val (str): value

    Returns:
        str: Formated line
    """
    return f'{cur_deep_indent}{key}: {foramted_val}'


def get_flag_processor(source: dict, compare: dict) -> Callable:
    """Return a wrapper of process_value function.

    Args:
        source (dict): Source
        compare (dict): Compare

    Returns:
        Callable: Wrapper function
    """
    flag_map = {
        flag.FLAG_CHANGED: {
            '-': source,
            '+': compare,
        },
        flag.FLAG_ADDED: {
            '+': compare,
        },
        flag.FLAG_UNCHANGED: {
            ' ': source,
        },
        flag.FLAG_REMOVED: {
            '-': source,
        },
    }

    def process_flag(prop_value, prop_path, proceed):
        if prop_value in flag.FLAGS:
            return [
                process_value(
                    helper.get_item(data_source, prop_path),
                    prop_path,
                    proceed,
                    sign,
                )
                for sign, data_source in flag_map[prop_value].items()
            ]
        return [process_value(
            prop_value,
            prop_path,
            proceed,
        )]

    return process_flag


def process_value(
    subject: Any,
    prop_path: list,
    proceed: Callable,
    sign: str = None,
) -> str:
    """Wrap value processing.

    Args:
        subject (Any): Value to proceed
        prop_path (list): Paths of the value
        proceed (Callable): Function to path futher for processing
        sign (str): Sign. Defaults to None.

    Returns:
        str: Formated line
    """
    depth = len(prop_path)
    deep_indent_size = depth * SPACE_COUNT
    cur_deep_indent = get_formated_intend(REPLACER * deep_indent_size, sign)
    if isinstance(subject, dict):
        proceed = get_result_decorator(depth)(proceed)
        foramted_val = proceed(subject, prop_path)
    else:
        foramted_val = helper.to_string(subject)
    return format_line(cur_deep_indent, prop_path[-1], foramted_val)


def get_result_decorator(depth: int = 0) -> Callable:
    """Retrun function which glue the result.

    Args:
        depth (int): Deth of recursion to calculate line intend

    Returns:
        Callable: Decorator
    """
    intend = REPLACER * depth * SPACE_COUNT
    intend = ''.join(intend)

    def wrapper(function):

        def inner(*args, **kwargs):
            lines = function(*args, **kwargs)
            return '\n'.join(
                itertools.chain(
                    '{',
                    lines,
                    [intend + '}'],  # noqa:WPS336
                ),
            )
        return inner
    return wrapper
