"""Diff Entry point."""
import collections
import functools
import gendiff.module.data_loader as data_loader  # noqa:WPS301
import gendiff.module.formater.plain as plain  # noqa:WPS301


def generate_diff(first_file, second_file, format: str = 'plain'):
    """
    Return difference in between two json files.

    Args:
        first_file (str): File path.
        second_file (str): File path.
        format (str): output format
    Returns:
        string: Difference in string representation.
    """
    source = data_loader.load(first_file)
    compare = data_loader.load(second_file)

    @format_difference(format, source, compare)
    def get_diff(source, compare):
        """
        Return difference in between two json files.

        Args:
            source (dict): Source dict.
            compare (dict): Compare dict.

        Returns:
            list: Return List  of strings.
        """
        diff = collections.defaultdict(list)
        def walk(source, compare, path):
            for key in sorted(source.keys() | compare.keys()):
                current_path = path + [key]
                if key not in source:
                    diff['added'].append(current_path)
                elif key not in compare:
                    diff['deleted'].append(current_path)
                elif source[key] == compare[key]:
                    diff['unchanged'].append(current_path)
                else:
                    vals_to_compare = [source[key], compare[key]]
                    if all(
                        map(lambda val: isinstance(val, dict), vals_to_compare)
                    ):
                        walk(source[key], compare[key], current_path)
                    else:
                        diff['changed'].append(current_path)
            return diff
        return walk(source, compare, [])
    return get_diff(source, compare)


def format_difference(format, source, compare):
    formater = plain
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            return formater.format(source, compare, result)
        return inner
    return wrapper