"""Format differce between two data structures as plain text."""

from typing import Callable

import gendiff.module.flag as flag
import gendiff.module.formater.helper as helper
import gendiff.module.formater.iterator as formater_iter


def format_diff(source: dict, compare: dict, diff_result: dict):
    """
    Make string representation of difference result.

    Args:
        source (dict): Dict which is compared.
        compare (dict): Dict which is compared with.
        diff_result (dict): File path.

    Returns:
        sting: Converted to sting difference result.
    """
    iterator = formater_iter.get_iterator(get_flag_processor(source, compare))
    iterator = get_result_decorator()(iterator)

    return '\n'.join(iterator(diff_result, []))


def get_flag_processor(source: dict, compare: dict) -> Callable:
    """Return a wrapper of process_value function.

    Args:
        source (dict): Source
        compare (dict): Compare

    Returns:
        Callable: Wrapper function
    """
    flag_map_handlers = {
        flag.FLAG_CHANGED: get_changed_proccessor(source, compare),
        flag.FLAG_ADDED: get_added_proccessor(source, compare),
        flag.FLAG_REMOVED: get_removed_proccessor(source, compare),
        flag.FLAG_UNCHANGED: get_unchanged_proccessor(source, compare),
    }

    def process_flag(prop_value, prop_path, proceed):
        if prop_value in flag.FLAGS:
            return flag_map_handlers[prop_value](prop_path)
        return get_result_decorator()(proceed)(prop_value, prop_path)

    return process_flag


def get_result_decorator() -> Callable:
    """Retrun function which marge the result.

    Returns:
        Callable: Decorator
    """
    result_merged = []

    def wrapper(function):

        def inner(*args, **kwargs):
            lines = function(*args, **kwargs)
            result_merged.extend(lines)
            return result_merged
        return inner
    return wrapper


def get_changed_proccessor(source: dict, compare: dict) -> Callable:
    """Return function for handling changed flag.

    Args:
        source (dict): Source
        compare (dict): Compare

    Returns:
        Callable: Handler function
    """
    string_template = "Property '{0}' was updated. From {1} to {2}"

    def proccessor(prop_path):
        prop_name = helper.get_prop_name(prop_path)
        old_val = helper.to_simple(helper.get_item(source, prop_path))
        new_val = helper.to_simple(helper.get_item(compare, prop_path))
        return [string_template.format(prop_name, old_val, new_val)]
    return proccessor


def get_added_proccessor(source: dict, compare: dict) -> Callable:
    """Return function for handling added flag.

    Args:
        source (dict): Source
        compare (dict): Compare

    Returns:
        Callable: Handler function
    """
    string_template = "Property '{0}' was added with value: {1}"

    def proccessor(prop_path):
        prop_name = helper.get_prop_name(prop_path)
        prop_value = helper.to_simple(helper.get_item(compare, prop_path))
        return [string_template.format(prop_name, prop_value)]
    return proccessor


def get_removed_proccessor(source: dict, compare: dict) -> Callable:
    """Return function for handling removed flag.

    Args:
        source (dict): Source
        compare (dict): Compare

    Returns:
        Callable: Handler function
    """
    string_template = "Property '{0}' was removed"

    def proccessor(prop_path):
        prop_name = helper.get_prop_name(prop_path)
        return [string_template.format(prop_name)]
    return proccessor


def get_unchanged_proccessor(source: dict, compare: dict) -> Callable:
    """Return function for handling unchanged flag.

    Args:
        source (dict): Source
        compare (dict): Compare

    Returns:
        Callable: Handler function
    """

    def proccessor(prop_path):
        return []
    return proccessor
